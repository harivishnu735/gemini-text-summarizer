import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from pypdf import PdfReader
import docx

# Load local .env (for local testing)
load_dotenv()

API_KEY = None
try:
    API_KEY = st.secrets["API_KEY"]  # works only on Streamlit Cloud
except Exception:
    API_KEY = os.getenv("API_KEY")   # fallback for local .env


API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Streamlit UI
st.set_page_config(page_title="QuickRead - AI Summarizer", layout="centered")
st.title("Smart AI Text Summarizer")

# File upload
uploaded_file = st.file_uploader("📂 Upload a file (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])

file_text = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            file_text += page.extract_text() or ""
    elif uploaded_file.type == "text/plain":
        file_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        file_text = "\n".join([para.text for para in doc.paragraphs])

# Two sources: either uploaded file OR pasted text
pasted_text = st.text_area("Or paste your text to summarize:", height=250)

# Final text = file content if uploaded, else pasted text
input_text = file_text if file_text else pasted_text


# Language selection
language = st.selectbox(
    "Choose summary language:",
    ["English", "Telugu", "Hindi", "Spanish", "French", "German"]
)

if st.button("Summarize"):
    if not input_text.strip():
        st.warning("Please provide text (paste or upload a file).")
    elif not API_KEY:
        st.error("API key not found. Add API_KEY in Streamlit Secrets or .env file.")
    else:
        with st.spinner("Summarizing using Gemini REST API..."):
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": API_KEY
            }

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"Summarize the following text clearly and accurately in {language} without adding false info:\n\n{input_text}"
                            }
                        ]
                    }
                ]
            }

            try:
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()

                summary = ""
                candidates = data.get("candidates", [])
                if candidates:
                    summary = (
                        candidates[0]
                        .get("content", {})
                        .get("parts", [{}])[0]
                        .get("text", "")
                    )

                if summary:
                    st.subheader(f"📌 Summary in {language}:")
                    st.success(summary)
                    # Download button
                    st.download_button("⬇️ Download Summary", summary, file_name="summary.txt")
                else:
                    st.error("No summary returned. Check API quota or input size.")
            except requests.exceptions.RequestException as e:
                st.error(f"Request error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
