import requests
import json
import os

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {os.environ['HUGGINGFACE_TOKEN']}"}

def summarize(text):
    try:
        payload = {"inputs": text[:1024]}  # Truncate to avoid token limits
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()[0]['summary_text']
    except Exception as e:
        return f"Summary failed: {str(e)}"

with open("articles.json", "r") as f:
    articles = json.load(f)

for article in articles:
    article["summary"] = summarize(article["content"])

with open("summarized_articles.json", "w") as f:
    json.dump(articles, f)
