# Korea Public Benefit Brief — release rules

## Legacy GitHub Pages is the production artifact

GitHub Pages serves the pre-rendered `gh-pages` branch, not `main`. A source commit is not a publication. A release is complete only after the static page is pushed, publicly reachable, and passes the public verifier.

## Required reader-first ending

Every published post must end in this order when evidence exists:

```text
결론 또는 후속 확인 포인트
→ FAQ
→ 전문용어 쉽게 풀어쓰기
→ 연구/핵심 데이터 정리
→ 공식 출처와 확인 근거
→ 이 글과 함께 읽어보세요
```

Never invent research, terms, data, or links to fill an empty block. Keep an internal omission reason only when a non-applicable block must be absent.

## Related-reading release gate

`이 글과 함께 읽어보세요` is mandatory for every public post.

1. Use matching tag/category posts first.
2. If no match exists, use up to three already-public recent posts as fallback.
3. Do not rely on the Liquid layout alone when generating legacy static HTML. After rendering each new page, run:

```bash
python scripts/ensure-related-posts.py \
  _posts/YYYY-MM-DD-slug.md \
  ../korea-public-benefit-brief-pages/<category-path>/YYYY/MM/DD/slug/index.html
```

4. Run `scripts/verify-public-benefit-post.py` locally and publicly. Both `SECTION_이 글과 함께 읽어보세요` and `RELATED_POST_LINK` must PASS.
5. If either check fails, do not push `gh-pages`, announce publication, or send the internal newsletter.

## Safety and evidence

- Preserve the public-policy evidence boundary: do not add health, eligibility, benefit, or timing claims beyond official sources.
- Use only public, actually deployed related-post URLs.
- Do not commit credentials, `.env`, token files, browser sessions, cron data, or system backups.
