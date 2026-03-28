import json
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util


class GitaEmotionRecommender:
    def __init__(self, json_path="gita_vedabase.json"):
        print("Loading verses...")
        with open(json_path, "r", encoding="utf-8") as f:
            self.verses = json.load(f)

        self.verse_lookup = {}
        for verse in self.verses:
            ref = verse.get("reference", "").strip()
            if ref:
                self.verse_lookup[ref] = verse

        print("Loading RoBERTa emotion model...")
        self.emotion_classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=1
        )

        print("Loading Sentence Transformer model...")
        self.sentence_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Keyword rules for emotions RoBERTa misses
        self.keyword_rules = {
            "guilt": [
                "guilt", "guilty", "regret", "regretted", "ashamed", "shame",
                "sorry", "apologize", "bad words", "said bad", "hurt someone",
                "self-blame", "mistake", "blunder", "wronged", "misbehaved",
                "rude to", "mean to", "bad to my", "behaved badly"
            ],
            "loneliness": [
                "lonely", "alone", "isolated", "abandoned", "no one",
                "nobody", "no friends", "left out", "excluded", "ignored",
                "invisible", "disconnected", "friendless"
            ],
            "confusion": [
                "confused", "confusion", "lost", "unclear", "unsure",
                "don't know what", "no idea", "mixed up", "indecisive",
                "can't decide", "what should i", "which path", "dilemma"
            ],
            "devotion": [
                "devotion", "devoted", "faith", "bhakti", "krishna",
                "god", "surrender", "prayer", "worship", "spiritual",
                "divine", "lord", "bless", "blessed"
            ],
            "grief": [
                "grief", "grieving", "grieve", "loss", "lost someone",
                "died", "death", "passed away", "mourning", "mourn",
                "miss them", "missing someone", "bereavement"
            ],
            "anxiety": [
                "anxious", "anxiety", "panic", "panicking", "stressed",
                "stress", "nervous", "worried", "worry", "overthinking",
                "overwhelmed", "can't sleep", "restless", "dread"
            ],
            "anger": [
                "angry", "anger", "furious", "rage", "hate", "frustrated",
                "frustration", "irritated", "annoyed", "mad at", "so mad",
                "enraged", "outraged", "livid"
            ],
            "sadness": [
                "sad", "sadness", "depressed", "depression", "hopeless",
                "cry", "crying", "tears", "broken", "heartbroken",
                "upset", "miserable", "unhappy", "down", "low"
            ],
            "motivation": [
                "motivation", "motivated", "inspire", "inspired", "hope",
                "hopeful", "strong", "determined", "goals", "achieve",
                "succeed", "push forward", "keep going", "never give up"
            ],
            "peace": [
                "peace", "peaceful", "calm", "serene", "stillness",
                "tranquil", "quiet mind", "at ease", "content", "harmony"
            ]
        }

        self.emotion_map = {
            "sadness": [
                {
                    "reference": "Bg. 2.14",
                    "custom_title": "Pain does not stay forever",
                    "simple_meaning": "Sadness and difficulty come and go. This painful moment will not remain forever."
                },
                {
                    "reference": "Bg. 2.11",
                    "custom_title": "Do not let sorrow consume you",
                    "simple_meaning": "Grief is natural, but wisdom teaches you not to drown in it. Try to see beyond the pain."
                },
                {
                    "reference": "Bg. 2.13",
                    "custom_title": "Life keeps moving forward",
                    "simple_meaning": "Change is part of life. Even when your heart hurts, life is still moving, and you can move with it."
                }
            ],
            "loneliness": [
                {
                    "reference": "Bg. 10.20",
                    "custom_title": "You are never alone",
                    "simple_meaning": "God lives in every heart. Even when you feel lonely, you are never truly alone."
                },
                {
                    "reference": "Bg. 6.5",
                    "custom_title": "You can become your own support",
                    "simple_meaning": "When no one else seems near, you can still lift yourself with strength and self-kindness."
                },
                {
                    "reference": "Bg. 9.22",
                    "custom_title": "God cares for those who turn to Him",
                    "simple_meaning": "When you sincerely remember God, you are protected, guided, and cared for."
                }
            ],
            "anxiety": [
                {
                    "reference": "Bg. 2.47",
                    "custom_title": "Focus on your effort, not the outcome",
                    "simple_meaning": "Do your best in the present moment. Anxiety becomes lighter when you stop carrying the whole future at once."
                },
                {
                    "reference": "Bg. 6.26",
                    "custom_title": "Bring the mind back gently",
                    "simple_meaning": "Whenever the mind runs toward worry, bring it back calmly and patiently."
                },
                {
                    "reference": "Bg. 6.35",
                    "custom_title": "The restless mind can be trained",
                    "simple_meaning": "Even if your mind feels unstable now, it can become calmer through practice and detachment."
                }
            ],
            "confusion": [
                {
                    "reference": "Bg. 2.7",
                    "custom_title": "It is okay to ask for guidance",
                    "simple_meaning": "Confusion is not weakness. The first step toward clarity is admitting that you need direction."
                },
                {
                    "reference": "Bg. 4.34",
                    "custom_title": "Seek wisdom when you feel lost",
                    "simple_meaning": "When you are confused, do not stay trapped in your thoughts alone. Seek truth, guidance, and understanding."
                },
                {
                    "reference": "Bg. 18.63",
                    "custom_title": "Reflect and choose wisely",
                    "simple_meaning": "After receiving guidance, think deeply and decide with awareness."
                }
            ],
            "guilt": [
                {
                    "reference": "Bg. 18.66",
                    "custom_title": "You are not beyond forgiveness",
                    "simple_meaning": "No mistake has to define your whole life. Sincere surrender and change can open the way forward."
                },
                {
                    "reference": "Bg. 9.30",
                    "custom_title": "A person can still change",
                    "simple_meaning": "Even if someone has acted wrongly, true devotion and right effort can transform them."
                },
                {
                    "reference": "Bg. 4.36",
                    "custom_title": "Wisdom can carry you across mistakes",
                    "simple_meaning": "Past errors do not make growth impossible. True understanding can help you rise beyond them."
                }
            ],
            "anger": [
                {
                    "reference": "Bg. 2.62",
                    "custom_title": "Anger begins with attachment",
                    "simple_meaning": "When we cling too strongly to what we want, frustration and anger begin to grow."
                },
                {
                    "reference": "Bg. 2.63",
                    "custom_title": "Anger clouds judgment",
                    "simple_meaning": "Unchecked anger confuses the mind and leads to poor decisions. Calmness protects clarity."
                },
                {
                    "reference": "Bg. 16.21",
                    "custom_title": "Let go before anger harms you",
                    "simple_meaning": "Anger can become destructive if it is fed again and again. Releasing it is a form of strength."
                }
            ],
            "peace": [
                {
                    "reference": "Bg. 2.70",
                    "custom_title": "Peace comes to the steady heart",
                    "simple_meaning": "Real peace comes when desires stop controlling the mind."
                },
                {
                    "reference": "Bg. 5.29",
                    "custom_title": "Peace grows through spiritual understanding",
                    "simple_meaning": "When you understand God as the ultimate well-wisher, the heart becomes quieter."
                },
                {
                    "reference": "Bg. 6.7",
                    "custom_title": "A calm mind stays balanced",
                    "simple_meaning": "Inner peace grows when the mind is disciplined and not shaken by outer situations."
                }
            ],
            "motivation": [
                {
                    "reference": "Bg. 3.30",
                    "custom_title": "Act with courage",
                    "simple_meaning": "Do what you must do with dedication and without fear. Right action builds strength."
                },
                {
                    "reference": "Bg. 6.5",
                    "custom_title": "Lift yourself up",
                    "simple_meaning": "Do not wait for life to change first. Start by strengthening your own mind and effort."
                },
                {
                    "reference": "Bg. 2.47",
                    "custom_title": "Keep working sincerely",
                    "simple_meaning": "Stay focused on your effort. Progress comes from action, not from worrying about immediate results."
                }
            ],
            "devotion": [
                {
                    "reference": "Bg. 9.22",
                    "custom_title": "God protects sincere devotion",
                    "simple_meaning": "When you remember God with sincerity, you are guided and cared for."
                },
                {
                    "reference": "Bg. 12.6",
                    "custom_title": "Offer your heart with devotion",
                    "simple_meaning": "Steady devotion creates strength, closeness, and spiritual security."
                },
                {
                    "reference": "Bg. 18.66",
                    "custom_title": "Surrender brings shelter",
                    "simple_meaning": "Turning wholeheartedly toward God brings relief, trust, and protection."
                }
            ],
            "grief": [
                {
                    "reference": "Bg. 2.20",
                    "custom_title": "The soul is never destroyed",
                    "simple_meaning": "What is deepest in us is eternal. Grief softens when seen through spiritual truth."
                },
                {
                    "reference": "Bg. 2.13",
                    "custom_title": "Life changes, but the soul continues",
                    "simple_meaning": "Bodies change, but the deeper self continues its journey."
                },
                {
                    "reference": "Bg. 2.27",
                    "custom_title": "Loss is part of mortal life",
                    "simple_meaning": "Birth and death are part of the material world. Understanding this can bring strength in grief."
                }
            ]
        }

        # Pre-compute embeddings
        print("Pre-computing verse embeddings...")
        self.all_verses_flat = []
        for emotion, verses in self.emotion_map.items():
            for v in verses:
                self.all_verses_flat.append({
                    "emotion": emotion,
                    "reference": v["reference"],
                    "custom_title": v["custom_title"],
                    "simple_meaning": v["simple_meaning"]
                })

        self.verse_embeddings = self.sentence_model.encode(
            [v["simple_meaning"] for v in self.all_verses_flat],
            convert_to_tensor=True
        )
        print("✅ All models loaded and ready!")

    def detect_emotion(self, user_text: str) -> str:
        text = user_text.lower()

        # Step 1: Keyword override (catches what RoBERTa misses)
        for emotion, keywords in self.keyword_rules.items():
            if any(kw in text for kw in keywords):
                print(f"Keyword match → {emotion}")
                return emotion

        # Step 2: RoBERTa fallback for everything else
        result = self.emotion_classifier(user_text)
        detected = result[0][0]["label"].lower()
        print(f"RoBERTa detected → {detected}")

        # Map RoBERTa labels to our emotions
        label_map = {
            "sadness": "sadness",
            "fear": "anxiety",
            "anger": "anger",
            "joy": "peace",
            "disgust": "guilt",
            "surprise": "confusion",
            "neutral": "motivation"
        }
        return label_map.get(detected, "sadness")

    def recommend_verses(self, user_text: str, top_k: int = 3):
        emotion = self.detect_emotion(user_text)

        user_embedding = self.sentence_model.encode(user_text, convert_to_tensor=True)

        emotion_verses = [v for v in self.all_verses_flat if v["emotion"] == emotion]
        emotion_indices = [i for i, v in enumerate(self.all_verses_flat) if v["emotion"] == emotion]

        if not emotion_verses:
            emotion_verses = self.all_verses_flat
            emotion_indices = list(range(len(self.all_verses_flat)))

        filtered_embeddings = self.verse_embeddings[emotion_indices]
        scores = util.cos_sim(user_embedding, filtered_embeddings)[0]
        top_indices = scores.argsort(descending=True)[:top_k]

        results = []
        for idx in top_indices:
            item = emotion_verses[idx]
            ref = item["reference"]
            verse_data = self.verse_lookup.get(ref)

            if not verse_data:
                continue

            results.append({
                "emotion": emotion,
                "reference": ref,
                "title": item["custom_title"],
                "devanagari": verse_data.get("devanagari", ""),
                "translation": verse_data.get("translation", ""),
                "simplified_meaning": item["simple_meaning"],
                "source": verse_data.get("source", ""),
                "similarity_score": float(scores[idx])
            })

        return results