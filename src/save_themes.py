from theme_detection import detect_themes

df, cluster_keywords = detect_themes("data/Bhagwad_Gita.csv", num_clusters=5)

df.to_csv("outputs/theme_detection_results.csv", index=False)

print("Theme detection results saved in outputs/theme_detection_results.csv")
print("\nCluster Keywords:")
for cluster, words in cluster_keywords.items():
    print(f"Cluster {cluster}: {', '.join(words)}")