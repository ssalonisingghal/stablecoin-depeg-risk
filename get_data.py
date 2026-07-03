import time

import requests
import pandas as pd
import matplotlib.pyplot as plt

# 1. Fetch the data
def get_prices(coin_id, days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}&interval=daily"
    response = requests.get(url)
    data = response.json()

    #build the dataframe from data["prices"]
    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")

    #deviation colum
    df["deviation"] = df["price"] - 1.0
    return df

coins = ["usd-coin", "tether", "dai"]

for coin in coins:
    df = get_prices(coin)
    df.to_csv(f"data/{coin}.csv", index=False)
    print(f"Saved {coin}: {len(df)} rows")
    time.sleep(2)
