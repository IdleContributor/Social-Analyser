import re
from collections import Counter

STOPWORDS = {
    "the","is","a","an","and","or","to","of","in","on","for","with","this","that",
    "it","as","are","was","were","be","been","being","at","by","from","about"
}


def extract_topics(text: str, top_n: int = 3):
    words = re.findall(r"[a-zA-Z]{3,}", text.lower())

    filtered = [w for w in words if w not in STOPWORDS]

    if not filtered:
        return ["general topic"]

    freq = Counter(filtered)
    keywords = [w for w, _ in freq.most_common(top_n)]

    return keywords
