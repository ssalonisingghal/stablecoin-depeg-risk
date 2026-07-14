import pandas as pd
import matplotlib.pyplot as plt

coins = ["usdc", "usdt", "dai"]
WINDOW = 10  # days before/after each episode start

for name in coins:
    labeled = pd.read_csv(f"data/{name}_labeled.csv")
    labeled["date"] = pd.to_datetime(labeled["date"])

    supply = pd.read_csv(f"data/{name}_supply.csv")
    supply["date"] = pd.to_datetime(supply["date"]).dt.normalize()

    df = pd.merge(labeled, supply, on="date", how="inner")
    df["supply_pct_change"] = df["supply"].pct_change() * 100

    episodes = df[df["episode_id"] > 0].groupby("episode_id")["date"].min()

    for ep_id, ep_date in episodes.items():
        mask = (df["date"] >= ep_date - pd.Timedelta(days=WINDOW)) & \
               (df["date"] <= ep_date + pd.Timedelta(days=WINDOW))
        window = df[mask]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        ax1.plot(window["date"], window["deviation"], color="tab:blue")
        ax1.axvline(ep_date, color="red", linestyle="--")
        ax1.set_ylabel("Deviation ($)")
        ax1.set_title(f"{name.upper()} episode {ep_id} — {ep_date.date()}")

        ax2.bar(window["date"], window["supply_pct_change"], color="tab:orange")
        ax2.axvline(ep_date, color="red", linestyle="--")
        ax2.set_ylabel("Supply chg (%)")

        plt.tight_layout()
        plt.savefig(f"charts/{name}_episode_{ep_id}.png")
        plt.close()
        print(f"Saved {name} episode {ep_id} ({ep_date.date()})")