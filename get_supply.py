import requests
import pandas as pd
import time

def get_supply(coin_id, name):
    endpoint = f"https://stablecoins.llama.fi/stablecoin/{coin_id}"
    response = requests.get(endpoint)
    data = response.json()

    rows = [
        {"date": t["date"], "supply": t["circulating"]["peggedUSD"]}
        for t in data["tokens"]
    ]
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], unit="s")
    df["supply_change"] = df["supply"].diff()

    df.to_csv(f"data/{name}_supply.csv", index=False)
    return df

pairs = [(2, "usdc"), (1, "usdt"), (5, "dai")]

for coin_id, name in pairs:
    df = get_supply(coin_id, name)
    print(f"Saved {name}: {len(df)} rows")
    time.sleep(2)

