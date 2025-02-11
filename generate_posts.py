import json
from datetime import datetime
import os

# Load summarized articles
with open("summarized_articles.json", "r") as f:
    articles = json.load(f)

# Create a folder for posts
os.makedirs("posts", exist_ok=True)

# Generate markdown files for Jekyll
for article in articles:
    filename = f"posts/{datetime.now().strftime('%Y-%m-%d')}-{article['title'][:20].replace(' ', '-').lower()}.md"
    content = f"""---
title: "{article['title']}"
date: {datetime.now().strftime('%Y-%m-%d')}
---

{article['summary']}

[Read original article]({article['link']})
"""
    with open(filename, "w") as f:
        f.write(content)
