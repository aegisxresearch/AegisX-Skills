# Programmatic SEO & Web Metadata

## Goal
Make public content discoverable without exposing private, duplicate, low-value, or unbounded pages.

## URL Contract
Define one canonical URL per indexable resource. Normalize trailing slashes, casing, query parameters, locale, and pagination. Redirect obsolete URLs intentionally and preserve query parameters only when they affect content.

## Metadata Example
```typescript
export function buildArticleMetadata(article: Article): Metadata {
  const canonical = new URL(`/articles/${article.slug}`, 'https://example.com');
  return {
    title: article.title,
    description: article.summary.slice(0, 160),
    alternates: { canonical: canonical.toString() },
    openGraph: { type: 'article', url: canonical, title: article.title },
    robots: article.isPublic ? { index: true, follow: true } : { index: false, follow: false },
  };
}
```
Validate title and description length as guidance, not as a guarantee of search snippet behavior.

## Structured Data
Use JSON-LD matching visible page content. Validate required fields and avoid marking up hidden, misleading, or user-generated claims without moderation.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Example title",
  "datePublished": "2026-01-15T10:00:00Z",
  "author": { "@type": "Person", "name": "Example author" }
}
```
Escape serialized values safely and do not insert untrusted strings as raw HTML.

## Crawl Controls
- `robots.txt` controls crawling, not access control.
- Authentication and authorization must protect private content.
- Sitemap entries should return indexable `200` pages.
- Exclude search result pages, infinite filter combinations, and duplicate tracking URLs.
- Keep sitemap files within protocol limits and split them predictably.

## Rendering
Public content must be present in server-rendered HTML or reliably rendered before indexing. Provide meaningful loading and error states that do not replace the content with an empty shell.

## Internationalization
Use stable locale prefixes or subdomains, `hreflang` alternates, translated metadata, and a self-referencing canonical. Never automatically redirect crawlers based only on IP.

## Monitoring
Track crawl errors, index coverage, broken canonical links, sitemap freshness, structured-data errors, response status, and template-level traffic changes. Tie alerts to releases.

## Checklist
- [ ] Public/private boundary is enforced independently of SEO controls.
- [ ] Canonicals are absolute, stable, and self-consistent.
- [ ] Metadata is unique for meaningful pages.
- [ ] Structured data matches visible content.
- [ ] Sitemap contains only eligible URLs.
- [ ] Robots rules do not accidentally block assets or public pages.
- [ ] Pagination and faceted navigation have an explicit policy.
- [ ] Redirects and 404/410 behavior are tested.
- [ ] Core Web Vitals are monitored in field data.

## References
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/crawling-indexing/robots/intro
- https://schema.org/docs/gs.html

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
