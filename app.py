
import os
import time
import requests
import streamlit as st

from dotenv import load_dotenv
from pypdf import PdfReader
from docx import Document


# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv()

try:
    API_KEY = st.secrets.get("API_KEY")
except Exception:
    API_KEY = None

API_KEY = API_KEY or os.getenv("API_KEY")

MODEL_NAME = "gemini-3.5-flash-lite"

API_URL = (
    f"https://generativelanguage.googleapis.com/"
    f"v1beta/models/{MODEL_NAME}:generateContent"
)

MAX_CHUNK_SIZE = 15000
MAX_RETRIES = 3
REQUEST_TIMEOUT = 60


# --------------------------------------------------
# Streamlit Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="QuickRead - AI Summarizer",
    page_icon="📚",
    layout="centered"
)

st.title("📚 QuickRead - AI Text Summarizer")

st.caption(
    "Summarize documents and text using AI "
    "in multiple languages."
)


# --------------------------------------------------
# Document Extraction
# --------------------------------------------------

def extract_file_text(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        if reader.is_encrypted:
            raise ValueError(
                "Password-protected PDFs are not supported."
            )

        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return "\n".join(pages)

    elif file_name.endswith(".txt"):

        return uploaded_file.getvalue().decode("utf-8-sig")

    elif file_name.endswith(".docx"):

        document = Document(uploaded_file)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        # Include text from DOCX tables as well.
        for table in document.tables:
            for row in table.rows:
                paragraphs.append(
                    " | ".join(cell.text for cell in row.cells)
                )

        return "\n".join(paragraphs)

    raise ValueError("Unsupported file format.")


# --------------------------------------------------
# Text Chunking
# --------------------------------------------------

def split_text(text, max_size=MAX_CHUNK_SIZE):

    paragraphs = text.splitlines()

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # Handle exceptionally long paragraphs.
        while len(paragraph) > max_size:

            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            chunks.append(paragraph[:max_size])
            paragraph = paragraph[max_size:]

        if not paragraph:
            continue

        if len(current_chunk) + len(paragraph) + 1 > max_size:

            chunks.append(current_chunk)
            current_chunk = paragraph

        else:

            current_chunk += "\n" + paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


# --------------------------------------------------
# Gemini API Integration
# --------------------------------------------------

def generate_summary(text, language):

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY
    }

    prompt = f"""
    You are a professional document summarization assistant.

    Summarize the provided content in {language}.

    Requirements:
    1. Preserve the original meaning.
    2. Include only information from the source.
    3. Do not invent facts or assumptions.
    4. Highlight important points.
    5. Use clear headings and bullet points where appropriate.
    6. Keep the summary concise but informative.

    Source content:

    {text}
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048
        }
    }

    for attempt in range(MAX_RETRIES):

        try:

            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT
            )

            if response.status_code in (429, 500, 502, 503, 504):

                if attempt < MAX_RETRIES - 1:

                    retry_after = response.headers.get("Retry-After")

                    try:
                        wait_time = min(
                            int(retry_after),
                            30
                        ) if retry_after else 2 ** attempt

                    except ValueError:
                        wait_time = 2 ** attempt

                    time.sleep(wait_time)
                    continue

            response.raise_for_status()

            data = response.json()

            candidates = data.get("candidates", [])

            if not candidates:
                feedback = data.get("promptFeedback", {})

                raise ValueError(
                    "No summary generated. "
                    f"API feedback: {feedback.get('blockReason', 'No candidate returned.')}"
                )

            candidate = candidates[0]

            parts = candidate.get("content", {}).get("parts", [])

            summary = "\n".join(
                part.get("text", "")
                for part in parts
                if part.get("text")
            ).strip()

            if not summary:
                raise ValueError(
                    "The API returned an empty summary."
                )

            return summary

        except requests.exceptions.Timeout:
            if attempt == MAX_RETRIES - 1:
                raise RuntimeError("API request timed out.")

            time.sleep(2 ** attempt)

        except requests.exceptions.HTTPError as error:

            status_code = error.response.status_code

            if status_code == 429:
                raise RuntimeError(
                    "API rate limit exceeded. Please try again later."
                )

            if status_code == 400:
                raise RuntimeError(
                    "Invalid request. Please check your input."
                )

            if status_code in (401, 403):
                raise RuntimeError(
                    "API authentication failed. Check your API key."
                )

            raise RuntimeError(
                f"Gemini API error: HTTP {status_code}"
            )

        except requests.exceptions.RequestException:
            if attempt == MAX_RETRIES - 1:
                raise RuntimeError(
                    "Unable to connect to Gemini API."
                )

            time.sleep(2 ** attempt)

    raise RuntimeError("Unable to generate summary.")


# --------------------------------------------------
# Complete Document Summarization
# --------------------------------------------------

def summarize_document(text, language):

    chunks = split_text(text)

    if not chunks:
        raise ValueError("No readable text found in the input.")

    summaries = []

    progress = st.progress(0)

    status = st.empty()

    total_chunks = len(chunks)

    for index, chunk in enumerate(chunks):

        status.write(
            f"Processing document: {index + 1}/{total_chunks}"
        )

        chunk_summary = generate_summary(
            chunk,
            language
        )

        summaries.append(chunk_summary)

        progress.progress(
            (index + 1) / total_chunks
        )

    if len(summaries) == 1:
        return summaries[0]

    status.write("Combining all section summaries...")

    combined_text = "\n\n".join(summaries)

    final_summary = generate_summary(
        combined_text,
        language
    )

    progress.progress(100)

    status.success("Summarization completed!")

    return final_summary


# --------------------------------------------------
# User Interface
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📂 Upload PDF, TXT or DOCX",
    type=["pdf", "txt", "docx"]
)

pasted_text = st.text_area(
    "Or paste your text here:",
    height=250,
    placeholder="Paste your content here..."
)

language = st.selectbox(
    "Choose summary language:",
    [
        "English",
        "Telugu",
        "Hindi",
        "Spanish",
        "French",
        "German"
    ]
)

# Uploaded file takes priority.
input_text = ""

if uploaded_file:

    try:
        input_text = extract_file_text(uploaded_file)

    except Exception as error:
        st.error(f"File processing error: {error}")

else:
    input_text = pasted_text


# --------------------------------------------------
# Summarize Button
# --------------------------------------------------

if st.button("✨ Summarize", type="primary"):

    if not input_text.strip():

        st.warning(
            "Please upload a document or paste some text."
        )

    elif not API_KEY:

        st.error(
            "API key not found. Configure API_KEY in "
            "Streamlit Secrets or your local .env file."
        )

    else:

        with st.spinner("Generating your AI summary..."):

            try:

                summary = summarize_document(
                    input_text,
                    language
                )

                st.subheader(
                    f"📌 Summary in {language}"
                )

                st.success(summary)

                st.download_button(
                    label="⬇️ Download Summary",
                    data=summary,
                    file_name="quickread_summary.txt",
                    mime="text/plain"
                )

            except Exception as error:

                st.error(str(error))


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "QuickRead | Built with Python, Streamlit and Google Gemini AI"
)
