# generate_posts.py
import json
import os
import re
from datetime import datetime

def clean_filename(title):
    return re.sub(r'[^\w-]', '', title.lower())[:40]  # Reduced length

# Inside the loop:
filename = f"_posts/{date}-{clean_filename(article['title']}.md"
with open("articles.json") as f:
    articles = json.load(f)

os.makedirs("_posts", exist_ok=True)

for article in articles:
    try:
        date = datetime.fromisoformat(article["date"]).strftime("%Y-%m-%d")
    except:
        date = datetime.now().strftime("%Y-%m-%d")
        
    filename = f"_posts/{date}-{clean_filename(article['title'])}.md"
    
    content = f"""---
title: "{article['title']}"
date: {date}
source: {article.get('source', 'RSS Feed')}
---

{article['content'][:500]}... [Read full article]({article['link']})
"""
    with open(filename, "w") as f:
        f.write(content)
