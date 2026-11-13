import os
import re
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nltk
import pandas as pd
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

DATA_FILE = "feedback.csv"
WORDFREQ_FILE = "feedback_word_freq.png"
BIGRAM_FILE = "feedback_bigrams.csv"
WORDCLOUD_FILE = "feedback_word_cloud.png"


def build_reviews():
    return [
        "The product is very easy to use and the design looks modern.",
        "I am unhappy with the delivery because it arrived late and damaged.",
        "Customer service was friendly and solved my issue quickly.",
        "The app crashes often and the performance is very slow.",
        "I love the quality of this product and would definitely recommend it.",
        "Support team helped me with the setup and answered all questions.",
        "The battery lasts all day and the screen is very bright.",
        "The package arrived on time but the instructions were confusing.",
        "This service feels reliable and the price is reasonable.",
        "The website is difficult to navigate and the checkout is frustrating.",
        "Overall experience was excellent, and I will buy again soon.",
        "The mobile app is intuitive, fast, and easy to understand.",
        "I had a bad experience because the product broke after two days.",
        "The product is good but the shipping costs are too high.",
        "The refund process was smooth and the staff was professional.",
    ]


def load_data(path):
    if not os.path.exists(path):
        reviews = build_reviews()
        pd.DataFrame({"review": reviews}).to_csv(path, index=False)
    return pd.read_csv(path)


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def count_tokens_before_and_after(cleaned_reviews):
    token_lists = [word_tokenize(review) for review in cleaned_reviews]
    tokens_before = [token for row in token_lists for token in row]
    stop_words = set(stopwords.words("english"))
    tokens_after = [
        token for row in token_lists for token in row if token not in stop_words and len(token) >= 3
    ]
    return len(tokens_before), len(tokens_after), token_lists, tokens_after


def save_word_frequency_chart(frequencies):
    data = pd.DataFrame(frequencies.most_common(15), columns=["word", "frequency"])
    data = data.sort_values("frequency", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(data["word"], data["frequency"], color="steelblue")
    ax.set_title("Top 15 words by frequency")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Word")
    ax.invert_yaxis()
    for bar, value in zip(ax.patches, data["frequency"]):
        ax.text(value + 0.2, bar.get_y() + bar.get_height() / 2, str(value), va="center")
    fig.tight_layout()
    fig.savefig(WORDFREQ_FILE)
    plt.close(fig)
    return data


def save_wordcloud(frequencies):
    wordcloud = WordCloud(width=800, height=500, background_color="white").generate_from_frequencies(frequencies)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(WORDCLOUD_FILE)
    plt.close(fig)


def save_bigrams(tokens):
    freq = Counter(bigrams(tokens))
    bigram_data = pd.DataFrame(
        [{"bigram": " ".join(pair), "frequency": count} for pair, count in freq.most_common(10)]
    )
    bigram_data.to_csv(BIGRAM_FILE, index=False)
    return bigram_data


def main():
    df = load_data(DATA_FILE)
    df["clean_review"] = df["review"].apply(clean_text)
    print(f"Rows count: {len(df)}")
    words_per_row = df["review"].apply(lambda text: len(str(text).split()))
    print(f"Average length of reviews in words: {words_per_row.mean():.2f}")

    before_tokens, after_tokens, token_lists, filtered_tokens = count_tokens_before_and_after(df["clean_review"])
    print(f"Total tokens before cleaning: {before_tokens}")
    print(f"Total tokens after cleaning: {after_tokens}")

    frequencies = Counter(filtered_tokens)
    print("Top 15 most common words:")
    for word, count in frequencies.most_common(15):
        print(f"{word}: {count}")

    save_word_frequency_chart(frequencies)
    save_wordcloud(frequencies)
    bigram_data = save_bigrams(filtered_tokens)
    print("\nTop 10 bigrams:")
    print(bigram_data.to_string(index=False))
    print(f"\nSaved word frequency chart: {WORDFREQ_FILE}")
    print(f"Saved word cloud: {WORDCLOUD_FILE}")
    print(f"Saved bigram data: {BIGRAM_FILE}")


if __name__ == "__main__":
    main()
