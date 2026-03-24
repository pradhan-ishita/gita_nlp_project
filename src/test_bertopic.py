from src.theme_detection_bertopic import detect_topics_bertopic

df, topic_info, topic_model = detect_topics_bertopic("data/Bhagwad_Gita.csv")

print(topic_info.head(10))
print(df[["ID", "Chapter", "Verse", "topic"]].head(10))