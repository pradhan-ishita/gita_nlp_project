def detect_emotion(text):
    text = text.lower()

    emotion_keywords = {
        "Anxiety / Fear": [
            "anxious","worried","fear","afraid","panic","nervous","stress","scared","future"
        ],

        "Sadness / Depression": [
            "sad","unhappy","depressed","cry","crying","lonely","hopeless","worse","miserable","down"
        ],

        "Guilt / Regret / Self-Blame": [
            "guilt","guilty","regret","ashamed","sorry","blame","dishonored","failed","disappointed"
        ],

        "Confusion / Doubt": [
            "confused","doubt","lost","uncertain","don't know","unsure"
        ],

        "Anger / Frustration": [
            "angry","anger","frustrated","hate","annoyed","rage"
        ],

        "Seeking Peace / Calm": [
            "peace","calm","relax","quiet","mindful","inner peace"
        ],

        "Motivation / Strength": [
            "motivation","strength","encourage","hope","determined","improve","try again"
        ]
    }

    for emotion, keywords in emotion_keywords.items():
        for word in keywords:
            if word in text:
                return emotion

    return "General"