from ddgs import DDGS
import re

def looks_like_opinion(text: str) -> bool:
    text = text.lower()

    opinion_words = [
        "issue", "problem", "good", "bad", "better", "worse",
        "drain", "slow", "fast", "love", "hate", "fix", "bug",
        "improve", "complain", "review", "experience"
    ]

    if any(word in text for word in opinion_words):
        return True

    # sentences longer than 8 words are usually meaningful
    if len(text.split()) >= 8:
        return True

    return False


def fetch_web_reviews(query: str, max_results: int = 40):
    texts = []

    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            region="us-en",
            safesearch="moderate",
            max_results=max_results
        )

        for r in results:
            snippet = r.get("body", "")
            if snippet and looks_like_opinion(snippet):
                texts.append(snippet)

    return texts
