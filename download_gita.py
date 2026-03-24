import requests
import pandas as pd
import json
import time

print("Downloading Bhagavad Gita data from GitHub API...")

# Total verses per chapter
verses_per_chapter = [47,72,43,42,29,47,30,28,34,42,55,20,35,27,20,24,28,78]

all_verses = []

for chapter_num, total_verses in enumerate(verses_per_chapter, start=1):
    print(f"Downloading Chapter {chapter_num} ({total_verses} verses)...")
    
    for verse_num in range(1, total_verses + 1):
        url = f"https://vedicscriptures.github.io/slok/{chapter_num}/{verse_num}/"
        
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json()
                
                verse = {
                    "Chapter": chapter_num,
                    "Verse": verse_num,
                    "Shloka": data.get("slok", ""),
                    "Transliteration": data.get("transliteration", ""),
                    "EngMeaning": data.get("tej", {}).get("ht", "") or data.get("siva", {}).get("et", "") or data.get("purohit", {}).get("et", ""),
                    "Purport": data.get("gambir", {}).get("et", "") or data.get("san", {}).get("et", ""),
                    "HinMeaning": data.get("tej", {}).get("ht", ""),
                }
                all_verses.append(verse)
            else:
                print(f"  Failed: Chapter {chapter_num} Verse {verse_num} - Status {r.status_code}")
        
        except Exception as e:
            print(f"  Error: Chapter {chapter_num} Verse {verse_num} - {e}")
        
        time.sleep(0.1)  # be polite to the API

print(f"\nTotal verses downloaded: {len(all_verses)}")

df = pd.DataFrame(all_verses)
df["ID"] = [f"BG{row.Chapter}.{row.Verse}" for _, row in df.iterrows()]
df = df[["ID", "Chapter", "Verse", "Shloka", "Transliteration", "EngMeaning", "HinMeaning", "Purport"]]

df.to_csv("data/gita_full.csv", index=False)
print("Saved to data/gita_full.csv")
print("Columns:", df.columns.tolist())
print("\nSample:")
print(df.head(2).to_string())