
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


# --------------------------------------------------
# PREMIUM QUICKREAD UI THEME
# --------------------------------------------------

st.markdown("""
<style>

/* Main application background */
.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #24204b 0%, transparent 38%),
        radial-gradient(ellipse at 90% 20%, #102f49 0%, transparent 35%),
        #0b1020;
    color: #f8fafc;
}

/* Main content width and spacing */
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Header */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Hero section */
.hero {
    text-align: center;
    padding: 42px 25px 32px;
    margin-bottom: 25px;
}

.hero-badge {
    display: inline-block;
    background: rgba(139, 92, 246, 0.15);
    border: 1px solid rgba(167, 139, 250, 0.4);
    color: #c4b5fd;
    padding: 8px 17px;
    border-radius: 30px;
    font-size: 13px;
    letter-spacing: 0.5px;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: clamp(34px, 5vw, 52px);
    font-weight: 800;
    letter-spacing: -1.8px;
    background: linear-gradient(
        90deg,
        #ffffff,
        #c4b5fd,
        #67e8f9
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 14px;
}

.hero p {
    color: #a5b4cc;
    font-size: 16px;
    line-height: 1.8;
}

/* Section headings */
h2, h3 {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(21, 29, 50, 0.85);
    border: 1px solid #34415e;
    border-radius: 16px;
    padding: 15px;
}

[data-testid="stFileUploaderDropzone"] {
    background: #18233a;
    border: 1px dashed #6473a0;
    border-radius: 12px;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #e2e8f0 !important;
}

/* Text area */
.stTextArea textarea {
    background: #151d32 !important;
    color: #f8fafc !important;
    border: 1px solid #35435f !important;
    border-radius: 12px !important;
    font-size: 14px !important;
}

.stTextArea textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 1px #8b5cf6 !important;
}

/* Select box */
[data-testid="stSelectbox"] > div > div {
    background: #151d32 !important;
    border-color: #35435f !important;
    border-radius: 10px !important;
    color: white !important;
}

/* Buttons */
.stButton button,
.stDownloadButton button {
    background: linear-gradient(
        100deg,
        #7c3aed,
        #4f46e5
    ) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 650 !important;
    transition: all 0.2s ease;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: linear-gradient(
        100deg,
        #6d28d9,
        #4338ca
    ) !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(124, 58, 237, 0.3);
}

/* Labels */
label, .stMarkdown p {
    color: #d1d9e8;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(
        90deg,
        #8b5cf6,
        #22d3ee
    );
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Dividers */
hr {
    border-color: #29344c;
}

/* Footer */
.footer {
    text-align: center;
    color: #8290a9;
    font-size: 13px;
    padding: 25px 10px;
    border-top: 1px solid #29344c;
    margin-top: 45px;
}

/* Mobile */
@media (max-width: 640px) {
    .block-container {
        padding: 1rem 1rem 3rem;
    }

    .hero {
        padding: 30px 10px;
    }
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# PREMIUM HERO SECTION
# --------------------------------------------------

st.markdown("""
<div class="hero">

    <div class="hero-badge">
        ✨ AI POWERED DOCUMENT INTELLIGENCE
    </div>

    <h1>QuickRead AI</h1>

    <p>
        Transform lengthy documents into meaningful insights.<br>
        Upload, summarize and understand your content
        in multiple languages.
    </p>

</div>
""", unsafe_allow_html=True)

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

                st.markdown("### ✨ Your AI Summary")

                with st.container(border=True):
                
                    st.markdown(f"**Summary Language:** {language}")
                
                    st.divider()
                
                    st.markdown(summary)
                
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
