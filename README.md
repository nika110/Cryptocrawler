# Crypto Trading Tools

This project contains cryptocurrency market analysis tools built for tracking Bitcoin prices and gathering market data from CoinMarketCap.

## Setup

Install required packages:
```bash
pip install -r requirements.txt
```

## Features

### 1. Live Bitcoin Price Tracker (`crypto_crawler.py`)

Real-time Bitcoin price monitoring with moving average calculation.

**Features:**
- Live price updates every second
- 10-period simple moving average
- Automatic retry on API failures
- Clean shutdown with Ctrl+C

**Usage:**
```bash
python crypto_crawler.py
```

Sample output:
```
[2025-06-23T14:30:15] BTC → USD: $42,150.75 SMA(10): $42,098.23
```

### 2. CoinMarketCap Data Collection

Two different approaches for collecting top 500 cryptocurrency data:

#### HTML Scraper (`coinmarketcap_html.py`, `coinmarketcap_json.py`)
- Scrapes data from CoinMarketCap web pages
- Uses BeautifulSoup for HTML parsing
- Handles pagination across 5 pages
- Outputs data to `coins_data_selenium.csv` and `coinmarketcap_json.csv`

#### JSON API Scraper (`coinmarketcap_internal_api.py`)  
- Uses CoinMarketCap's internal API endpoint
- Single request for 100 coins
- Faster and more reliable
- Outputs data to `coinmarketcap_data_internal.csv`

**Data collected:**
- Rank
- Name & Symbol
- Current Price (USD)
- 24h Price Change (%)
- Market Cap (USD)

**Usage:**
```bash
python coinmarketcap_html.py    # HTML approach
python coinmarketcap_json.py    # JSON approach
python coinmarketcap_internal_api.py    # JSON Internal API approach

```

## Performance Comparison

The JSON API approach significantly outperforms HTML scraping:

