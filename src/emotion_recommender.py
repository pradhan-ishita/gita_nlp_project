from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.data_preprocessing import load_and_clean_data
from src.emotion_detector_bert import detect_emotion


class GitaEmotionRecommender:
    def __init__(self, csv_path):
        self.df = load_and_clean_data(csv_path)
        self.vectorizer = TfidfVectorizer()
        self.verse_vectors = self.vectorizer.fit_transform(self.df["clean_text"])

    def expand_emotion_query(self, user_input: str, detected_emotion: str) -> str:
        text = user_input.lower().strip()

        if detected_emotion == "Sadness / Depression":
            return (
                "I feel sad, emotionally weak, lonely, hopeless, and worse. "
                "I need healing, peace, faith, and inner strength."
            )

        elif detected_emotion == "Anxiety / Fear":
            return (
                "I feel anxious, afraid, restless, and worried about the future. "
                "I need peace, calmness, courage, and stability."
            )

        elif detected_emotion == "Anger / Frustration":
            return (
                "I feel angry, frustrated, and unable to control my emotions. "
                "I need patience, calmness, self-control, and wisdom."
            )

        elif detected_emotion == "Confusion / Doubt":
            return (
                "I feel confused, doubtful, and uncertain about what is right. "
                "I need clarity, wisdom, guidance, and right understanding."
            )

        elif detected_emotion == "Motivation / Hope":
            return (
                "I need hope, encouragement, motivation, and inner strength "
                "to continue doing my duty."
            )

        elif detected_emotion == "Guilt / Regret / Self-Blame":
            return (
                "I feel guilty, ashamed, regretful, and deeply sorry for disappointing "
                "people who trusted me. I feel self-blame and remorse. "
                "I need forgiveness, inner strength, wisdom, self-control, and guidance "
                "to act rightly and restore my character."
            )

        self_doubt_phrases = [
            "not good to society",
            "not good enough",
            "i am useless",
            "i am worthless",
            "i hate myself",
            "i am a burden",
            "i am not good",
            "i am not worthy",
            "i failed as a person",
            "i am nothing",
            "i am a bad person",
            "nobody needs me",
            "i am not good to the society",
            "i am not good for society"
        ]
        if any(p in text for p in self_doubt_phrases):
            return (
                "I feel worthless, ashamed, and full of self doubt. "
                "I feel that I am not good enough and I may have disappointed others. "
                "I need wisdom, self-understanding, forgiveness, hope, and inner strength "
                "to realize my true self and regain purpose."
            )

        guilt_phrases = [
            "failed my parents",
            "failed my family",
            "failed them",
            "let them down",
            "let my parents down",
            "disappointed my parents",
            "disappointed them",
            "people trusted me",
            "broke their trust",
            "broke trust",
            "dishonored them",
            "dishonoured them",
            "dishonored my parents",
            "dishonoured my parents",
            "hurt them",
            "hurt my parents",
            "betrayed them",
            "betrayed trust",
            "ashamed of myself",
            "hate myself",
            "self blame",
            "self-blame"
        ]

        guilt_words = [
            "guilt", "guilty", "regret", "regretful", "ashamed", "shame",
            "dishonor", "dishonour", "dishonored", "dishonoured",
            "betrayed", "sorry", "remorse", "remorseful",
            "wronged", "trust", "trusted", "blame"
        ]

        if any(phrase in text for phrase in guilt_phrases) or any(word in text for word in guilt_words):
            return (
                "I feel guilty, ashamed, regretful, and deeply sorry for disappointing "
                "people who trusted me. I feel self-blame and remorse. "
                "I need forgiveness, inner strength, wisdom, self-control, and guidance "
                "to act rightly and restore my character."
            )

        failure_phrases = [
            "exam", "marks", "result", "failed", "failure",
            "did not do well", "bad score", "low score", "test"
        ]
        if any(phrase in text for phrase in failure_phrases):
            return (
                "I feel disappointed, anxious, discouraged, and worried about failure. "
                "I need strength, peace, motivation, and guidance to keep doing my duty."
            )

        anxiety_words = [
            "anxious", "anxiety", "worried", "stress", "stressed",
            "overthinking", "pressure", "tense", "restless"
        ]
        if any(word in text for word in anxiety_words):
            return (
                "I feel anxious, restless, and worried about the future. "
                "I need peace, calmness, strength, and detachment from results."
            )

        anger_words = [
            "angry", "anger", "furious", "rage", "upset", "frustrated"
        ]
        if any(word in text for word in anger_words):
            return (
                "I feel angry and unable to control my emotions. "
                "I need calmness, self-control, patience, and wisdom."
            )

        sadness_words = [
            "sad", "depressed", "hurt", "crying", "hopeless",
            "lonely", "broken", "empty", "worse", "down", "miserable"
        ]
        if any(word in text for word in sadness_words):
            return (
                "I feel sad, emotionally weak, lonely, hopeless, and worse. "
                "I need inner strength, healing, peace, and faith."
            )

        confusion_words = [
            "confused", "lost", "uncertain", "doubt", "dilemma", "unsure"
        ]
        if any(word in text for word in confusion_words):
            return (
                "I feel confused and do not know what is right. "
                "I need clarity, wisdom, guidance, and right understanding."
            )

        fear_words = [
            "fear", "afraid", "scared", "nervous", "panic", "frightened"
        ]
        if any(word in text for word in fear_words):
            return (
                "I feel fear, nervousness, and lack of courage. "
                "I need bravery, stability, confidence, and faith."
            )

        motivation_words = [
            "motivation", "lazy", "tired", "demotivated", "exhausted",
            "can't continue", "give up"
        ]
        if any(word in text for word in motivation_words):
            return (
                "I feel tired, demotivated, and weak. "
                "I need strength, discipline, purpose, and motivation to act."
            )

        peace_words = [
            "peace", "calm", "calmness", "relaxed", "quiet", "stillness", "serenity"
        ]
        if any(word in text for word in peace_words):
            return (
                "I want peace, serenity, calmness, inner stability, freedom from stress, "
                "and purity of mind."
            )

        devotion_words = [
            "devotion", "god", "krishna", "spiritual", "faith", "bhakti", "prayer"
        ]
        if any(word in text for word in devotion_words):
            return (
                "I seek devotion, surrender, faith, spiritual wisdom, and closeness to God."
            )

        return user_input

    def recommend_verses(self, user_input: str, top_k: int = 5):
        emotion_result = detect_emotion(user_input)
        detected_emotion = emotion_result["mapped_label"]

        expanded_query = self.expand_emotion_query(user_input, detected_emotion)

        input_vector = self.vectorizer.transform([expanded_query.lower()])
        similarities = cosine_similarity(input_vector, self.verse_vectors).flatten()
        top_indices = similarities.argsort()[::-1][:top_k]

        recommendations = []
        for idx in top_indices:
            row = self.df.iloc[idx]
            recommendations.append({
                "ID": row["ID"],
                "Chapter": row["Chapter"],
                "Verse": row["Verse"],
                "Shloka": row["Shloka"] if "Shloka" in self.df.columns else "",
                "Meaning": row["EngMeaning"],
                "Score": float(similarities[idx]),
                "DetectedEmotion": detected_emotion,
                "ExpandedQuery": expanded_query,
                "EmotionScore": float(emotion_result["score"]),
                "RawEmotion": emotion_result["raw_label"]
            })

        return recommendations


if __name__ == "__main__":
    recommender = GitaEmotionRecommender("data/Bhagwad_Gita.csv")

    user_text = input("Describe how you are feeling: ")
    results = recommender.recommend_verses(user_text, top_k=5)

    if results:
        print("\nDetected Emotion:", results[0]["DetectedEmotion"])
        print("Raw Emotion Label:", results[0]["RawEmotion"])
        print("Emotion Confidence:", f"{results[0]['EmotionScore']:.4f}")
        print("Expanded Emotional Query:", results[0]["ExpandedQuery"])

    for i, r in enumerate(results, 1):
        print(f"\nRecommendation {i}")
        print(f"ID: {r['ID']}")
        print(f"Chapter: {r['Chapter']}, Verse: {r['Verse']}")
        print(f"Similarity Score: {r['Score']:.4f}")

        if r["Shloka"]:
            print("\nSanskrit Shloka:")
            print(r["Shloka"])

        print("\nEnglish Meaning:")
        print(r["Meaning"])