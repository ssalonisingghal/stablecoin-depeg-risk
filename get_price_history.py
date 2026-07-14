import requests
import pandas as pd
import time
from datetime import datetime, timezone

def get_price_history(gecko_id, start_date="2021-01-01"):
    """Fetch daily price history from DeFiLlama's coins API, in chunks."""
    start_ts = int(datetime.strptime(start_date, "%Y-%m-%d")
                   .replace(tzinfo=timezone.utc).timestamp())
    now_ts = int(datetime.now(timezone.utc).timestamp())

    all_prices = []
    chunk_days = 500  # DeFiLamma max per request, staying under API limits
    ts = start_ts

    while ts < now_ts:
        url = (f"https://coins.llama.fi/chart/coingecko:{gecko_id}"
               f"?start={ts}&span={chunk_days}&period=1d")
        response = requests.get(url)
        data = response.json()

        try:
            prices = data["coins"][f"coingecko:{gecko_id}"]["prices"]
        except KeyError:
            print(f"Unexpected response for {gecko_id}: {data}")
            break

        all_prices.extend(prices)
        ts += chunk_days * 86400  # jump forward chunk_days worth of seconds
        time.sleep(1)

    df = pd.DataFrame(all_prices)
    df["date"] = pd.to_datetime(df["timestamp"], unit="s")
    df["date"] = df["date"].dt.normalize()
    df["abs_dev"] = (df["price"] - 1.0).abs()
    df = df.sort_values("abs_dev").drop_duplicates(subset="date", keep="last")
    df = df.drop(columns="abs_dev").sort_values("date").reset_index(drop=True)
    df["deviation"] = df["price"] - 1.0
    return df

coins = ["usd-coin", "tether", "dai"]

for coin in coins:
    df = get_price_history(coin)
    df.to_csv(f"data/{coin}_history.csv", index=False)
    print(f"Saved {coin}: {len(df)} rows, from {df['date'].min()} to {df['date'].max()}")
    time.sleep(2)