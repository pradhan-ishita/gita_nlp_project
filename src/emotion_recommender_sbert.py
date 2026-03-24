from sentence_transformers import SentenceTransformer
from src.vector_store import VerseFAISSIndex

class GitaSBERTRecommender:
    def __init__(self, csv_path):
        self.df = load_and_clean_data(csv_path)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.verse_embeddings = self.model.encode(
            self.df["EngMeaning"].tolist(),
            convert_to_numpy=True
        )
        self.index = VerseFAISSIndex(self.verse_embeddings)

    def recommend_verses(self, user_input, top_k=5):
        emotion_result = detect_emotion(user_input)
        detected_emotion = emotion_result["mapped_label"]

        expanded_query = self.expand_emotion_query(user_input, detected_emotion)
        query_embedding = self.model.encode(expanded_query, convert_to_numpy=True)

        scores, indices = self.index.search(query_embedding, top_k=top_k)

        results = []
        for score, idx in zip(scores, indices):
            row = self.df.iloc[int(idx)]
            results.append({
                "ID": row["ID"],
                "Chapter": row["Chapter"],
                "Verse": row["Verse"],
                "Shloka": row["Shloka"],
                "Meaning": row["EngMeaning"],
                "Score": float(score),
                "DetectedEmotion": detected_emotion,
                "ExpandedQuery": expanded_query
            })
        return results