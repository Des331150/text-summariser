import os
from fastapi import FastAPI, File, UploadFile
from extraction import extract_text
import tempfile


app = FastAPI()

@app.post("/uploadfiles/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@app.post("/extract/")
async def extract_text(file: UploadFile = File(description="Extract files.")):
    file_bytes = await file.read()
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    text = extract_text(tmp_path)
    os.unlink(tmp_path)
    return {"text": text}
