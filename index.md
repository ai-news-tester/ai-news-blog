---
layout: home
title: "AI News Blog"
---

# AI News Blog

Welcome to the AI News Blog! Here you'll find the latest articles on artificial intelligence from various sources.

## Latest Posts

{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%B %d, %Y" }} ({{ post.source }})
{% endfor %}
