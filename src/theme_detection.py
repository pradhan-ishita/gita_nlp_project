from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from src.data_preprocessing import load_and_clean_data

def detect_themes(csv_path, num_clusters=5):
    df = load_and_clean_data(csv_path)

    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(df["clean_text"])

    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    df["theme_cluster"] = kmeans.fit_predict(X)

    terms = vectorizer.get_feature_names_out()
    cluster_keywords = {}

    for i in range(num_clusters):
        top_indices = kmeans.cluster_centers_[i].argsort()[-10:][::-1]
        cluster_keywords[i] = [terms[idx] for idx in top_indices]

    return df, cluster_keywords