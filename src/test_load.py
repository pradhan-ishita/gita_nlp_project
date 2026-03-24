import pandas as pd

df = pd.read_csv("data/Bhagwad_Gita.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())