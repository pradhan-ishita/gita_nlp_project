from src.emotion_options import CUSTOM_TO_THEME


def detect_custom_emotion(text, base_emotion=None):
    t = str(text).lower().strip()

    emotion_keywords = {
        "trust": [
            "trust", "believe in", "have faith", "rely on", "depend on",
            "confidence in", "i trust", "i believe in"
        ],
        "surprise": [
            "surprised", "unexpected", "shocked", "suddenly",
            "didn't expect", "what just happened"
        ],
        "disgust": [
            "disgust", "gross", "dirty", "revolting", "nasty", "sickened"
        ],
        "anticipation": [
            "looking forward", "anticipating", "waiting eagerly",
            "can't wait", "expecting", "upcoming"
        ],
        "love": [
            "love", "deeply care", "affection", "adore", "cherish"
        ],
        "jealousy": [
            "jealous", "envy", "why not me", "they have more",
            "comparing myself", "resent their success"
        ],
        "shame": [
            "ashamed", "shame", "i am bad", "i feel dirty", "i feel small"
        ],
        "embarrassment": [
            "embarrassed", "humiliated", "awkward", "laughed at",
            "felt stupid", "made a fool of myself"
        ],
        "pride": [
            "proud", "accomplished", "achievement", "i did it",
            "i am proud of myself"
        ],
        "gratitude": [
            "grateful", "thankful", "blessed", "appreciate",
            "thank god", "fortunate"
        ],
        "hope": [
            "hope", "hopeful", "things will get better",
            "maybe it will work", "i still believe"
        ],
        "amazement": [
            "amazed", "astonished", "incredible", "unbelievable", "wonder"
        ],
        "admiration": [
            "admire", "respect deeply", "look up to", "inspired by"
        ],
        "rage": [
            "rage", "furious", "enraged", "boiling with anger", "livid"
        ],
        "loathing": [
            "loathe", "despise", "can't stand", "hate deeply"
        ],
        "acceptance": [
            "accept", "coming to terms", "let it be", "i understand now", "it is okay"
        ],
        "terror": [
            "terrified", "horrified", "panic", "extreme fear",
            "paralyzed with fear"
        ],
        "aggressiveness": [
            "attack", "aggressive", "fight them", "hurt them",
            "dominate", "destroy them"
        ],
        "distraction": [
            "distracted", "can't focus", "mind wandering",
            "not concentrating", "losing focus"
        ],
        "boredom": [
            "bored", "nothing interests me", "dull", "uninterested",
            "fed up", "nothing to do"
        ],
        "remorse": [
            "remorse", "deep regret", "i feel terrible for what i did",
            "i deeply regret", "i am sorry"
        ],
        "disapproval": [
            "disapprove", "this feels wrong", "i don't approve",
            "against it", "i dislike this decision"
        ]
    }

    for emotion, keywords in emotion_keywords.items():
        if any(k in t for k in keywords):
            return emotion

    if base_emotion:
        broad_map = {
            "joy": "gratitude",
            "love": "love",
            "anger": "rage",
            "fear": "terror",
            "surprise": "amazement",
            "sadness": "remorse",
            "disgust": "disgust"
        }
        return broad_map.get(str(base_emotion).lower(), "acceptance")

    return "acceptance"


def map_custom_to_theme(custom_emotion):
    return CUSTOM_TO_THEME.get(custom_emotion, "Peace / Acceptance")