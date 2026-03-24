import faiss
import numpy as np

class VerseFAISSIndex:
    def __init__(self, embeddings):
        self.embeddings = np.array(embeddings).astype("float32")

        # normalize for cosine-like search via inner product
        faiss.normalize_L2(self.embeddings)

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.embeddings)

    def search(self, query_embedding, top_k=5):
        query = np.array([query_embedding]).astype("float32")
        faiss.normalize_L2(query)
        scores, indices = self.index.search(query, top_k)
        return scores[0], indices[0]