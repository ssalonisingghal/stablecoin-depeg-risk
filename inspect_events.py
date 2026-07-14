import pandas as pd

coins = ["usdc", "usdt", "dai"]

for name in coins:
    df = pd.read_csv(f"data/{name}_labeled.csv")
    df["date"] = pd.to_datetime(df["date"])

    events = df[df["event"] == 1]
    print(f"\n=== {name.upper()} — {len(events)} events (definition C) ===")
    print(events[["date", "deviation", "rolling_sigma", "threshold"]].to_string(index=False))

df = pd.read_csv("data/usdt_labeled.csv")
df["date"] = pd.to_datetime(df["date"])
mask = (df["date"] >= "2022-11-05") & (df["date"] <= "2022-11-20")
print(df[mask][["date", "deviation", "event"]].to_string(index=False))