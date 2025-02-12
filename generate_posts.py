import json
from datetime import datetime
import os
import re

def sanitize_title(title):
    return re.sub(r'[^a-zA-Z0-9-]', '', title.lower())[:50]

with open("articles.json", "r") as f:
    articles = json.load(f)

os.makedirs("_posts", exist_ok=True)

for article in articles:
    # Use publication date from feed if available
    date_str = article.get('date', datetime.now().strftime('%Y-%m-%d'))
    clean_title = sanitize_title(article['title'])
    filename = f"_posts/{date_str}-{clean_title}.md"
    
    content = f"""---
title: "{article['title']}"
date: {date_str}
---

{article['content']}

[Read full article]({article['link']})
"""
    with open(filename, "w") as f:
        f.write(content)
