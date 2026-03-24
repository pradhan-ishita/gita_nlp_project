from theme_detection import detect_themes
import pandas as pd

df, cluster_keywords = detect_themes("data/Bhagwad_Gita.csv", num_clusters=5)

chapter_theme_counts = pd.crosstab(df["Chapter"], df["theme_cluster"])

print("Chapter-wise Theme Distribution:\n")
print(chapter_theme_counts)

chapter_theme_counts.to_csv("outputs/chapter_theme_counts.csv")

print("\nSaved as outputs/chapter_theme_counts.csv")