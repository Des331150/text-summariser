import os
from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from extraction import extract_text_from_pdf
import tempfile
from schemas import TextInput, SummaryText
from summarize import summarize_text

app = FastAPI()

# @app.post("/uploadfiles/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}

#refactor to include the extraction options as well
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
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF.")
        summary = summarize_text(text)
        print("✅ Reached: text summarized")

        os.unlink(temp_path)
        print("✅ Reached: temp file deleted")

        return {"summary": summary}
    except Exception as e:
        print("🚨 ERROR:", repr(e))
        raise e

