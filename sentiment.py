import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_json(text: str):
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start:end])
    except Exception:
        return None


def analyze_texts(texts):
    if not texts:
        return {
            "average_score": 0,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "total": 0
        }

    texts = texts[:60]
    joined = "\n".join([f"{i+1}. {t}" for i, t in enumerate(texts)])

    prompt = f"""
You are a strict sentiment classifier.

For each sentence classify sentiment as:
Positive / Neutral / Negative

Return ONLY JSON. No explanation.

Format:
{{
  "positive": <int>,
  "neutral": <int>,
  "negative": <int>
}}

Sentences:
{joined}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text
        data = extract_json(text)

        if not data:
            raise ValueError("Invalid JSON")

    except Exception:
        return {
            "average_score": 0,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "total": 0
        }

    total = data["positive"] + data["neutral"] + data["negative"]

    if total == 0:
        return {
            "average_score": 0,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "total": 0
        }

    score = (data["positive"] - data["negative"]) / total

    return {
        "average_score": round(score, 3),
        "positive": data["positive"],
        "neutral": data["neutral"],
        "negative": data["negative"],
        "total": total
    }
