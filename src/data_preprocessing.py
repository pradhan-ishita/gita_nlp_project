import pandas as pd


def load_and_clean_data(csv_path):
    df = pd.read_csv(csv_path)

    required_columns = [
        "ID", "Chapter", "Verse", "Shloka",
        "Transliteration", "EngMeaning", "HinMeaning"
    ]

    for col in required_columns:
        if col not in df.columns:
            df[col] = ""

    if "WordMeaning" not in df.columns:
        df["WordMeaning"] = ""

    df["clean_text"] = df["EngMeaning"].fillna("").astype(str).str.lower()

    return df