import pandas as pd

# load dataset
df = pd.read_csv("data/Bhagwad_Gita.csv")

print("Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nFirst 5 rows:")
print(df.head())

print("\nSample English meanings:")
print(df["EngMeaning"].head(10))