---
layout: page
title: 생활정책·혜택
description: "시민의 일상에 필요한 정책·복지·안전·건강·주거·교육 정보를 공식 출처로 확인해 안내합니다."
permalink: /living-policy/
---

<p class="eyebrow">FOR CITIZENS</p>
# 생활정책·혜택

시민의 일상에 필요한 정책·복지·안전·건강·주거·교육 정보를 공식 원문 기준으로 정리합니다. 글을 읽은 뒤에는 실제 대상, 기한, 신청 경로를 반드시 원문에서 다시 확인하세요.

<div class="archive-posts">
{% assign living_count = 0 %}
{% for post in site.posts %}
  {% unless post.categories contains 'funding' %}
  <article class="post-item">
    {% if post.image %}<a class="post-thumb-link" href="{{ post.url | relative_url }}" aria-label="{{ post.title }}"><img src="{{ post.image | relative_url }}" alt="{{ post.image_alt | default: post.title }}" loading="lazy"></a>{% endif %}
    <div class="post-copy"><time>{{ post.date | date: "%Y.%m.%d" }}</time><h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2><p>{{ post.excerpt | strip_html | truncate: 150 }}</p></div>
  </article>
  {% assign living_count = living_count | plus: 1 %}
  {% endunless %}
{% endfor %}
</div>

{% if living_count == 0 %}
<p class="empty-state">검증을 마친 생활정책·혜택 브리프를 준비하고 있습니다.</p>
{% endif %}
