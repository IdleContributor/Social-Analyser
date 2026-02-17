# Social Media Content Analyzer

An AI-powered web application that analyzes user content (text, images, or PDFs), compares it with real-world public opinion, and generates **engagement improvement suggestions**.

The system extracts text from uploaded documents, identifies the topic, gathers related information from news and web sources, and uses LLM reasoning to provide actionable feedback and a rewritten improved post.

## Features

- Upload Text, Image, or PDF
- OCR extraction for scanned documents
- Automatic topic detection
- Public opinion collection (News + Web results)
- AI tone comparison
- Engagement improvement tips
- Rewritten optimized post
- Time-range filtering (24h, week, month, year, all)

## Tech Stack

### Backend
- FastAPI
- Python

### AI & NLP
- Gemini API
- Groq (fallback LLM)
- Lightweight keyword extraction

### Data Extraction
- EasyOCR (image text extraction)
- pdfplumber + pdf2image

### Data Sources
- NewsAPI (headlines)
- DuckDuckGo search results

### Frontend
- Jinja2 Templates (server-rendered UI)

## How It Works

1. User submits text or uploads a document
2. System extracts readable content
3. Topic is detected automatically
4. Related public data is fetched
5. Public sentiment is estimated
6. LLM compares user tone vs public tone
7. AI generates:
   - Tone comparison
   - Engagement tips
   - Rewritten improved post

## Running Locally

```bash
# 1. Clone Repository
git clone https://github.com/yourusername/social-analyser.git
cd social-analyser

# 2. Create Virtual Environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Add Environment Variables
# Create .env file with:
GEMINI_API_KEY=your_key
GROQ_API_KEY=your_key
NEWS_API_KEY=your_key

# 5. Run Server
uvicorn main:app --reload

Open:
http://127.0.0.1:8000

DeploymentStart command:bash

uvicorn main:app --host 0.0.0.0 --port 10000

Design Decisions

LLM used only for reasoning, not preprocessing
Fallback AI provider prevents quota failures
Lightweight topic extraction avoids heavy ML dependencies
OCR fallback handles scanned documents

→ This ensures reliability, speed, and deployability.

Future Improvements

Social media API integration
Sentiment visualization charts
Multi-language support
User history dashboard

```

## Author

Simarjot Singh
