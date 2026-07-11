# 4TENLAB Content Funnel + AEO/GEO Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a staged content funnel where one GitHub Pages blog post becomes search/AEO/GEO traffic, email subscribers, newsletter delivery, SNS distribution, community touchpoints, and eventually paid products.

**Architecture:** Keep GitHub Pages as the public content hub. Add structured metadata, JSON-LD, RSS/sitemap/indexing automation, then subscription + Resend newsletter flow, then SNS/community automation. Avoid overbuilding: validate each layer with simple metrics before expanding.

**Tech Stack:** GitHub Pages/Jekyll-style static site, `gh-pages` direct static deploy, RSS/XML, JSON-LD, OpenGraph/Twitter cards, Google Search Console/Bing Webmaster, Resend API, small subscriber store later (Google Sheet/Supabase/Cloudflare D1), Hermes cron, GitHub Actions or external ping where credentials permit.

---

## Strategic Phasing

## 단기 계획: 0~4주 — 검색/신뢰/구독 기반 만들기

### 목표

- 블로그가 검색·AI 답변·링크 공유에서 제대로 읽히게 만든다.
- 구독 전환 전 단계까지 신뢰 기반을 정리한다.
- 유료화가 아니라 “반복 구독 가능한 정보 자산”을 만든다.

### 핵심 산출물

1. **AEO/GEO 기술 기반**
   - `description` front matter를 모든 post에 필수화.
   - `canonical` URL 추가.
   - `og:url`, `og:site_name`, `article:published_time`, `article:modified_time` 추가.
   - `twitter:title`, `twitter:description` 추가.
   - `JSON-LD` 추가:
     - homepage: `WebSite`, `Organization`
     - about: `AboutPage`, `Organization`
     - post: `BlogPosting`, `FAQPage` when FAQ exists, `BreadcrumbList`
   - `robots.txt`에 sitemap 위치 명시.
   - `sitemap.xml`에 최신 post 포함 확인.

2. **인덱싱 자동화 준비**
   - Google Search Console 등록은 계정 소유권이 필요하므로 대표님 계정에서 1회 등록 필요.
   - Bing Webmaster도 1회 등록 권장.
   - GitHub Pages 사이트맵 URL:
     - `https://ai4tenlab.github.io/korea-public-benefit-brief/sitemap.xml`
   - RSS URL:
     - `https://ai4tenlab.github.io/korea-public-benefit-brief/feed.xml`
   - 자동화는 먼저 “sitemap ping + 검증 로그”부터 시작한다.
   - Google Indexing API는 일반 블로그 URL에는 공식적으로 제한적이므로, Search Console sitemap 제출/갱신 중심으로 접근한다.

3. **구독 전환 준비**
   - 글 하단 CTA:
     - “이런 정책 브리프를 이메일로 받아보세요.”
   - 아직 개인정보 수집 전에는 구독 폼 대신 내부 테스트 CTA/설계만 둘 수 있다.
   - 구독 폼을 넣을 경우 필수 문구:
     - 수신 목적
     - 수신 빈도
     - 구독 취소 가능
     - 개인정보 최소 수집

4. **뉴스레터 품질 고정**
   - 현재 `4TENLAB Lucky` Resend 발신자 유지.
   - 뉴스레터형 HTML 디자인 유지.
   - 발행 후 내부 테스트 이메일은 계속 발송.

### 단기 KPI

| 항목 | 목표 |
|---|---:|
| 발행 성공률 | 95%+ |
| URL/썸네일/OG/RSS 검증 | 매 글 100% |
| JSON-LD 오류 | 0개 목표 |
| Search Console 색인 시작 | 확인 |
| 내부 이메일 한글/디자인 오류 | 0개 |

---

## 중기 계획: 1~3개월 — 구독/메일링/SNS 자동화 MVP

### 목표

- 익명 방문자를 이메일 구독자로 전환한다.
- 블로그 원문을 뉴스레터와 SNS로 재가공한다.
- 채널별 성과를 측정한다.

### 핵심 산출물

1. **구독 기능 MVP**
   - 선택지 A: Google Sheet + Apps Script/Webhook
   - 선택지 B: Supabase table + Edge Function
   - 선택지 C: Cloudflare Worker + D1
   - 추천: 초기에는 Supabase 또는 Cloudflare D1. 단, 가장 빠른 MVP는 Google Sheet.

2. **구독/취소 기능**
   - `/subscribe/` landing page.
   - 이메일 입력.
   - double opt-in 또는 최소 확인 메일.
   - unsubscribe token 생성.
   - `/unsubscribe/?token=...` 처리.
   - 발송 로그 저장.

