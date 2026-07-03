import pandas as pd
import matplotlib.pyplot as plt

coins = ["usd-coin", "tether", "dai"]


for coin in coins:
    df = pd.read_csv(f"data/{coin}.csv")
    df["date"] = pd.to_datetime(df["date"])
    plt.plot(df["date"], df["deviation"], label=coin)

plt.legend()
plt.axhline(0, color="gray", linestyle="--")
plt.title("Stablecoin deviation from $1 peg (past year)")
plt.xlabel("Date")
plt.ylabel("Deviation ($)")
plt.show()
