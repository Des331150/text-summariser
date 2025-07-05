from pydantic import BaseModel

class TextInput(BaseModel):
    text: str

class SummaryText(BaseModel):
    summary: str
    download_link: str 