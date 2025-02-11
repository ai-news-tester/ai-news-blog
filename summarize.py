import requests
import json
import os

# Hugging Face Summarization API
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {os.environ['HUGGINGFACE_TOKEN']}"}

def summarize(text):
    payload = {"inputs": text, "parameters": {"max_length": 150}}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]['summary_text']

# Load fetched articles
with open("articles.json", "r") as f:
    articles = json.load(f)

# Summarize each article
for article in articles:
    summary = summarize(article["content"])
    article["summary"] = summary

# Save summaries
with open("summarized_articles.json", "w") as f:
    json.dump(articles, f)
