from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

def slow_scroll(driver, pause_time=0.5, scroll_step=300):
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    while current_position < last_height:
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(pause_time)
        current_position += scroll_step
        last_height = driver.execute_script("return document.body.scrollHeight")

def parse_coin_row(row):
    try:
        cols = row.find_elements(By.TAG_NAME, 'td')
        rank = cols[1].text.strip()
        name_symbol = cols[2].find_element(By.CSS_SELECTOR, "p.coin-item-name").text.strip()
        symbol = cols[2].find_element(By.CSS_SELECTOR, "p.coin-item-symbol").text.strip()
        price = cols[3].text.strip()
        change_24h = cols[5].text.strip()
        market_cap = cols[7].text.strip()
        return {
            "Rank": rank,
            "Name": name_symbol,
            "Symbol": symbol,
            "Price (USD)": price,
            "24h % Change": change_24h,
            "Market Cap (USD)": market_cap
        }
    except Exception as e:
        print(f"Error parsing row: {e}")
        return None

def scrape_coinmarketcap_selenium():
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    base_url = "https://coinmarketcap.com/?page={}"

    all_data = []

    for page in range(1, 6): 
        print(f"Scraping page {page}...")
        driver.get(base_url.format(page))
        time.sleep(2)
        slow_scroll(driver, pause_time=0.3)

        rows = driver.find_elements(By.XPATH, '//tbody/tr[contains(@style, "cursor") and contains(@style, "pointer")]')

        page_data = []
        for row in rows:
            coin_data = parse_coin_row(row)
            if coin_data:
                page_data.append(coin_data)

        print(f"  Found {len(page_data)} coins")
        all_data.extend(page_data)

    driver.quit()

    # Save to CSV
    with open("coins_data_selenium.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Rank", "Name", "Symbol", "Price (USD)", "24h % Change", "Market Cap (USD)"])
        writer.writeheader()
        writer.writerows(all_data)

    print(f"\n✅ Saved {len(all_data)} coins to coins_data_selenium.csv")

if __name__ == "__main__":
    scrape_coinmarketcap_selenium()