3. **메일링 자동화**
   - 새 글 발행 후:
     - 내부 테스트 발송
     - 문제 없으면 구독자 발송
   - 발송 전 체크:
     - URL 200
     - RSS 갱신
     - 썸네일 200
     - JSON-LD valid enough
     - unsubscribe 링크 포함

4. **SNS 원소스 멀티유즈 v1**
   - 블로그 원문 → 채널별 초안 생성:
     - Telegram: 요약 + 링크
     - X/Threads: 3~5문장 스레드
     - LinkedIn: 전문적 해설형
   - 초기에는 자동 게시보다 “자동 초안 생성 + 승인 후 게시” 권장.

5. **커뮤니티 실험**
   - 처음부터 큰 커뮤니티를 만들지 않는다.
   - Telegram 채널 또는 소규모 뉴스레터 회신 기반으로 반응을 본다.

### 중기 KPI

| 항목 | 목표 |
|---|---:|
| 이메일 구독 전환율 | 방문자 대비 1~3% 시작 |
| 뉴스레터 오픈율 | 30%+ 목표 |
| 뉴스레터 클릭률 | 3~8% 목표 |
| 구독 취소율 | 낮게 유지, 원인 기록 |
| SNS 초안 재사용률 | 글당 2채널 이상 |

---

## 장기 계획: 3~12개월 — 브랜드/커뮤니티/수익화

### 목표

- 콘텐츠 신뢰를 관계 자산으로 전환한다.
- 뉴스레터/커뮤니티/리포트/교육/컨설팅으로 수익화를 실험한다.
- 4TENLAB 브랜드의 owned media funnel을 만든다.

### 핵심 산출물

1. **프리미엄 뉴스레터**
   - 무료: 공익정책 브리프 요약.
   - 유료: 주간 심층 리포트, 체크리스트, 정책 캘린더, 신청 가이드.

2. **주제별 브랜드 라인**
   - 공익정책 브리프
   - AI시민연구소
   - 교육채널오름
   - AllWeatherOS
   - 기록하는신문/ArchiverNews

3. **커뮤니티화**
   - 이메일 구독자 중 참여도가 높은 사람을 커뮤니티로 초대.
   - 커뮤니티는 토론보다 “질문 수집 → 다음 콘텐츠 반영” 구조가 먼저.

4. **유료 상품 후보**
   - 월간 정책/복지 캘린더 PDF.
   - 소상공인/가정/청년 맞춤 정책 체크리스트.
   - AI 리터러시 교육 콘텐츠.
   - 공공정보 AEO/GEO 리포트.

### 장기 KPI

| 항목 | 목표 |
|---|---:|
| 구독자 수 | 1차 100명, 2차 1,000명 |
| 반복 오픈 독자 | 30%+ |
| 유료 전환 | 검증 후 1~5% |
| 커뮤니티 활성 | 주간 질문/피드백 수 |
| 원소스 멀티유즈 | 글 1개당 5개 산출물 |

---

# CTO Implementation Plan

## Task 1: Metadata front matter standardize

**Objective:** Make every post provide machine-readable title/description/image metadata.

**Files:**
- Modify: `_posts/*.md`
- Modify: `_layouts/default.html`

**Add/require front matter:**

```yaml
title: "..."
description: "검색·SNS·뉴스레터에 표시될 80~160자 요약"
date: 2026-07-11 05:30:00 +0900
categories: [benefit]
author: "대한민국 공익정책 브리프"
image: "/assets/images/thumbnails/YYYY-MM-DD-slug.png"
image_alt: "주제 설명 썸네일"
last_modified_at: 2026-07-11 05:30:00 +0900
```

**Verification:**

```bash
python scripts/verify-post-metadata.py _posts/YYYY-MM-DD-slug.md
```

Expected: required fields present.

---

## Task 2: Add canonical/OG/Twitter metadata

**Objective:** Improve link previews and search clarity.

**Files:**
- Modify: `_layouts/default.html`

**Implementation concept:**

```html
<link rel="canonical" href="{{ page.url | absolute_url }}">
<meta property="og:url" content="{{ page.url | absolute_url }}">
<meta property="og:site_name" content="{{ site.title }}">
<meta name="twitter:title" content="{% if page.title %}{{ page.title }}{% else %}{{ site.title }}{% endif %}">
<meta name="twitter:description" content="{{ page.description | default: site.description }}">
```

For posts:

```html
{% if page.layout == 'post' %}
<meta property="article:published_time" content="{{ page.date | date_to_xmlschema }}">
{% if page.last_modified_at %}<meta property="article:modified_time" content="{{ page.last_modified_at | date_to_xmlschema }}">{% endif %}
{% endif %}
```

**Verification:** public post HTML contains canonical, og:url, twitter fields.

---

## Task 3: Add JSON-LD templates

**Objective:** Make posts understandable to search engines and AI answer systems.

