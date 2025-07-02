from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str):
    result = summarizer(text, min_length=30 ,do_sample=True)
    return result[0]["summary_text"]