#!/usr/bin/env python3
"""Add per-skill Pitfalls and Trade-off sections to skill guides.

Inserts:
1. '## Kesalahan Umum / Pitfalls' — 3-4 skill-specific bullets
2. '## Trade-off dan Kapan Tidak Pakai' — 2-3 skill-specific bullets

Both are inserted before the References section if present, otherwise
before the watermark footer at the end of the file.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

# skill_id -> (pitfalls bullets, tradeoff bullets)
CONTENT: dict[str, tuple[list[str], list[str]]] = {    "animation-performance-guide": (
        ["Animating `width`/`height`/`top`/`left` — triggers layout + paint on every frame.",
         "Animating `filter` or `box-shadow` — expensive to repaint; prefer composited properties.",
         "Forgetting `prefers-reduced-motion` — users with vestibular disorders get nauseous.",
         "Testing only on a fast machine — always profile on the slowest target device."],
        ["GPU compositing helps, but memory bandwidth is still finite — batch effects.",
         "CSS animations are simpler, JS (requestAnimationFrame) gives control — pick by need.",
         "Not every animation needs 60fps; 30fps is fine for subtle transitions and saves battery."],
    ),
    "anti-hallucinated-dependencies": (
        ["Adding a package without checking it exists on the registry — a `pip install` typo fails at build time.",
         "Trusting a package name from an LLM suggestion without verifying the real API surface.",
         "Copying a version pin from a random blog post — the version may not exist or be yanked.",
         "Forgetting to commit the lockfile — builds become non-reproducible."],
        ["Lockfiles add merge noise; small prototypes may not need them yet.",
         "Verifying every transitive dependency is costly — focus on direct deps + known vuln feeds.",
         "A monorepo may centralize deps; per-package lockfiles can fight that workflow."],
    ),
    "anti-slop-agent-output": (
        ["Reporting 'done' without listing what was changed and what was tested.",
         "Stating assumptions as facts ('the endpoint is slow') without measurements.",
         "Omitting risks or known limitations to look more competent.",
         "Writing vague summaries instead of file-level, verifiable change lists."],
        ["Short reports are faster to read but may hide context — match depth to audience.",
         "Forcing a report format on trivial one-line fixes adds ceremony.",
         "Machine-readable output helps pipelines but hurts human debugging — use both."],
    ),
    "anti-slop-documentation": (
        ["Claiming something 'works' without a runnable example or test.",
         "Copying examples from other projects without adapting them to your stack.",
         "Using 'obviously' and 'simply' — hides real complexity from readers.",
         "Documenting the happy path only, never failure modes or limits."],
        ["Deep docs cost time to write and maintain — prioritize public APIs and onboarding.",
         "Code comments vs docs: comments explain 'why', docs explain 'how to use'.",
         "Generated docs drift when code changes — keep a review step in CI."],
    ),
    "anti-slop-test-quality": (
        ["Asserting implementation details instead of behavior — tests break on refactors.",
         "Mocking everything, including the code under test's own collaborators.",
         "Writing tests that pass without ever failing — no assertion strength check.",
         "Ignoring flakey tests instead of fixing the root cause."],
        ["Heavy integration tests catch more but are slower and flakier — balance with unit tests.",
         "Property-based tests find edge cases but need good generators — not always worth it.",
         "100% coverage is a target, not a quality metric — mutation testing is stronger."],
    ),
    "api-design-patterns": (
        ["Breaking changes on every release — no versioning strategy.",
         "Exposing internal database IDs in URLs without considering enumeration.",
         "Ignoring pagination — unbounded responses kill mobile clients and DBs.",
         "Rate limiting only at the gateway — bypassable by direct service access."],
        ["REST is not the only option — GraphQL or gRPC may fit better for some clients.",
         "Strict contracts help stability but slow iteration — version early, not late.",
         "Pagination with deep offsets is slow on large tables — consider keyset pagination."],
    ),
    "api-observability": (
        ["Logging secrets or full payloads — a compliance and security incident waiting.",
         "No correlation ID — cannot trace a request across services.",
         "Alerting on every metric — alert fatigue kills the on-call rotation.",
         "Metrics without SLOs — you cannot know when to page."],
        ["High-cardinality logging is expensive — sample debug logs in production.",
         "Tracing every request adds overhead — use sampling at high traffic.",
         "Centralized logging is a single point of failure — consider local buffers."],
    ),
    "api-testing-strategy": (
        ["Only happy-path tests — failures and edge cases untested.",
         "Contract tests that drift from the real spec — keep them generated from OpenAPI.",
         "Load tests run against a toy environment — results don't transfer to prod.",
         "Test data with hardcoded IDs — tests break when data changes."],
        ["E2E tests are slow and brittle — use them sparingly, unit tests heavily.",
         "Contract testing adds tooling overhead — worth it for cross-team APIs.",
         "Load testing costs infrastructure — run in CI on schedules, not every commit."],
    ),
    "auth-implementation-guide": (
        ["Storing secrets in localStorage — XSS can steal them.",
         "Rolling your own crypto or JWT library — almost always a mistake.",
         "No token expiry or rotation — long-lived tokens are a liability.",
         "Session fixation — not regenerating session ID after login."],
        ["JWT vs opaque sessions: JWTs scale horizontally but cannot be revoked easily.",
         "OAuth2 adds complexity — only needed when third parties access your API.",
         "Passwordless (WebAuthn) is more secure but has UX and browser support costs."],
    ),
    "ci-cd-production": (
        ["Building artifacts in the deploy job — non-reproducible builds.",
         "Deploying from a branch instead of an immutable artifact.",
         "No rollback plan — a bad deploy takes the site down for hours.",
         "Secrets in build logs or environment variables visible to all jobs."],
        ["Blue/green is safer but doubles infrastructure cost.",
         "Canary deploys reduce risk but need good metrics to decide rollback.",
         "Faster deploys mean more risk per deploy — balance with automated checks."],
    ),
    "cybersecurity-fundamentals": (
        ["Using outdated dependencies with known CVEs.",
         "Storing passwords in plaintext or with weak hashing (MD5/SHA1).",
         "Trusting client-side input without server-side validation.",
         "Ignoring security headers — X-Frame-Options, CSP, HSTS."],
        ["Security tools (SAST/DAST) catch known patterns, not logic flaws — combine with review.",
         "Penetration testing is expensive — prioritize critical assets.",
         "Zero-trust is stronger but harder to operate — start with least privilege."],
    ),
    "data-engineering-pipelines": (
        ["No schema validation — bad data silently corrupts downstream.",
         "Batch jobs that fail at 2am with no alerting.",
         "Incremental loads without idempotency — double-loading duplicates data.",
         "No data lineage — cannot trace a bug to its source."],
        ["Streaming is lower latency but more complex — batch is fine for daily reports.",
         "Full reloads are simpler but expensive — incremental saves cost but add complexity.",
         "A single pipeline tool may not fit all teams — standardize on contracts instead."],
    ),
    "design-system-builder": (
        ["Tokens not used consistently — designers and devs drift apart.",
         "Components without accessibility baked in.",
         "Versioning breaking changes without a migration path.",
         "Documentation that is not kept in sync with the code."],
        ["A design system is a product — it needs investment or it rots.",
         "Too strict tokens limit creativity — allow escape hatches with review.",
         "Adopting a system-wide refactor is risky — roll out incrementally."],
    ),
    "docker-production-checklist": (
        ["Running as root inside the container.",
         "No healthcheck — orchestrator cannot detect a dead container.",
         "Unpinned base images — builds break when upstream changes.",
         "Copying secrets into the image at build time."],
        ["Multi-stage builds reduce size but add complexity — worth it for large images.",
         "Distroless images are smaller but harder to debug — no shell.",
         "Image scanning adds CI time — run it on the final image only."],
    ),
    "frontend-testing-playbook": (
        ["Testing only the happy path — no error states or edge cases.",
         "Snapshot tests that change on every layout tweak — brittle.",
         "E2E tests that are slow and flaky — CI becomes a lottery.",
         "No accessibility testing — a11y regressions are silent."],
        ["Visual regression testing is powerful but noisy — use it on critical pages only.",
         "Component tests are fast but miss integration issues — combine with E2E.",
         "Test coverage is not the goal — behavior coverage is."],
    ),
    "git-workflow-master": (
        ["Force-pushing to shared branches — history rewrite breaks others.",
         "Huge PRs that are impossible to review.",
         "Merging without running CI.",
         "Committing secrets or large binaries."],
        ["Rebase keeps history clean but rewrites it — never rebase shared branches.",
         "Feature branches isolate work but create merge overhead — trunk-based is faster.",
         "Squash merges are clean but lose commit granularity — pick per repo."],
    ),
    "graphql-api-engineering": (
        ["No query cost limits — a client can request the whole database.",
         "N+1 queries in resolvers — database hammering.",
         "Exposing internal fields via introspection.",
         "No pagination on list fields — unbounded responses."],
        ["GraphQL is powerful but complex — REST is simpler for public APIs.",
         "Schema evolution is easier with GraphQL but harder to cache.",
         "Persisted queries help caching — but add complexity."],
    ),
    "incident-response-sre": (
        ["No runbooks — every incident is a new investigation.",
         "Siloed communication — the incident commander is not clear.",
         "No postmortem — the same incident happens twice.",
         "Metrics that are not monitored — you find out from users."],
        ["Immediate mitigation vs root cause — stabilize first, investigate later.",
         "Postmortems take time — but they are the highest-leverage investment.",
         "On-call rotation is expensive — balance with alert quality."],
    ),
    "kubernetes-production": (
        ["No resource limits — a runaway pod takes down the node.",
         "Running as root or with excessive RBAC.",
         "No probes — rolling updates kill healthy pods.",
         "State in pods — ephemeral storage is lost on restart."],
        ["Kubernetes is powerful but operationally heavy — consider managed platforms.",
         "Helm charts add abstraction — sometimes plain manifests are clearer.",
         "Multi-node clusters need careful networking — start small."],
    ),
    "llm-application-engineering": (
        ["No structured output — parsing free text is fragile.",
         "No cost limits — a runaway loop burns the budget.",
         "Prompt injection — untrusted input reaches the model.",
         "No evaluation — you cannot tell if a change improves quality."],
        ["LLM APIs are non-deterministic — add tests with tolerance, not exact match.",
         "Smaller models are cheaper and faster but less capable — match model to task.",
         "Caching responses helps cost but may serve stale data."],
    ),
    "message-queues-events": (
        ["No idempotency — duplicate events cause double-processing.",
         "No DLQ — poison messages block the queue forever.",
         "No contract versioning — schema changes break consumers.",
         "At-least-once semantics assumed as exactly-once."],
        ["Queues add latency and complexity — sometimes a simple HTTP call is enough.",
         "Exactly-once is impossible in distributed systems — design for at-least-once + idempotency.",
         "Outbox pattern is robust but adds a write to the database."],
    ),
    "ml-evaluation-mlops": (
        ["Evaluating on the training set — inflated metrics.",
         "No data lineage — you cannot reproduce a model.",
         "No drift monitoring — the model silently degrades in production.",
         "Manual deployment without rollback."],
        ["MLOps tooling is heavy — start with a simple registry and add as needed.",
         "Shadow deployment is safer but doubles compute — balance with traffic.",
         "Evaluation is subjective — agree on metrics before optimizing."],
    ),
    "postgresql-master": (
        ["No indexes on foreign keys — joins degrade with data growth.",
         "SELECT * on wide tables — unnecessary I/O.",
         "No EXPLAIN before optimizing — guessing is expensive.",
         "Connection pool exhaustion under load."],
        ["Indexes speed reads but slow writes — index what you query, not everything.",
         "Partitioning helps large tables but adds complexity — only when needed.",
         "ORM-generated queries may be suboptimal — profile and hand-tune hot paths."],
    ),
    "prisma-orm-playbook": (
        ["No migrations in version control — schema drift.",
         "N+1 queries from lazy loading relations.",
         "Raw SQL mixed with the ORM inconsistently.",
         "No transaction wrapping on multi-write operations."],
        ["Prisma is convenient but abstracts SQL — learn SQL for complex queries.",
         "Migrations are automated but review them — they can be destructive.",
         "Prisma's query engine adds overhead — consider raw SQL for hot paths."],
    ),
    "pytorch-training-playbook": (
        ["No seed — training is not reproducible.",
         "Mixed precision without checking for numerical instability.",
         "Gradient accumulation without proper loss scaling.",
         "Training on the full dataset without a validation split."],
        ["Mixed precision is faster but can overflow — monitor loss curves.",
         "Distributed training adds complexity — start single-GPU.",
         "Checkpointing every epoch is expensive — save best + last."],
    ),
    "rag-pipeline-architect": (
        ["Chunking without considering semantic boundaries — context gets split.",
         "No evaluation — retrieval quality is unmeasured.",
         "Embedding model mismatch between indexing and querying.",
         "Ignoring hybrid search — pure vector misses exact matches."],
        ["Vector search is powerful but not always better than keyword — use hybrid.",
         "Reranking improves quality but adds latency — measure the trade-off.",
         "Indexing is expensive — balance freshness with cost."],
    ),
    "react-nextjs-patterns": (
        ["Client-side state that should be server-side.",
         "No caching strategy — every request hits the origin.",
         "Server Actions without error handling — silent failures.",
         "Ignoring Next.js caching headers — CDN misses."],
        ["Server Components are great for SEO but limit interactivity — use client where needed.",
         "Server Actions simplify mutations but complicate optimistic UI — weigh them.",
         "App Router is the future but has migration cost — plan it."],
    ),
    "responsive-layout-master": (
        ["Fixed pixel widths — break on small screens.",
         "No fluid typography — text overflows on mobile.",
         "Container queries where viewport queries would do — over-engineering.",
         "Testing only on one device — browsers differ."],
        ["Mobile-first is a mindset, not a rule — desktop-first works for some apps.",
         "Container queries are powerful but new — check browser support.",
         "Fluid grids can cause layout shifts — use min/max constraints."],
    ),
    "linux-cli-mastery": (
        ["Parsing `ls` output — filenames with spaces break scripts.",
         "No quoting — glob expansion surprises.",
         "Piping without error handling — `set -e` is your friend.",
         "Running scripts with `sudo` that don't need it."],
        ["Shell scripts are fast to write but hard to test — use Python for complex logic.",
         "`find -exec` vs `xargs` — both have edge cases, know them.",
         "Aliases are convenient but not portable — use functions for reuse."],
    ),
    "api-security-hardening": (
        ["BOLA/IDOR — object IDs guessable without ownership checks.",
         "No rate limiting — brute force and scraping.",
         "Verbose error messages leaking internals.",
         "Missing security headers — CORS, CSP, HSTS."],
        ["Security hardening adds latency (rate limiting, auth checks) — measure the cost.",
         "WAFs help but are bypassable — defense in depth.",
         "Pen testing is periodic — continuous scanning is better."],
    ),
    "clean-architecture-ddd": (
        ["Over-engineering — DDD for a CRUD app adds ceremony.",
         "Domain model leaking into infrastructure — coupling.",
         "Anemic domain models — services do all the logic.",
         "Bounded contexts drawn wrong — teams step on each other."],
        ["DDD shines in complex domains — skip it for simple CRUD.",
         "Ports & adapters add indirection — worth it for testability of core logic.",
         "Event-driven DDD is powerful but hard to debug — start with commands/queries."],
    ),
    "elasticsearch-search": (
        ["No mapping — dynamic mapping causes type conflicts.",
         "Analyzer mismatch — search terms don't match indexed terms.",
         "Ignoring relevance tuning — default scoring may not fit.",
         "No index lifecycle — unbounded growth kills performance."],
        ["Elasticsearch is powerful but operationally heavy — consider managed search.",
         "Keyword vs full-text — know which field type fits each query.",
         "Reindexing is disruptive — plan for downtime or use aliases."],
    ),
    "fastapi-python-backend": (
        ["Blocking I/O in async endpoints — the event loop stalls.",
         "Pydantic v1 vs v2 API drift — upgrade carefully.",
         "No dependency injection for services — hard to test.",
         "Synchronous SQLAlchemy calls in async handlers."],
        ["FastAPI is fast to build but async adds complexity — sync endpoints are fine for I/O-bound work.",
         "Pydantic v2 is faster but has migration cost — plan it.",
         "Starlette's test client is sync — async tests need care."],
    ),
    "gdpr-data-privacy": (
        ["No data mapping — you cannot answer 'where is user data?'.",
         "Consent not logged — cannot prove compliance.",
         "No retention policy — data kept forever.",
         "DSR (delete) requests not automated — manual is error-prone."],
        ["Privacy engineering adds friction — balance with product velocity.",
         "Data minimization means collecting less — sometimes you need more for analytics.",
         "GDPR compliance is regional — a global policy may be overkill for some markets."],
    ),
    "gitops-kubernetes": (
        ["Drift between repo and cluster — manual changes fight the pipeline.",
         "No review on manifests — a typo deploys to prod.",
         "Progressive delivery without rollback — a bad canary sticks.",
         "Secrets in the git repo — even in a private repo."],
        ["GitOps is powerful but requires discipline — every change is a PR.",
         "Argo CD vs Flux — both are good, pick one and standardize.",
         "Automated sync is great but can fight hotfixes — have an escape hatch."],
    ),
    "golang-microservices": (
        ["Blocking the event loop with CPU-heavy work — Go's scheduler is cooperative.",
         "No error handling on gRPC calls — silent failures.",
         "Over-using channels — sometimes a mutex is simpler.",
         "No observability — Go's speed hides problems until they're big."],
        ["Go is fast but verbose for some tasks — match language to team.",
         "gRPC is efficient but harder to debug than REST — use HTTP/JSON for public APIs.",
         "Concurrency primitives are powerful but easy to misuse — prefer libraries."],
    ),
    "node-typescript-backend": (
        ["Synchronous I/O in async handlers — blocks the event loop.",
         "No input validation — Zod/Valibot forgotten.",
         "Catching errors and swallowing them — silent failures.",
         "No type safety at the boundary — `any` leaks in."],
        ["TypeScript adds safety but costs boilerplate — worth it for teams.",
         "Fastify vs Express — Fastify is faster but less familiar.",
         "Async is non-optional in Node — learn it properly."],
    ),
    "microfrontends-module-federation": (
        ["Shared dependencies version conflicts — runtime errors.",
         "No contract between teams — integration breaks.",
         "Over-engineering — a monolith is simpler for small teams.",
         "No fallback for a failed remote module — the whole page breaks."],
        ["Module Federation is powerful but adds runtime complexity — use it for true multi-team scale.",
         "Shared deps reduce duplication but create coupling — choose carefully.",
         "Version skew between teams is real — agree on a release cadence."],
    ),
    "pwa-offline-first": (
        ["Cache invalidation — users get stale data.",
         "No offline sync conflict resolution — data loss.",
         "Service worker scope too broad — caches everything.",
         "No manifest — PWA installability lost."],
        ["Offline-first is great for flaky networks but adds sync complexity — consider if users are online.",
         "Service workers are powerful but hard to debug — use Workbox.",
         "Push notifications need permission — don't rely on them."],
    ),
    "web-localization-i18n": (
        ["Pluralization done manually — breaks for languages with 3+ plural forms.",
         "RTL layout not handled — text overflows.",
         "No locale routing — wrong content for wrong region.",
         "Hardcoded strings — translation impossible."],
        ["i18n adds complexity — start with a few locales and grow.",
         "Machine translation is fast but error-prone — human review for customer-facing text.",
         "Locale routing (URL prefixes) is SEO-friendly but adds URL complexity."],
    ),
    "property-based-testing": (
        ["Generators that don't cover edge cases — false confidence.",
         "Shrinking disabled — failure output is unusable.",
         "Properties too weak — tests pass trivially.",
         "Running too few cases — misses rare failures."],
        ["Property-based testing finds edge cases but needs good generators — invest in them.",
         "It complements, not replaces, example-based tests — use both.",
         "Hypothesis/QuickCheck add a learning curve — start with simple properties."],
    ),
    "react-native-expo": (
        ["No offline handling — app breaks on flaky networks.",
         "State not persisted — app resets on restart.",
         "No push notifications — user engagement drops.",
         "Release without staging — app store rejects."],
        ["Expo is fast to develop but abstracts native — some features need native code.",
         "Offline-first adds sync complexity — consider if users are online.",
         "App store release cycles are slow — plan updates carefully."],
    ),
    "flutter-development": (
        ["State management overkill — setState everywhere.",
         "No platform channels — iOS/Android differences ignored.",
         "Widget tree too deep — performance suffers.",
         "No integration tests — refactors break UI."],
        ["Flutter is fast to build but Dart is a niche language — consider team familiarity.",
         "Hot reload is great but hides state issues — test thoroughly.",
         "Platform channels are powerful but add complexity — use them judiciously."],
    ),
    "mongodb-data-modeling": (
        ["Embedding everything — document growth hits 16MB limit.",
         "No indexes on query fields — full collection scans.",
         "Referencing without population — N+1 queries.",
         "Ignoring aggregation pipeline — client-side processing."],
        ["Embedding is fast but limits flexibility — reference for many-to-many.",
         "MongoDB is great for flexible schemas but weak for transactions — use Postgres for relational data.",
         "Aggregation pipeline is powerful but complex — know when to use it."],
    ),
    "observability-prometheus-grafana": (
        ["Alerting on every metric — alert fatigue.",
         "No SLOs — you cannot know what to alert on.",
         "PromQL too complex — dashboards unreadable.",
         "No retention policy — disk fills up."],
        ["Prometheus is great for metrics but not logs — use Loki or ELK for logs.",
         "Grafana is powerful but has a learning curve — start with templates.",
         "High-cardinality metrics are expensive — aggregate where possible."],
    ),
    "serverless-edge-computing": (
        ["Cold starts — user-facing latency spikes.",
         "No timeout handling — functions die mid-task.",
         "State in functions — lost on scale-down.",
         "Cost surprises — invocations add up."],
        ["Serverless is great for bursty workloads but costly for sustained load — compare pricing.",
         "Edge functions reduce latency but limit compute — match task to layer.",
         "Cold starts are a real UX issue — use warm pools or keep-alive."],
    ),
    "redis-caching": (
        ["Cache-aside without TTL — stale data forever.",
         "Using Redis as a primary database — it is not durable by default.",
         "No connection pooling — connection exhaustion.",
         "Cache stampede — all requests miss at once and hit the DB."],
        ["Redis is fast but not a replacement for a real database — use it for cache/queue.",
         "Distributed locking with Redis is tricky — consider Redlock carefully.",
         "Cache invalidation is hard — prefer TTLs over explicit invalidation."],
    ),
    "secrets-management": (
        ["Secrets in code or config files committed to git.",
         "No rotation — a leaked secret is valid forever.",
         "Broad access to the vault — least privilege forgotten.",
         "No audit log — you cannot know who accessed what."],
        ["Vault adds operational complexity — start with environment variables for small apps.",
         "Rotation is disruptive — balance frequency with risk.",
         "Centralized vaults are a single point of failure — plan for availability."],
    ),
    "seo-programmatic": (
        ["Duplicate meta tags across pages — search engines penalize.",
         "No canonical URLs — duplicate content confusion.",
         "Blocking robots.txt on pages that should be indexed.",
         "No sitemap — slow discovery of new pages."],
        ["SEO is a long game — measure over months, not days.",
         "JSON-LD structured data helps rich results but adds maintenance.",
         "Client-side rendering hurts SEO — use SSR or prerendering."],
    ),
    "supply-chain-security": (
        ["No SBOM — you cannot know what is in your software.",
         "No dependency pinning — builds break or get hijacked.",
         "No signature verification — tampered artifacts.",
         "Ignoring known CVEs in transitive dependencies."],
        ["SBOMs add process overhead — start with critical services.",
         "Pinning everything prevents drift but blocks updates — balance.",
         "Signature verification is important but adds key management."],
    ),
    "system-design-architect": (
        ["Designing for scale before you have users — premature optimization.",
         "No circuit breaker — cascading failures.",
         "Synchronous calls between services — latency and coupling.",
         "Ignoring backpressure — slow consumers overflow queues."],
        ["Microservices add operational complexity — start monolith, split when needed.",
         "Queues add resilience but latency — use sync for low-latency paths.",
         "Caching improves speed but adds staleness — know your tolerance."],
    ),
    "terraform-infrastructure": (
        ["No remote state — concurrent applies corrupt state.",
         "Plan review skipped — destructive changes hit production.",
         "Hardcoded secrets in .tf files.",
         "No drift detection — reality differs from code."],
        ["Terraform is powerful but stateful — plan carefully, review plans.",
         "Terragrunt/OpenTofu add abstraction — evaluate the cost.",
         "IaC is code — version it, review it, test it."],
    ),
    "threat-modeling-stride": (
        ["Modeling after implementation — too late to change design.",
         "No abuse cases — only happy-path threats.",
         "Trust boundaries drawn too coarsely — internal threats missed.",
         "Mitigations listed but not implemented or tested."],
        ["Threat modeling is time-consuming — focus on high-value assets.",
         "STRIDE is a checklist, not a substitute for thinking.",
         "Automated tools help but miss business logic threats."],
    ),
    "typescript-advanced-patterns": (
        ["Using `any` liberally — defeats the type system.",
         "Overly clever generics — unreadable by the team.",
         "Type guards that lie — runtime behavior differs from type claims.",
         "Discriminated unions without a discriminant — unsafe narrowing."],
        ["Strict typing costs boilerplate but prevents whole classes of bugs.",
         "Generic utilities are powerful but can obscure intent — name them well.",
         "Type-level programming is clever but hard to maintain — use sparingly."],
    ),
    "web-performance-core-vitals": (
        ["Optimizing LCP while INP is the bottleneck — misdirected effort.",
         "No performance budget — regressions go unnoticed.",
         "Third-party scripts blocking render.",
         "Ignoring mobile — desktop-only testing misses real users."],
        ["Perf budgets can slow velocity — set them at a sustainable level.",
         "RUM is noisy — use it with synthetic tests.",
         "Every optimization has a cost — measure before and after."],
    ),
    "websocket-realtime": (
        ["No heartbeat — dead connections linger.",
         "No reconnect with backoff — thundering herd on server restart.",
         "No backpressure — slow clients buffer unbounded data.",
         "Broadcasting to all clients when only some need it."],
        ["WebSockets are stateful — horizontal scaling needs sticky sessions or a pub/sub layer.",
         "SSE is simpler for one-way server-to-client — consider it.",
         "Long-lived connections cost resources — idle timeout policies matter."],
    ),
    "zero-trust-application-security": (
        ["Treating the network as trusted — lateral movement is easy.",
         "No workload identity — service-to-service calls unauthenticated.",
         "Broad IAM grants — least privilege forgotten.",
         "No continuous verification — access persists after role change."],
        ["Zero-trust is operationally heavy — start with high-value services.",
         "mTLS everywhere adds complexity — prioritize critical paths.",
         "Identity-based access is powerful but needs strong identity management."],
    ),
}

def insert_before_refs_or_end(text: str, section: str) -> str:
    """Insert section before References heading, or before watermark, or append."""
    # Find References heading
    ref_match = re.search(r"^##\s+(?:References|Referensi)\b", text, re.M | re.I)
    if ref_match:
        return text[: ref_match.start()] + section + "\n\n" + text[ref_match.start() :]
    # Find watermark
    wm_match = re.search(r"^\*Dokumentasi ini bagian dari", text, re.M)
    if wm_match:
        return text[: wm_match.start()] + section + "\n\n" + text[wm_match.start() :]
    # Append at end
    return text.rstrip() + "\n\n" + section + "\n"

def main() -> int:
    changed = 0
    for sid, (pitfalls, tradeoffs) in sorted(CONTENT.items()):
        guide = SKILLS_DIR / sid / f"{sid}.md"
        if not guide.is_file():
            print(f"SKIP (no guide): {sid}")
            continue
        text = guide.read_text(encoding="utf-8")
        original = text
        additions = []

        # Add pitfalls section if not present (case-insensitive)
        if not re.search(
            r"^##\s*(?:Kesalahan Umum|Pitfalls|Common Failure Modes|Common Mistakes|Anti-patterns)",
            text,
            re.M | re.I,
        ):
            bullets = "\n".join(f"- {b}" for b in pitfalls)
            additions.append(f"## Kesalahan Umum / Pitfalls\n\n{bullets}")

        # Add trade-off section if not present
        if not re.search(
            r"^##\s*(?:Trade-off|Kapan Tidak|Tidak Pakai|When Not To Use|Tradeoffs)",
            text,
            re.M | re.I,
        ):
            bullets = "\n".join(f"- {b}" for b in tradeoffs)
            additions.append(f"## Trade-off dan Kapan Tidak Pakai\n\n{bullets}")

        if additions:
            section = "\n\n".join(additions)
            text = insert_before_refs_or_end(text, section)
        if text != original:
            guide.write_text(text, encoding="utf-8")
            changed += 1
            print(f"UPDATED: {sid}")

    print(f"\n{changed} guides updated.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
