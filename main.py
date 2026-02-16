from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
import pdfplumber
import easyocr
from pdf2image import convert_from_bytes
import io

from topic import extract_topics
from query_builder import build_search_query

from news import fetch_news
from web_reviews import fetch_web_reviews
from feedback import analyze_and_generate

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.concurrency import run_in_threadpool



app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Load OCR model once at startup
reader = easyocr.Reader(['en'], gpu=False)


# ---------- TEXT EXTRACTION FUNCTIONS ----------

def extract_from_pdf(file_bytes: bytes) -> str:
    text = ""

    # 1️⃣ Try normal selectable text extraction
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        pass

    # 2️⃣ If empty → scanned PDF → OCR fallback
    if not text.strip():
        try:
            images = convert_from_bytes(file_bytes)
            for img in images:
                img_bytes = io.BytesIO()
                img.save(img_bytes, format="PNG")
                results = reader.readtext(img_bytes.getvalue())
                text += " ".join([res[1] for res in results]) + "\n"
        except Exception:
            raise HTTPException(status_code=400, detail="Failed to process PDF file")

    return text.strip()


def extract_from_image(file_bytes: bytes) -> str:
    try:
        results = reader.readtext(file_bytes)
        return " ".join([res[1] for res in results]).strip()
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to read image")


# ---------- API ROUTE ----------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(None),
    text: str = Form(None),
    time_range: str = Query("all")
):
    extracted_text = ""

    # Prevent both inputs
    if text and file:
        raise HTTPException(
        status_code=400,
        detail="Provide either text OR file, not both."
        )


    # Case 1: Direct text input
    if text and text.strip():
        extracted_text = text.strip()

    # Case 2: File upload
    elif file:
        contents = await file.read()
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            extracted_text = extract_from_pdf(contents)

        elif filename.endswith((".png", ".jpg", ".jpeg")):
            extracted_text = extract_from_image(contents)

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

    else:
        raise HTTPException(status_code=400, detail="No input provided")

    if not extracted_text:
        raise HTTPException(status_code=400, detail="No readable text found")

    # ---------- TOPIC & QUERY ----------
    topics = extract_topics(extracted_text)
    search_query = build_search_query(topics, extracted_text)

    # ---------- COLLECT PUBLIC DATA ----------
    try:
        news_texts = await run_in_threadpool(fetch_news, search_query, time_range)
    except:
        news_texts = []

    try:
        web_texts = await run_in_threadpool(fetch_web_reviews, search_query)
    except:
        web_texts = []

    public_texts = news_texts + web_texts

    # ensure we have some data
    if not public_texts:
        public_texts = ["No strong public opinion found about this topic"]

    # ---------- SENTIMENT ----------
    # simple public sentiment approximation (only counts tone words)
    public_sentiment = {
    "positive": sum(any(w in t.lower() for w in ["good","great","love","better","improve"]) for t in public_texts),
    "neutral": sum(any(w in t.lower() for w in ["ok","fine","average"]) for t in public_texts),
    "negative": sum(any(w in t.lower() for w in ["bad","issue","problem","worse","drain"]) for t in public_texts),
}


    # ---------- FEEDBACK ----------
    analysis = await run_in_threadpool(
    analyze_and_generate,
    extracted_text,
    public_sentiment,
    search_query
)

    # ---------- RESPONSE ----------
    return {
    "extracted_text": extracted_text,
    "detected_topics": topics,
    "search_query": search_query,
    "public_sentiment": public_sentiment,
    "analysis": analysis
}

