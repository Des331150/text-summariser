import os
from fastapi import FastAPI, File, UploadFile, Query, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from extraction import extract_text_from_pdf
import tempfile
from schemas import SummaryText
from summarize import summarize_text

app = FastAPI(title="PDF Text Summarizer", description="API for extracting text from PDF files and summarizing it.", version="1.0.0")

@app.post("/upload-and-summarize/", response_model=SummaryText)
async def upload_and_summarize(file: UploadFile = File(description="Upload file, extract text and summarize."), mode: str = Query(..., enum=["full", "pages", "chapter"]), chapter: str | None = None, pages: str | None = None):
    try:
        file_bytes = await file.read()
        with tempfile.NamedTemporaryFile(mode="wb", delete=True) as temp:
            temp.write(file_bytes)
            temp_path = temp.name

        text = extract_text_from_pdf(temp_path, mode=mode, chapter=chapter, pages=pages)
        os.unlink(temp_path)

        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF.")
        else:
            summary = summarize_text(text)

        with tempfile.NamedTemporaryFile(mode="w", delete=True, encoding="utf-8") as summary_file:
            summary_file.write(summary)
            summary_path = summary_file.name

        return {"status": "success" ,"summary": summary, "download_link": f"/download-summary/?file={summary_path}"}
    except Exception as e:
        raise e


@app.get("/download-summary/")
def download_summary(background_tasks: BackgroundTasks, file: str = Query(..., description="Path to the summary file")):
    if not os.path.exists(file):
        raise HTTPException(status_code=404, detail="Summary file not found")
    
    background_tasks.add_task(os.remove, file)
    return FileResponse(file, filename="summary.txt", media_type="text/plain")