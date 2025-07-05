import os
from fastapi import FastAPI, File, UploadFile, Query, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from extraction import extract_text_from_pdf
import tempfile
from schemas import TextInput, SummaryText
from summarize import summarize_text

app = FastAPI()

# @app.post("/uploadfiles/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}


@app.post("/extract/")
async def extract_text(file: UploadFile = File(description="Extract files."), mode: str = Query(..., enum=["full", "page", "chapter"]), chapter_title: str | None = None, pages: str | None = None):
    file_bytes = await file.read()
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    text = extract_text_from_pdf(tmp_path)
    os.unlink(tmp_path)
    return {"text": text}

@app.post("/summarize/", response_model=SummaryText)
async def summarize_route(
    text: TextInput,
    mode: str = Query(..., enum=["full", "page", "chapter"]),
    chapter_title: str | None = None,
    pages: str | None = None
):
    summary = summarize_text(text.text)
    return {"summary": summary}

#test this endpoint to see if it works as expected
@app.post("/upload-and-summarize/", response_model=SummaryText)
async def upload_and_summarize(file: UploadFile = File(description="Upload file, extract text and summarize."), mode: str = Query(..., enum=["full", "pages", "chapter"]), chapter: str | None = None, pages: str | None = None):
    print("✅ Reached: route entered")
    try:
        file_bytes = await file.read()
        print("✅ Reached: file read")

        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as temp:
            temp.write(file_bytes)
            temp_path = temp.name
        print("✅ Reached: file written to temp:", temp_path)

        text = extract_text_from_pdf(temp_path, mode=mode, chapter=chapter, pages=pages)
        print("✅ Reached: text extracted")
        os.unlink(temp_path)
        print("✅ Reached: temp file deleted")

        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF.")
        else:
            summary = summarize_text(text)
            print("✅ Reached: text summarized")

        with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as summary_file:
            summary_file.write(summary)
            summary_path = summary_file.name
        print("🧪 Summary Path:", summary_path)
        
        return {"summary": summary, "download_link": f"/download-summary/?file={summary_path}"}
    except Exception as e:
        print("🚨 ERROR:", repr(e))
        raise e


@app.get("/download-summary/")
def download_summary(background_tasks: BackgroundTasks, file: str = Query(..., description="Path to the summary file")):
    if not os.path.exists(file):
        raise HTTPException(status_code=404, detail="Summary file not found")
    
    background_tasks.add_task(os.remove, file)
    return FileResponse(file, filename="summary.txt", media_type="text/plain")
    
    
