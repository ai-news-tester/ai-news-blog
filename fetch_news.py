import feedparser
import requests
import json
import hashlib
import os
from datetime import datetime

# Configuration
MAX_ARTICLES = 15  # Total articles per run
seen_urls = set()

def get_hash(url):
    return hashlib.md5(url.encode()).hexdigest()

# API Sources
def fetch_newsapi():
    """NewsAPI (100 requests/day free)"""
    try:
        response = requests.get(
            f"https://newsapi.org/v2/everything?q=AI&language=en&apiKey={os.environ['NEWSAPI_KEY']}&pageSize=5"
        )
        print(f"NewsAPI response: {response.json()}")
        return [{
            'title': a['title'],
            'link': a['url'],
            'content': a['description'],
            'source': 'NewsAPI'
        } for a in response.json().get('articles', [])[:3]]
    except Exception as e:
        print(f"NewsAPI Error: {str(e)}")
        return []

def fetch_gnews():
    """GNews API (100 requests/day free)"""
    try:
        response = requests.get(
            f"https://gnews.io/api/v4/search?q=AI&lang=en&token={os.environ['GNEWS_TOKEN']}"
        )
        print(f"GNews response: {response.json()}")
        return [{
            'title': a['title'],
            'link': a['url'],
            'content': a['content'],
            'source': 'GNews'
        } for a in response.json().get('articles', [])[:3]]
    except Exception as e:
        print(f"GNews Error: {str(e)}")
        return []

def fetch_guardian():
    """The Guardian API (5k requests/month free)"""
    try:
        response = requests.get(
            f"https://content.guardianapis.com/search?q=AI&api-key={os.environ['GUARDIAN_KEY']}&show-fields=body"
        )
        print(f"Guardian response: {response.json()}")
        return [{
            'title': r['webTitle'],
            'link': r['webUrl'],
            'content': r['fields']['body'] if 'fields' in r else '',
            'source': 'The Guardian'
        } for r in response.json().get('response', {}).get('results', [])[:3]]
    except Exception as e:
        print(f"Guardian Error: {str(e)}")
        return []

# RSS Sources
RSS_FEEDS = [
    ('TechCrunch AI', 'https://techcrunch.com/category/artificial-intelligence/feed/'),
    ('MIT Tech Review', 'https://www.technologyreview.com/topic/artificial-intelligence/feed/'),
    ('Arxiv AI Papers', 'http://export.arxiv.org/rss/cs.AI'),
    ('Wired AI', 'https://www.wired.com/feed/tag/ai/latest/rss'),
    ('VentureBeat AI', 'https://venturebeat.com/category/ai/feed/')
]

def fetch_rss():
    articles = []
    for name, url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            print(f"Parsing RSS feed: {name}")
            for entry in feed.entries[:5]:
                if get_hash(entry.link) not in seen_urls:
                    articles.append({
                        'title': entry.title,
                        'link': entry.link,
                        'content': entry.get('description', ''),
                        'source': name
                    })
                    seen_urls.add(get_hash(entry.link))
        except Exception as e:
            print(f"RSS Error ({name}): {str(e)}")
    return articles

# Main execution
all_articles = []
all_articles += fetch_newsapi()
all_articles += fetch_gnews()
all_articles += fetch_guardian()
all_articles += fetch_rss()

print(f"Total articles fetched: {len(all_articles)}")
print(f"Articles: {all_articles}")

# Save results
with open("articles.json", "w") as f:
    json.dump(all_articles[:MAX_ARTICLES], f)
