from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str):
    result = summarizer(text,do_sample=True)
    return result[0]["summary_text"]