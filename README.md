# Gemini Text Summarizer

An AI-powered text summarization app built with **Python** and **Streamlit**, using the **Google Gemini API**.  
This app allows users to upload documents or paste text, and get a clear, concise summary in multiple languages.

---

## Features
-  **File Upload Support**: Upload **PDF, TXT, or DOCX** files.  
-  **Multi-language summaries**: English, Telugu, Hindi, Spanish, French, German.  
-  **Paste text option**: Works even without file upload.  
-  **Download summary**: Save the result as a `.txt` file.  
-  **Error handling**: Warns if no input or missing API key.  
-  Clean and simple **Streamlit UI**. 

---

## Tech Stack
- **Python 3.9+**  
- **Streamlit** (for UI)  
- **Requests** (for REST API calls)  
- **pypdf** (PDF text extraction)  
- **python-docx** (Word file parsing)  
- **python-dotenv** (for local `.env` API keys)  
- **Google Gemini API**  

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
Gemini_API_KEY = your_google_gemini_api_key

# Note: `.env` is not included in the repo for security reasons.

## 5️ Run the app
streamlit run app.py

# Author
Hari Vishnu
Node.js & Python Developer
LinkedIn - www.linkedin.com/in/hari-vishnu-dadi
GitHub - https://github.com/harivishnu735
