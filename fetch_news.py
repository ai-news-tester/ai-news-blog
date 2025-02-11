import feedparser
import requests
import json
import hashlib
import os
from datetime import datetime

# Configuration
seen_urls = set()

def get_hash(url):
    return hashlib.md5(url.encode()).hexdigest()

def fetch_rss_feeds():
    """Get articles from free RSS feeds"""
    sources = [
        ('MIT Tech Review', 'https://www.technologyreview.com/topic/artificial-intelligence/feed/'),
        ('TechCrunch', 'https://techcrunch.com/category/artificial-intelligence/feed/'),
        ('Arxiv', 'http://export.arxiv.org/rss/cs.AI')
    ]
    
    articles = []
    for name, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:  # Get top 3 per feed
                if get_hash(entry.link) not in seen_urls:
                    articles.append({
                        'title': entry.title,
                        'link': entry.link,
                        'content': entry.get('description', ''),
                        'source': name
                    })
                    seen_urls.add(get_hash(entry.link))
        except:
            pass
    return articles

def fetch_newsapi():
    """NewsAPI - 1 request/day"""
    try:
        url = f"https://newsapi.org/v2/everything?q=AI&language=en&apiKey={os.environ['NEWSAPI_KEY']}&pageSize=5"
        response = requests.get(url)
        return [{
            'title': a['title'],
            'link': a['url'],
            'content': a['content'],
            'source': 'NewsAPI'
        } for a in response.json().get('articles', [])[:3]]  # Top 3
    except:
        return []

# Main execution
all_articles = fetch_rss_feeds() + fetch_newsapi()

# Save results
with open("articles.json", "w") as f:
    json.dump(all_articles[:10], f)  # Max 10 articles/day
