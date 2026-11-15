import os
import re
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from nltk import download
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

warnings.filterwarnings("ignore")

download("punkt", quiet=True)
download("stopwords", quiet=True)

DATA_PATH = os.path.join(os.path.dirname(__file__), "feedback.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "word2vec_model.model")
PLOT_PATH = os.path.join(os.path.dirname(__file__), "semantic_clusters.png")

REVIEWS = [
    "The product is very easy to use and the design looks modern.",
    "The product is good and the quality is great.",
    "This is a good product with a nice design and perfect finish.",
    "The product feels great, reliable, and easy to recommend.",
    "The price is reasonable and the value is worth it.",
    "The price is fair, the cost is good, and the product feels valuable.",
    "The product is nice and the price matches the quality.",
    "The price is low and the product is perfect for everyday use.",
    "This product is good and the price feels worth it.",
    "The product is great and the quality is excellent.",
    "The price is good and the service is nice.",
    "The value is great, and the product is perfect for my needs.",
    "The cost is high but the product is still worth the value.",
    "I love the product because it is good, nice, and great.",
    "Customer service was friendly and solved my issue quickly.",
    "Support team helped me with the setup and answered all questions.",
    "The battery lasts all day and the screen is very bright.",
    "The app crashes often and the performance is very slow.",
    "The website is difficult to navigate and the checkout is frustrating.",
    "Overall experience was excellent, and I will buy again soon.",
    "The mobile app is intuitive, fast, and easy to understand.",
    "I had a bad experience because the product broke after two days.",
    "The product is good but the shipping costs are too high.",
    "The refund process was smooth and the staff was professional.",
    "The product is great, the price is fair, and the quality is nice.",
    "The product feels good and the value is perfect.",
    "The delivery was quick, the price was reasonable, and the product is good.",
    "The quality is great and the service is cost effective.",
    "This product is nice, good, and worth the price.",
    "The product is perfect and the price is acceptable.",
    "The app is useful and the price is competitive.",
    "This is good value because the product is reliable and practical.",
    "The cost is fair and the quality feels worth it.",
    "The product is excellent and the price is not too high.",
    "The product is nice, the cost is good, and the quality is excellent.",
    "The product is great, the value is high, and the design is nice.",
    "This is a good product and the price is competitive.",
    "The product is perfect, simple, and very good.",
    "The page is clean, the product is nice, and the cost is fair.",
    "The price is good and the service is great.",
    "The product quality is good and the price remains reasonable.",
    "The value is clear and the product feels good.",
    "The price is worth it because the quality is excellent.",
    "The design is perfect and the product is very good.",
    "This service feels reliable and the price is reasonable.",
    "The package arrived on time but the instructions were confusing.",
    "I am unhappy with the delivery because it arrived late and damaged.",
]


def ensure_data():
    pd.DataFrame({"review": REVIEWS}).to_csv(DATA_PATH, index=False)
    return pd.read_csv(DATA_PATH)


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def prepare_sentences(data):
    stop_words = set(stopwords.words("english"))
    sentences = []
    for review in data["review"].fillna(""):
        tokens = word_tokenize(clean_text(review))
        tokens = [token for token in tokens if token.isalpha() and token not in stop_words and len(token) > 1]
        if tokens:
            sentences.append(tokens)
    return sentences


def build_model(sentences):
    model = Word2Vec(
        sentences=sentences,
        vector_size=100,
        window=5,
        min_count=2,
        sg=1,
        seed=42,
        workers=1,
    )
    model.save(str(MODEL_PATH))
    return model


def print_similar_words(model, word):
    try:
        similar = model.wv.most_similar(word, topn=10)
    except KeyError:
        print(f"Word '{word}' is not in the vocabulary.")
        return
    print(f"\nTop 10 words for '{word}':")
    for neighbor, similarity in similar:
        print(f"{neighbor}: {similarity:.4f}")


def cluster_words(model):
    words = model.wv.index_to_key
    vectors = np.array([model.wv[word] for word in words])
    n_clusters = min(10, len(words))
    if n_clusters < 2:
        return words, vectors, np.zeros(len(words), dtype=int)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(vectors)
    return words, vectors, labels


def print_cluster_summary(words, labels):
    clusters = {}
    for word, label in zip(words, labels):
        clusters.setdefault(label, []).append(word)
    print("\nClusters:")
    for label in sorted(clusters):
        items = clusters[label][:10]
        print(f"Cluster {label}: {', '.join(items)}")


def plot_clusters(words, vectors, labels):
    reducer = PCA(n_components=2, random_state=42)
    reduced = reducer.fit_transform(vectors)
    fig, ax = plt.subplots(figsize=(14, 8))
    for label in sorted(set(labels)):
        idx = np.where(labels == label)[0]
        ax.scatter(reduced[idx, 0], reduced[idx, 1], s=40, label=f"Cluster {label}")
        for i in idx:
            ax.text(reduced[i, 0], reduced[i, 1], words[i], fontsize=8)
    ax.set_title("Semantic clusters of words")
    ax.set_xlabel("PCA 1")
    ax.set_ylabel("PCA 2")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(PLOT_PATH)
    plt.close(fig)


def main():
    data = ensure_data()
    sentences = prepare_sentences(data)
    model = build_model(sentences)
    print("\nPrepared sentences:", len(sentences))
    print_similar_words(model, "good")
    print_similar_words(model, "price")
    words, vectors, labels = cluster_words(model)
    print_cluster_summary(words, labels)
    plot_clusters(words, vectors, labels)
    print(f"\nSaved model: {MODEL_PATH}")
    print(f"Saved cluster plot: {PLOT_PATH}")


if __name__ == "__main__":
    main()
