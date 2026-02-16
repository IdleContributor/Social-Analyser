from newsapi import NewsApiClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))


def get_from_date(time_range):
    now = datetime.utcnow()

    if time_range == "day":
        return now - timedelta(days=1)
    if time_range == "week":
        return now - timedelta(days=7)
    if time_range == "month":
        return now - timedelta(days=30)
    if time_range == "year":
        return now - timedelta(days=365)

    return None


def fetch_news(query, time_range="all"):
    params = {
        "q": query,
        "language": "en",
        "sort_by": "relevancy",
        "page_size": 40
    }

    from_date = get_from_date(time_range)
    if from_date:
        params["from_param"] = from_date.strftime("%Y-%m-%d")

    articles = newsapi.get_everything(**params)

    texts = []
    for a in articles["articles"]:
        if a["title"]:
            texts.append(a["title"])
        if a["description"]:
            texts.append(a["description"])

    return texts
