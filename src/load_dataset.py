from ucimlrepo import fetch_ucirepo
import pandas as pd # type: ignore

dataset = fetch_ucirepo(id=144)

X = dataset.data.features
y = dataset.data.targets

data = pd.concat([X, y], axis=1)

data.to_csv("data/german_credit_data.csv", index=False)

print("Dataset saved successfully!")
print(data.head())