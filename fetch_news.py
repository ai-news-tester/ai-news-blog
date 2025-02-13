import feedparser
import requests
import json
import hashlib
import os
from datetime import datetime

SOURCES = {
    "rss": [
        ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
        ("MIT Tech Review", "https://www.technologyreview.com/topic/artificial-intelligence/feed/"),
        ("Arxiv AI Papers", "http://export.arxiv.org/rss/cs.AI")
    ],
    "api": [
        ("NewsAPI", "https://newsapi.org/v2/everything?q=AI&apiKey={key}&pageSize=5"),
        ("GNews", "https://gnews.io/api/v4/search?q=AI&token={key}&max=3")
    ]
}

seen_urls = set()

def get_hash(url):
    return hashlib.md5(url.encode()).hexdigest()

def fetch_rss():
    articles = []
    for name, url in SOURCES["rss"]:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                if get_hash(entry.link) not in seen_urls:
                    articles.append({
                        "title": entry.title,
                        "link": entry.link,
                        "content": entry.get("description", ""),
                        "date": entry.get("published", datetime.now().isoformat())
                    })
                    seen_urls.add(get_hash(entry.link))
        except Exception as e:
            print(f"RSS Error ({name}): {str(e)}")
    return articles

def fetch_api():
    articles = []
    try:
        # NewsAPI
        newsapi_url = SOURCES["api"][0][1].format(key=os.environ["NEWSAPI_KEY"])
        newsapi_res = requests.get(newsapi_url).json()
        for article in newsapi_res.get("articles", [])[:3]:
            if get_hash(article["url"]) not in seen_urls:
                articles.append({
                    "title": article["title"],
                    "link": article["url"],
                    "content": article["description"],
                    "date": article["publishedAt"]
                })
                
        # GNews
        gnews_url = SOURCES["api"][1][1].format(key=os.environ["GNEWS_TOKEN"])
        gnews_res = requests.get(gnews_url).json()
        for article in gnews_res.get("articles", [])[:2]:
            if get_hash(article["url"]) not in seen_urls:
                articles.append({
                    "title": article["title"],
                    "link": article["url"],
                    "content": article["content"],
                    "date": article["publishedAt"]
                })
    except Exception as e:
        print(f"API Error: {str(e)}")
    return articles

if __name__ == "__main__":
    all_articles = fetch_rss() + fetch_api()
    with open("articles.json", "w") as f:
        json.dump(all_articles[:10], f)  # Max 10 articles/day
