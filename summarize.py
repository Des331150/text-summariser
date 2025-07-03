from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str):
    truncated_text = text[:1000]
    result = summarizer(truncated_text,do_sample=True)
    return result[0]["summary_text"]