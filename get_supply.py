
import requests
import pandas as pd
import matplotlib.pyplot as plt

endpoint = "https://stablecoins.llama.fi/stablecoin/2"
response = requests.get(endpoint)
data = response.json()
print(data.keys())
print(type(data["tokens"]))
print(data["tokens"][0])

rows = [
    {"date": t["date"], "supply": t["circulating"]["peggedUSD"]}
    for t in data["tokens"]
]
df = pd.DataFrame(rows)
df["date"] = pd.to_datetime(df["date"], unit="s")
df["supply_change"] = df["supply"].diff()

df.to_csv(f"data/usdc_supply.csv", index=False)

mask = (df["date"] >= "2023-02-01") & (df["date"] <= "2023-04-30")
crisis = df[mask]

plt.plot(crisis["date"], crisis["supply"])
plt.title("USDC circulating supply — SVB crisis, spring 2023")
plt.xlabel("Date")
plt.ylabel("Supply ($)")
plt.show()

