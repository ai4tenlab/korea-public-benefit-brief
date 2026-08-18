---
layout: page
title: 정책자금
description: "소상공인·중소기업·예비창업자가 정책자금과 창업지원 공고를 공식 출처에서 확인하는 방법과 최신 브리프를 안내합니다."
permalink: /policy-funding/
---

<p class="eyebrow">FOR BUSINESS</p>
# 정책자금

소상공인·1인기업·예비창업자·중소기업을 위한 융자·지원금·보증 정책을 다룹니다. 정책자금은 보조금, 융자, 보증, 이차보전, 바우처처럼 지원 방식이 다르므로 **대상·업력·업종·지역·마감일·신청 경로**를 공식 공고에서 먼저 확인해야 합니다.

## 최신 정책자금 브리프

<div class="archive-posts">
{% assign funding_count = 0 %}
{% for post in site.posts %}
  {% if post.categories contains 'funding' %}
  <article class="post-item">
    {% if post.image %}<a class="post-thumb-link" href="{{ post.url | relative_url }}" aria-label="{{ post.title }}"><img src="{{ post.image | relative_url }}" alt="{{ post.image_alt | default: post.title }}" loading="lazy"></a>{% endif %}
    <div class="post-copy"><time>{{ post.date | date: "%Y.%m.%d" }}</time><h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2><p>{{ post.excerpt | strip_html | truncate: 150 }}</p></div>
  </article>
  {% assign funding_count = funding_count | plus: 1 %}
  {% endif %}
{% endfor %}
</div>

{% if funding_count == 0 %}
<div class="empty-state"><strong>공식 공고를 검증하고 있습니다.</strong><p>대상·기한·신청 경로를 확인할 수 있는 정책자금 공고만 발행합니다. 확인 전 발표성 자료나 일반 금융 기사는 이 목록에 섞지 않습니다.</p></div>
{% endif %}

## 매일 확인하는 정책자금 분야

### 창업·초기기업
예비창업, 창업기업 사업화, 창업공간, 멘토링, 초기 자금 관련 공고를 다룹니다.

### 소상공인·자영업
경영안정, 재기, 상권·디지털 전환, 판로와 비용 부담 완화 관련 지원을 다룹니다.

### 중소기업 운영·시설자금
운전자금, 시설투자, 정책융자, 이차보전과 기업 금융 지원 공고를 구분해 설명합니다.

### 보증·기술·수출
신용보증·기술보증, R&D, 수출, 판로, 고용 지원처럼 심사와 자격 조건을 함께 봐야 하는 공고를 다룹니다.

### 지역별 지원사업
지자체 소재지·사업장 요건이 중요한 지역 한정 사업은 전국 공고와 구분해 안내합니다.

## 공식 출처 허브

정책자금 글은 아래 기관의 공고·신청 안내·보도자료를 우선 확인합니다. 같은 사업이라도 실제 신청 자격과 접수 상태는 각 공고 원문이 최종 기준입니다.

- [기업마당](https://www.bizinfo.go.kr/): 중앙부처·지자체·공공기관의 중소기업 지원사업 공고 확인
- [K-Startup 창업지원포털](https://www.k-startup.go.kr/web): 예비창업자·창업기업 지원사업과 창업 정보 확인
- [소상공인시장진흥공단](https://www.semas.or.kr/): 소상공인 지원사업과 정책자금 안내 확인
- [중소벤처기업진흥공단](https://www.kosmes.or.kr/): 중소기업 정책자금·성장지원 정보 확인
- [기술보증기금](https://www.kibo.or.kr/): 기술보증과 기술평가 기반 금융지원 안내 확인
- [신용보증기금](https://www.kodit.co.kr/): 신용보증과 기업금융 지원 안내 확인
- [중소벤처기업부](https://www.mss.go.kr/): 중소기업·소상공인·창업 정책의 공식 발표와 제도 안내 확인

## 읽는 방법

1. **지원 유형을 먼저 봅니다.** 보조금인지, 상환이 필요한 융자인지, 보증인지, 이차보전인지 구분합니다.
2. **대상 조건을 확인합니다.** 지역·업종·업력·매출·고용·대표자 요건과 제외 업종을 봅니다.
3. **공식 링크에서 최종 확인합니다.** 글의 요약은 판단을 돕는 안내이며, 실제 신청 전에는 원문 공고와 접수 시스템을 다시 확인해야 합니다.
4. **마감·변경 정보를 확인합니다.** 예산 소진, 연장, 접수 종료는 공고 이후에도 바뀔 수 있습니다.

## 편집·검증 기준

새 정책자금 브리프는 최소 두 개의 공식 확인 지점을 확보하고, 지원 금액·대상·기한·신청 경로처럼 중요한 사실에는 본문 안에서 직접 공식 링크를 연결합니다. 대상, 기간, 신청 경로를 확인할 수 없는 발표성 자료는 발행하지 않습니다.
