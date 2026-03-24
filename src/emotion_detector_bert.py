from transformers import pipeline
from src.emotion_mapper import detect_custom_emotion, map_custom_to_theme

MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

_classifier = pipeline(
    "text-classification",
    model=MODEL_NAME,
    top_k=None
)


def map_base_label(raw_label):
    label = str(raw_label).lower()

    base_map = {
        "joy": "Happiness / Joy",
        "sadness": "Sadness / Depression",
        "anger": "Anger / Frustration",
        "fear": "Anxiety / Fear",
        "surprise": "Confusion / Doubt",
        "love": "Devotion / Faith",
        "disgust": "Disgust / Loathing",
        "neutral": "Peace / Acceptance"
    }

    return base_map.get(label, "Peace / Acceptance")


def detect_emotion(text):
    text = str(text).strip()
    if not text:
        return {
            "raw_label": "neutral",
            "mapped_label": "Peace / Acceptance",
            "score": 0.0,
            "custom_emotion": "acceptance",
            "theme_label": "Peace / Acceptance"
        }

    preds = _classifier(text)[0]
    preds = sorted(preds, key=lambda x: x["score"], reverse=True)

    best = preds[0]
    raw_label = best["label"]
    score = float(best["score"])

    mapped_label = map_base_label(raw_label)
    custom_emotion = detect_custom_emotion(text, base_emotion=raw_label)
    theme_label = map_custom_to_theme(custom_emotion)

    return {
        "raw_label": raw_label,
        "mapped_label": mapped_label,
        "score": score,
        "custom_emotion": custom_emotion,
        "theme_label": theme_label,
        "all_predictions": preds
    }