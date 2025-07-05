# Text Summarizer

A FastAPI-based service for uploading PDF files, extracting text, and generating summaries.

## Features

- 📂 Upload PDF files
- 🔍 Extract text by:
  - Entire document (`full`)
  - Specific pages (`pages`)
  - Chapters (`chapter`)
- ✍️ Summarize extracted text using a transformer model
- 💾 Download the generated summary as a `.txt` file
- 🧹 Auto-cleans temporary files after download

---

## Endpoints

### `POST /upload-and-summarize/`

Uploads a PDF file, extracts text, summarizes it, and returns a download link.

**Form Data:**

| Field     | Type       | Required | Description                              |
|-----------|------------|----------|------------------------------------------|
| `file`    | `UploadFile` | ✅       | PDF file to upload                       |
| `mode`    | `string`    | ✅       | Extraction mode: `full`, `pages`, `chapter` |
| `chapter` | `string`    | ❌       | Chapter title or number (if `mode=chapter`) |
| `pages`   | `string`    | ❌       | Page numbers (comma-separated, if `mode=pages`) |

**Parameters:**

- `file`: PDF file to upload (form-data)
- `mode`: Extraction mode (`full`, `pages`, or `chapter`)
- `chapter`: (optional) Chapter name/number if `mode=chapter`
- `pages`: (optional) Page numbers if `mode=pages`

**Response:**

```json
{
  "status": "success",
  "summary": "Short summary text...",
  "download_link": "/download-summary/?file=..."
}

### `GET /download-summary/`

Download the summary as a text file.

**Parameters:**

- `file`: Path to the summary file (from the previous response)

## Setup

Follow these steps to get the project running on your local machine:

1. **Clone the repository or download the code:**
    - If using git:
      ```sh
      git clone <repo-url>
      cd text-summarizer
      ```
    - Or simply download and extract the ZIP, then open the folder.

2. **(Optional but recommended) Create and activate a virtual environment:**
    ```sh
    python -m venv .venv
    venv\Scripts\activate
    ```

3. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Start the FastAPI server:**
    ```sh
    uvicorn main:app --reload
    ```

5. **Access the API documentation:**
    - Open your browser and go to (http://127.0.0.1:8000/docs) to interact with the API using the Swagger



## Project Structure

text-summarizer/
│
├── main.py            # FastAPI app and endpoints
├── extraction.py      # PDF text extraction logic
├── summarize.py       # Text summarization logic
├── schemas.py         # Pydantic models for request/response validation
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
└── ...                # Any other files or folders

## Requirements

Below are the main dependencies you need (add these to your `requirements.txt` if not already present):

```

fastapi
uvicorn
pydantic
python-multipart
PyMuPDF
