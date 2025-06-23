import requests
import time
import signal
from datetime import datetime

class CryptoCrawler:    
    def __init__(self):
        self.url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_last_updated_at=true"
        self.prices = []
        self.running = True
        self.consecutive_failures = 0
        self.max_failures = 5
        self.current_backoff = 1
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        print("\nShutting down...")
        self.running = False
    
    def fetch_price(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            data = response.json()
            price = data['bitcoin']['usd']
            timestamp = data['bitcoin']['last_updated_at']
            return price, timestamp
        except Exception as e:
            print(f"API call failed: {e}")
            return None
    
    def calculate_sma(self):
        if len(self.prices) == 0:
            return None
        return sum(self.prices) / len(self.prices)
    
    def retry_with_backoff(self):
        for attempt in range(5):
            result = self.fetch_price()
            if result is not None:
                self.consecutive_failures = 0
                self.current_backoff = 1
                return result
            
            if attempt < 4:
                print(f"Retrying in {self.current_backoff} seconds...")
                time.sleep(self.current_backoff)
                self.current_backoff *= 2
        
        self.consecutive_failures += 1
        if self.consecutive_failures >= self.max_failures:
            print(f"ERROR: {self.max_failures} consecutive failures reached. Continuing to poll...")
            self.consecutive_failures = 0
        return None
    
    def format_price(self, price: float) -> str:
        return f"${price:,.2f}"
    
    def run(self):
        print("Starting Bitcoin price poller...")
        print("Press Ctrl-C to stop")
        
        while self.running:
            result = self.retry_with_backoff()
            
            if result is not None:
                price, timestamp = result
                self.prices.append(price)
                
                if len(self.prices) > 10:
                    self.prices.pop(0)
                
                dt = datetime.fromtimestamp(timestamp)
                formatted_time = dt.strftime('%Y-%m-%dT%H:%M:%S')
                
                output = f"[{formatted_time}] BTC → USD: {self.format_price(price)}"
                
                if len(self.prices) >= 10:
                    sma = self.calculate_sma()
                    output += f" SMA(10): {self.format_price(sma)}"
                
                print(output)
            
            if self.running:
                time.sleep(1)

if __name__ == "__main__":
    crawler = CryptoCrawler()
    crawler.run()