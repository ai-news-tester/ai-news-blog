import feedparser
import json

feed_url = "https://news.google.com/rss/search?q=artificial+intelligence+OR+machine+learning&hl=en-US&gl=US&ceid=US:en"
feed = feedparser.parse(feed_url)
articles = []

for entry in feed.entries[:5]:  # Get top 5 articles
    articles.append({
        "title": entry.title,
        "link": entry.link,
        "content": entry.get("description", "No content available")
    })

with open("articles.json", "w") as f:
    json.dump(articles, f)
