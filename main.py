import os
from fastapi import FastAPI, File, UploadFile
from extraction import extract_text_from_pdf
import tempfile
from schemas import TextInput, SummaryText
from summarize import summarize_text

app = FastAPI()

@app.post("/uploadfiles/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

#refactor to include the extraction options as well
@app.post("/extract/")
async def extract_text(file: UploadFile = File(description="Extract files.")):
    file_bytes = await file.read()
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    text = extract_text_from_pdf(tmp_path)
    os.unlink(tmp_path)
    return {"text": text}

@app.post("/summarize/", response_model=SummaryText)
async def summarize_route(text: TextInput):
    summary = summarize_text(text.text)
    return {"summary": summary}

#test this endpoint to see if it works as expected
@app.post("/upload-and-summarize/", response_model=SummaryText)
async def upload_and_summarize(file: UploadFile = File(description="Upload file, extract text and summarize.")):
    file_bytes = await file.read()
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as temp:
        temp.write(file_bytes)
        temp_path = temp.name
    text = await extract_text_from_pdf(temp_path)
    summary = summarize_text(text)
    os.unlink(temp_path)
    return {"summary": summary}