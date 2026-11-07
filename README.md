# QuickRead AI – Smart Document Summarizer

An AI-powered document summarization application built using **Python, Streamlit, and Google Gemini API**.

QuickRead AI helps users extract meaningful insights from lengthy documents by generating concise, accurate summaries in multiple languages. Users can upload PDF, TXT, and DOCX files or directly paste text to generate summaries.

**Live Application:** https://plain-summarizer.streamlit.app/

---

## Features

### Document Processing
- **Multiple File Formats:** Upload PDF, TXT, and DOCX documents.
- **Text Extraction:** Extract text from PDF files using `pypdf` and Word documents using `python-docx`.
- **File Validation:** Validate file types, file size, document structure, and extracted content.
- **Upload Size Limit:** Supports files up to 20 MB.
- **Text Input:** Paste text directly without uploading a document.
- **Document Size Validation:** Prevents excessively large documents from being processed.

### AI-Powered Summarization
- **Google Gemini Integration:** Generate intelligent summaries using the Gemini REST API.
- **Multi-language Support:** Generate summaries in:
  - English
  - Telugu
  - Hindi
  - Spanish
  - French
  - German
- **Hierarchical Summarization:** Process large documents in smaller chunks and combine intermediate summaries into a final summary.
- **Context Preservation:** Maintain important facts, figures, dates, names, and conclusions.
- **Prompt Injection Protection:** Treat document content as untrusted input and prevent embedded instructions from overriding summarization requirements.

### Reliability and Security
- **Retry Mechanism:** Implement bounded retries with exponential backoff and jitter for temporary API failures.
- **Timeout Handling:** Configure connection and response timeouts for API requests.
- **Error Handling:** Handle API failures, invalid documents, empty files, and unsupported content.
- **Secure API Configuration:** Store API credentials using Streamlit Secrets or environment variables.
- **Resource Limits:** Restrict document size, PDF page count, and processing chunks.

### User Interface
- Modern dark-themed interface.
- Responsive Streamlit layout.
- Document upload and text input options.
- Summary generation progress indicator.
- Download generated summaries as `.txt` files.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.9+ | Backend application logic |
| Streamlit | Web application UI |
| Google Gemini API | AI-powered summarization |
| Requests | REST API communication |
| pypdf | PDF text extraction |
| python-docx | DOCX document processing |
| python-dotenv | Local environment variable management |
| TOML | Streamlit application configuration |

---

## Project Architecture

The application follows a modular processing flow within a single Python application.

```text
                User
                 |
                 v
          Streamlit Interface
                 |
                 v
       Document Upload / Text Input
                 |
                 v
         Input Validation
                 |
                 v
        Document Extraction
                 |
                 v
          Text Processing
                 |
                 v
        Text Chunking Logic
                 |
                 v
       Google Gemini REST API
                 |
                 v
       Chunk-wise Summarization
                 |
                 v
       Intermediate Summaries
                 |
                 v
          Final Summary
                 |
                 v
        Display / Download
```

### Summarization Workflow

1. Users upload a document or paste text.
2. The application validates the input and extracts document content.
3. Large documents are divided into manageable text chunks.
4. Each chunk is independently processed using the Gemini API.
5. Intermediate summaries are combined when necessary.
6. Gemini generates the final summary in the selected language.
7. Users can view and download the generated summary.

---

## Project Structure

```text
gemini-text-summarizer/
│
├── .streamlit/
│   └── config.toml          # Streamlit server configuration
│
├── app.py                   # Main Streamlit application
│
├── requirements.txt         # Python dependencies
│
├── .gitignore               # Git ignored files
│
├── .env                     # Local API credentials (not committed)
│
└── README.md                # Project documentation
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/harivishnu735/gemini-text-summarizer.git

cd gemini-text-summarizer
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API Key

Obtain your API key through Google AI Studio:

https://aistudio.google.com/apikey

For local development, create a `.env` file in the project root directory.

```env
API_KEY=your_google_gemini_api_key
```

For Streamlit Cloud deployment:

1. Open your application in Streamlit Community Cloud.
2. Navigate to App Settings.
3. Open Secrets.
4. Add the following configuration:

```toml
API_KEY = "your_google_gemini_api_key"
```

**Security Note:** Never commit `.env` files or expose API credentials in public repositories.

### 5. Configure Streamlit

Create the following file:

`.streamlit/config.toml`

```toml
[server]
maxUploadSize = 20
```

This configures the maximum upload size to 20 MB.

### 6. Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## Application Configuration

The application includes configurable processing limits.

| Configuration | Value |
|---|---:|
| Maximum upload size | 20 MB |
| Maximum extracted document size | 450,000 characters |
| Maximum PDF pages | 300 |
| Maximum chunk size | 12,000 characters |
| Maximum document chunks | 40 |
| API retry attempts | 3 |
| Connection timeout | 10 seconds |
| API response timeout | 90 seconds |

These limits help control resource consumption and API request sizes.

---

## Error Handling

The application handles common processing and API errors, including:

- Missing API credentials.
- Unsupported file formats.
- Empty documents.
- Invalid PDF and DOCX files.
- Password-protected PDFs.
- Documents exceeding configured limits.
- Gemini API rate limits.
- Temporary API server errors.
- Connection and timeout failures.
- Empty or incomplete AI responses.
- Model safety restrictions.

---

## Limitations

- Scanned PDFs and image-based documents require OCR and are not currently supported.
- Password-protected PDFs cannot be processed.
- Summarization quality depends on the source document and AI model.
- API availability and usage quotas depend on the Google Gemini API account.
- Large or complex documents may require multiple API requests.
- Prompt injection defenses reduce risk but cannot guarantee complete protection against malicious document content.

---

## Deployment

The application is deployed using **Streamlit Community Cloud**.

**Live Demo:** https://plain-summarizer.streamlit.app/

Deployment workflow:

1. Push application changes to GitHub.
2. Connect the repository to Streamlit Community Cloud.
3. Configure the Gemini API key using Streamlit Secrets.
4. Configure application dependencies through `requirements.txt`.
5. Deploy and monitor application status.

GitHub acts as the source repository, while Streamlit Community Cloud handles application deployment.

---

## Future Enhancements

- OCR support for scanned PDF documents.
- Export summaries as PDF and DOCX.
- Summary history and document management.
- User authentication and personalized workspaces.
- Additional language support.
- Advanced summary customization.
- Document comparison and key-point extraction.

---

## Author

**Hari Vishnu Dadi**

Node.js & Python Developer

- **LinkedIn:** https://www.linkedin.com/in/hari-vishnu-dadi/
- **GitHub:** https://github.com/harivishnu735

---

**QuickRead AI – Transform lengthy documents into meaningful insights.**
