from pydantic import BaseModel

class TextInput(BaseModel):
    text: str

class SummaryText(BaseModel):
    status: str
    summary: str
    download_link: str 