from src.emotion_detector_bert import detect_emotion

tests = [
    "i feel worse",
    "i disappointed my parents",
    "i want peace",
    "i am scared of the future",
    "i feel useless"
]

for t in tests:
    result = detect_emotion(t)
    print("\nInput:", t)
    print("Raw:", result["raw_label"])
    print("Mapped:", result["mapped_label"])
    print("Score:", round(result["score"], 4))