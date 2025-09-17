# Gemini Text Summarizer

A simple AI-powered text summarization app built with **Python** and **Streamlit**, using **Google Gemini API**.  
This app allows users to paste long or complex text and get a clear, concise summary for easier understanding.

---

## Features
- Summarizes long text into simple, easy-to-read content.  
- Clean user interface with **Streamlit**.  
- Integrates with **Google Gemini REST API**.  
- Handles invalid or empty input gracefully.  

---

## Tech Stack
- **Python 3.9+**
- **Streamlit** (for the UI)  
- **Requests** (for REST API calls)  
- **Google Gemini API** (for summarization)  

---

## Project Structure
.
├── app.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── .gitignore # Ignore sensitive & large files
└── README.md # Project documentation


# Setup Instructions

## 1 Clone the repository
git clone https://github.com/<your-username>/gemini-text-summarizer.git
cd gemini-text-summarizer

## 2️ Create & activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

## 3️ Install dependencies
pip install -r requirements.txt

## 4️ Create a .env file in the root directory and add your Gemini API key:
API_KEY=your_google_gemini_api_key

## 5️ Run the app
streamlit run app.py
