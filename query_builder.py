import re

GENERIC_WORDS = {
    "today", "thing", "something", "really",
    "very", "like", "crazy", "much", "many"
}

def build_search_query(topics, original_text):
    if not topics:
        return original_text

    query = topics[0]

    # remove weak words
    words = [
        w for w in query.split()
        if w.lower() not in GENERIC_WORDS
    ]

    query = " ".join(words)

    # fallback if too short
    if len(query.split()) < 2:
        query = original_text

    return query
