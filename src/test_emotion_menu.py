from emotion_recommender import GitaEmotionRecommender
from emotion_options import emotion_map

recommender = GitaEmotionRecommender("data/Bhagwad_Gita.csv")

print("Available emotions:")
for key in emotion_map:
    print("-", key)

choice = input("\nChoose an emotion: ").strip().lower()

if choice in emotion_map:
    query = emotion_map[choice]
    results = recommender.recommend_verses(query, top_k=5)

    for i, r in enumerate(results, 1):
        print(f"\nRecommendation {i}")
        print(f"Chapter: {r['Chapter']}, Verse: {r['Verse']}")
        print(f"Meaning: {r['Meaning']}")
        print(f"Score: {r['Score']:.4f}")
else:
    print("Invalid choice")