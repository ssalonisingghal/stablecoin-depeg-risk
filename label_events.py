import pandas as pd

WINDOW = 30      # days used to measure "normal wobble"
SIGMA_MULT = 5   # how many typical wobbles = an event
SIGMA_FLOOR = 0.0005  # never let "normal" be measured as < 5bps (frog-boil guard, part 1)

coins = ["usdc", "usdt", "dai"]
price_files = {"usdc": "usd-coin", "usdt": "tether", "dai": "dai"}

for name in coins:
    df = pd.read_csv(f"data/{price_files[name]}_history.csv")
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    df = df.sort_values("date").reset_index(drop=True)

    # rolling "typical wobble", using ONLY past days (shift(1) = exclude today)
    df["rolling_sigma"] = (
        df["deviation"].shift(1).rolling(WINDOW).std()
    )
    df["rolling_sigma"] = df["rolling_sigma"].clip(lower=SIGMA_FLOOR)

    # threshold and flag: event = today's deviation worse than -5 sigma
    df["threshold"] = -SIGMA_MULT * df["rolling_sigma"]
    df["event"] = (df["deviation"] < df["threshold"]).astype(int)

    # robustness definition A: fixed -50bps
    df["event_fixed"] = (df["deviation"] < -0.005).astype(int)

    df["episode_id"] = (
        (df["event"] == 1) & (df["event"].shift(1, fill_value=0) == 0)
    ).cumsum() * df["event"]
    
    df.to_csv(f"data/{name}_labeled.csv", index=False)
    print(f"{name}: {df['event'].sum()} events (C), {df['event_fixed'].sum()} events (A)")