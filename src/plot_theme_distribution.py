from theme_detection import detect_themes
import pandas as pd
import matplotlib.pyplot as plt

df, cluster_keywords = detect_themes("data/Bhagwad_Gita.csv", num_clusters=5)

chapter_theme_counts = pd.crosstab(df["Chapter"], df["theme_cluster"])

chapter_theme_counts.plot(kind="bar", figsize=(12, 6))
plt.title("Chapter-wise Theme Distribution")
plt.xlabel("Chapter")
plt.ylabel("Number of Verses")
plt.tight_layout()
plt.show()