import json
from datetime import datetime
import os
import re

def sanitize_filename(title):
    return re.sub(r'[^a-zA-Z0-9-]', '', title.replace(' ', '-').lower())[:50]

with open("summarized_articles.json", "r") as f:
    articles = json.load(f)

os.makedirs("_posts", exist_ok=True)

for article in articles:
    date_str = datetime.now().strftime('%Y-%m-%d')
    clean_title = sanitize_filename(article['title'])
    filename = f"_posts/{date_str}-{clean_title}.md"
    
    content = f"""---
title: "{article['title']}"
date: {date_str}
---

{article['summary']}

[Read original article]({article['link']})
"""
    with open(filename, "w") as f:
        f.write(content)
