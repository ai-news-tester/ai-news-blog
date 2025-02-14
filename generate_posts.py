import json
from datetime import datetime
import os
import re

def sanitize_title(title):
    return re.sub(r'[^a-zA-Z0-9-]', '', title.lower())[:50]

with open("articles.json", "r") as f:
    articles = json.load(f)

print(f"Loaded {len(articles)} articles from articles.json")

os.makedirs("_posts", exist_ok=True)

for article in articles:
    date_str = datetime.now().strftime('%Y-%m-%d')
    clean_title = sanitize_title(article['title'])
    filename = f"_posts/{date_str}-{clean_title}.md"
    
    content = f"""---
title: "{article['title']}"
date: {date_str}
source: {article.get('source', '')}
---

{article['content'][:1000]}... [Read full article]({article['link']})
"""
    print(f"Generating post: {filename}")
    with open(filename, "w") as f:
        f.write(content)

print("All posts generated successfully.")
