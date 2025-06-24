import requests
import csv
import time


def fetch_coinmarketcap_data(start=1, limit=100):
    url = f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start={start}&limit={limit}&sortBy=market_cap&sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinMarketCap: {e}")
        return None
    
def write_to_csv(all_data, filename='coinmarketcap_data_internal.csv'):
    if not all_data:
        print("No data to write.")
        return
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        header = ['Rank', 'Name', 'Symbol', 'Price (USD)', '24h % Change', 'Market Cap (USD)']
        writer.writerow(header)
        
        for crypto_data in all_data:
            crypto_list = crypto_data['data']['cryptoCurrencyList']
            for coin in crypto_list:
                # Find USD quote
                usd_quote = None
                for quote in coin['quotes']:
                    if quote['name'] == 'USD':
                        usd_quote = quote
                        break
                
                if usd_quote:
                    row = [
                        coin['cmcRank'],
                        coin['name'],
                        coin['symbol'],
                        f"${usd_quote['price']:.2f}",
                        f"{usd_quote['percentChange24h']:.2f}%",
                        f"${usd_quote['marketCap']:,.0f}"
                    ]
                    writer.writerow(row)


def fetch_multiple_pages(pages=5, coins_per_page=100):
    all_data = []
    
    for page in range(pages):
        start = page * coins_per_page + 1
        print(f"Fetching page {page + 1}/5 (coins {start}-{start + coins_per_page - 1})...")
        
        data = fetch_coinmarketcap_data(start, coins_per_page)
        if data and 'data' in data and 'cryptoCurrencyList' in data['data']:
            all_data.append(data)
            print(f"Successfully fetched {len(data['data']['cryptoCurrencyList'])} coins")
        else:
            print(f"Failed to fetch page {page + 1}")
        
        if page < pages - 1:
            time.sleep(1)
    
    return all_data

if __name__ == "__main__":
    print("Fetching cryptocurrency data from CoinMarketCap...")
    all_data = fetch_multiple_pages(pages=5, coins_per_page=100)
    
    if all_data:
        write_to_csv(all_data)
        total_coins = sum(len(data['data']['cryptoCurrencyList']) for data in all_data)
        print(f"Successfully fetched {total_coins} coins and written to coinmarketcap_data_internal.csv")
    else:
        print("No data was fetched")