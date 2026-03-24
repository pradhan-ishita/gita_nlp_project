from bertopic import BERTopic
from src.data_preprocessing import load_and_clean_data

def detect_topics_bertopic(csv_path):
    df = load_and_clean_data(csv_path)

    docs = df["EngMeaning"].tolist()

    topic_model = BERTopic(language="english")
    topics, probs = topic_model.fit_transform(docs)

    df["topic"] = topics

    topic_info = topic_model.get_topic_info()
    return df, topic_info, topic_model