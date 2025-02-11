import feedparser
import json

# Fetch AI news from Google RSS
feed_url = "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-US&gl=US&ceid=US:en"
feed = feedparser.parse(feed_url)
articles = []

for entry in feed.entries[:5]:  # Get top 5 articles
    articles.append({
        "title": entry.title,
        "link": entry.link,
        "content": entry.description
    })

# Save articles to a JSON file
with open("articles.json", "w") as f:
    json.dump(articles, f)
