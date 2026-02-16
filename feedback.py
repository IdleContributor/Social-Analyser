import os
import json
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

# clients
gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_json(text):
    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])


def gemini_call(prompt):
    response = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def groq_call(prompt):
    response = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content


def analyze_and_generate(user_text, public_sentiment, query):

    prompt = f"""
You are an AI social media analyzer.

User Post:
"{user_text}"

Topic:
{query}

Public Sentiment Statistics:
Positive: {public_sentiment['positive']}
Neutral: {public_sentiment['neutral']}
Negative: {public_sentiment['negative']}

Return STRICT JSON only:

{{
  "tone_comparison": "...",
  "tips": ["tip1","tip2","tip3"],
  "rewritten_post": "..."
}}
"""

    # --- Try Gemini first ---
    try:
        text = gemini_call(prompt)
        return extract_json(text)

    # --- If quota exceeded → fallback to Groq ---
    except Exception as e:
        print("Gemini failed, switching to Groq:", e)
        text = groq_call(prompt)
        return extract_json(text)
