import yfinance as yf
import pandas as pd
import time

# 1. List of tickers (you can replace or load more tickers from a file)
tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "JPM", "BAC",
    "INTC", "AMD", "WMT", "T", "VZ", "KO", "PEP", "CSCO", "ADBE", "CRM"
    # Add more tickers here (up to 1000)
]

# 2. Function to download stock data
def download_data(ticker_list, period="1mo", interval="1d"):
    all_data = {}
    for ticker in ticker_list:
        try:
            print(f"📥 Downloading {ticker} ...")
            data = yf.download(ticker, period=period, interval=interval)
            data["Ticker"] = ticker
            all_data[ticker] = data
            time.sleep(1)  # To avoid rate limits
        except Exception as e:
            print(f"❌ Failed for {ticker}: {e}")
    return all_data

# 3. Download and merge all data
data_dict = download_data(tickers)
df = pd.concat(data_dict.values())

# 4. Save to CSV
output_file = "us_stock_data_yfinance.csv"
df.to_csv(output_file)
print(f"\n✅ Saved {len(df)} rows to {output_file}")
