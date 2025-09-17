import streamlit as st
import requests
import json

API_KEY = "AIzaSyAXnrK_DLtZRct1MbOtgnUQyHNxT_MA2Ws"  # Replace with your actual API key
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Streamlit UI
st.set_page_config(page_title="Gemini Text Summarizer (REST API)", layout="centered")
st.title("Gemini REST API - Text Summarizer")

input_text = st.text_area("Enter your text to summarize:", height=300)

if st.button("Summarize"):
    if not input_text.strip():
        st.warning("Please enter text to summarize.")
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
                                "text": f"Summarize the following text clearly and accurately without adding false info:\n\n{input_text}"
                            }
                        ]
                    }
                ]
            }

            try:
                response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
                response.raise_for_status()
                summary = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                st.subheader("📌 Summary:")
                st.success(summary)
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
