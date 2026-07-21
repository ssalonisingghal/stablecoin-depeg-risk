import pandas as pd

coins = ["usdc", "usdt", "dai"]
price_files = {"usdc": "usd-coin", "usdt": "tether", "dai": "dai"}

LABEL_HORIZON = 5   # predict an event in the next 5 days

for name in coins:
    # --- load price (labeled) + supply, merge ---
    labeled = pd.read_csv(f"data/{name}_labeled.csv")
    labeled["date"] = pd.to_datetime(labeled["date"])
    supply = pd.read_csv(f"data/{name}_supply.csv")
    supply["date"] = pd.to_datetime(supply["date"]).dt.normalize()
    df = pd.merge(labeled, supply, on="date", how="inner").sort_values("date").reset_index(drop=True)

    # ============ FEATURES (all use PAST data only) ============
    # deviation side
    df["f_deviation"] = df["deviation"]
    df["f_dev_3d_min"] = df["deviation"].rolling(3).min()        # worst dip in last 3d
    # rolling_sigma already exists from labeler, computed with shift(1) — reuse it
    df["f_rolling_sigma"] = df["rolling_sigma"]
    df["f_zscore"] = df["deviation"] / df["rolling_sigma"]       # abnormality in coin's own terms

    # flow side
    df["supply_pct"] = df["supply"].pct_change() * 100
    df["f_flow"] = df["supply_pct"]                               # signed daily flow
    df["f_flow_abs"] = df["supply_pct"].abs()                     # CHURN catcher
    df["f_flow_3d"] = df["supply_pct"].rolling(3).sum()           # accelerating outflow (3d)
    df["f_flow_7d"] = df["supply_pct"].rolling(7).sum()           # accelerating outflow (7d)
    df["f_flow_vol_7d"] = df["supply_pct"].rolling(7).std()       # flow instability / churn (7d)

    # ============ LABEL (strictly FUTURE — no leakage) ============
    # 1 if an event occurs on ANY of the next LABEL_HORIZON days
    future_event = df["event"].shift(-1).rolling(LABEL_HORIZON).max()
    df["label"] = future_event.fillna(0).astype(int)

    # drop early rows where rolling features are NaN
    feature_cols = [c for c in df.columns if c.startswith("f_")]
    df_clean = df.dropna(subset=feature_cols).reset_index(drop=True)

    df_clean.to_csv(f"data/{name}_features.csv", index=False)
    print(f"{name}: {len(df_clean)} rows, {df_clean['label'].sum()} positive labels")