**Files:**
- Create: `_includes/jsonld.html`
- Modify: `_layouts/default.html`

**Types:**

| Page | JSON-LD |
|---|---|
| Home | `WebSite`, `Organization` |
| About | `AboutPage`, `Organization` |
| Post | `BlogPosting`, `BreadcrumbList`, optional `FAQPage` |

**Important:** FAQPage should only be emitted when FAQs can be extracted reliably or supplied as front matter/data. In phase 1, use `BlogPosting` and `BreadcrumbList`; add `FAQPage` after parser is stable.

**Verification:**

- View source contains `<script type="application/ld+json">`.
- JSON parses with Python `json.loads` after Liquid build/static output.

---

## Task 4: Add sitemap/robots verification

**Objective:** Ensure crawlers can find new content.

**Files:**
- Modify: `robots.txt`
- Verify: `sitemap.xml`
- Verify: `feed.xml`

**robots.txt should include:**

```text
User-agent: *
Allow: /
Sitemap: https://ai4tenlab.github.io/korea-public-benefit-brief/sitemap.xml
```

**Verification:**

```bash
python scripts/verify-public-indexing.py
```

Checks:
- homepage 200
- sitemap 200
- feed 200
- latest post URL included in sitemap/feed

---

## Task 5: Search indexing operations

**Objective:** Prepare safe automation around Google/Bing indexing.

**Manual prerequisites:**

1. Add `https://ai4tenlab.github.io/korea-public-benefit-brief/` to Google Search Console.
2. Verify ownership using HTML file, meta tag, DNS, or GitHub Pages-supported method.
3. Submit sitemap: `/sitemap.xml`.
4. Add same site to Bing Webmaster Tools and submit sitemap.

**Automation boundary:**

- Do not claim automatic Google indexing for every normal blog URL.
- Google Indexing API is officially limited for specific job/live-stream use cases; for normal blog pages, rely on sitemap submission, RSS, internal links, and Search Console monitoring.
- If credentials become available later, automate sitemap resubmission/check logs, not aggressive URL spam.

---

## Task 6: Subscription MVP design

**Objective:** Convert readers to owned audience.

**Files likely later:**
- Create: `subscribe.md`
- Create: `unsubscribe.md`
- Create: `assets/js/subscribe.js` if static form is used
- External: Supabase/Cloudflare Worker/Google Apps Script endpoint

**Minimum data model:**

```text
email
status: pending|active|unsubscribed
source_url
created_at
confirmed_at
unsubscribed_at
unsubscribe_token_hash
last_sent_at
```

**Legal/trust requirements:**

- 수신 목적 표시.
- 수신 빈도 표시.
- 언제든 구독 취소 가능.
- 개인정보 최소 수집.
- 발송 메일마다 unsubscribe 링크 포함.

---

## Task 7: Newsletter + SNS one-source multi-use

**Objective:** Reuse each post into multiple channels without making spam.

**Post-publish package:**

```text
1. Blog original
2. Resend newsletter
3. Telegram summary
4. X/Threads short thread
5. LinkedIn professional note
6. Community discussion question
```

**Initial rule:** auto-generate drafts, but do not auto-post to all SNS until channel quality is reviewed.

---

## Risks / Tradeoffs

| Risk | Mitigation |
|---|---|
| Over-automation makes AI-smelling content | Keep human/expert-reviewed tone and channel-specific rewrites |
| Search indexing expectations too high | Use sitemap/RSS/Search Console, avoid false “instant indexing” promises |
| 개인정보/스팸 리스크 | double opt-in, unsubscribe, clear sender identity, minimal data |
| Tool sprawl | Start with GitHub Pages + Resend + one subscriber store |
| SNS spam perception | Draft-first, channel-specific language, low frequency |

---

## Recommended immediate next implementation order

1. Add canonical/OG/Twitter metadata improvements.
2. Add JSON-LD `BlogPosting` + `WebSite` + `Organization`.
3. Verify `robots.txt`, `sitemap.xml`, `feed.xml`.
4. Create `verify-public-indexing.py` ad-hoc/permanent verifier.
5. Ask user to register Google Search Console/Bing Webmaster once.
6. Add non-invasive newsletter CTA below posts.
7. Design subscription MVP with unsubscribe before collecting public emails.

---

## Acceptance Criteria for Phase 1

- [ ] Every public post has title, description, image, image_alt.
- [ ] Public HTML includes canonical, OG, Twitter metadata.
- [ ] Public HTML includes valid JSON-LD for posts.
- [ ] sitemap/feed/robots are reachable and include latest post.
- [ ] Post-publish verifier reports metadata + indexing readiness.
- [ ] User has a clear Search Console/Bing setup checklist.
- [ ] No subscriber data is collected until unsubscribe/privacy flow is ready.
