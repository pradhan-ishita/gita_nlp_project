from data_preprocessing import load_and_clean_data

# load and clean dataset
df = load_and_clean_data("data/Bhagwad_Gita.csv")

# save cleaned dataset
df.to_csv("data/cleaned_gita.csv", index=False)

print("Cleaned data saved successfully!")
print(df.head())