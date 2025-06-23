import requests
from bs4 import BeautifulSoup
import json
import csv

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_coins = []

for page in range(1, 6):
    print(f"Scraping page {page}...")
    url = f"https://coinmarketcap.com/?page={page}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    script_tag = soup.find("script", id="__NEXT_DATA__")
    json_data = json.loads(script_tag.string)

    try:
        coins = json_data["props"]["dehydratedState"]["queries"][1]["state"]["data"]["data"]["listing"]["cryptoCurrencyList"]

        for coin in coins:
            usd_quote = next((q for q in coin["quotes"] if q["name"] == "USD"), None)
            if not usd_quote:
                continue

            all_coins.append([
                coin.get("cmcRank"),
                coin.get("name"),
                coin.get("symbol"),
                round(usd_quote.get("price", 0), 4),
                round(usd_quote.get("percentChange24h", 0), 2),
                round(usd_quote.get("marketCap", 0), 2)
            ])
    except Exception as e:
        print(f"⚠️ Failed to parse page {page}: {e}")

# Save to CSV
with open("coinmarketcap_json.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Rank", "Name", "Symbol", "Price (USD)", "24h % Change", "Market Cap (USD)"])
    writer.writerows(all_coins)

print("✅ Saved 500 coins to 'coinmarketcap_json.csv'")
