import pandas as pd

price_files = {"usdc": "usd-coin", "usdt": "tether", "dai": "dai"}
coins = ["usdc", "usdt", "dai"]

for name in coins:
    prices = pd.read_csv(f"data/{price_files[name]}.csv")
    supply = pd.read_csv(f"data/{name}_supply.csv")

    prices["date"] = pd.to_datetime(prices["date"])
    supply["date"] = pd.to_datetime(supply["date"])

    prices["date"] = prices["date"].dt.normalize()
    supply["date"] = supply["date"].dt.normalize()

    merged = pd.merge(prices, supply, on="date", how="inner")

    print(f"{name}: {len(merged)} rows")
    print(merged.isna().sum())

    merged.to_csv(f"data/{name}_merged.csv", index=False)