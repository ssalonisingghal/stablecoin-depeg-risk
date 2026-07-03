import requests
import pandas as pd
import matplotlib.pyplot as plt

# 1. Fetch the data
url = "https://api.coingecko.com/api/v3/coins/usd-coin/market_chart?vs_currency=usd&days=365&interval=daily"
response = requests.get(url)
data = response.json()

# 2. Build the dataframe
df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
df["date"] = pd.to_datetime(df["timestamp"], unit="ms")

# 3. Sanity check
print(df.head())

# 4. Deviation from peg
df["deviation"] = df["price"] - 1.0

# 5. Plot
plt.plot(df["date"], df["deviation"])
plt.title("USDC deviation from $1 peg (past year)")
plt.xlabel("Date")
plt.ylabel("Deviation ($)")
plt.axhline(0, color="gray", linestyle="--")  # reference line at perfect peg
plt.show()