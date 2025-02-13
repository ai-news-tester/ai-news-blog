---
layout: home
---

# Latest AI News

{% for post in site.posts %}
- [{{ post.title }}]({{ post.url }})
{% endfor %}
