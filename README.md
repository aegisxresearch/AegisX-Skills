# 🚀 AegisX Skills Collection

> Kumpulan **42 skills** untuk programmer, software engineer, DevOps engineer, security engineer, dan ML engineer — dibuat sebagai portfolio dan referensi praktis untuk pengembangan software modern.

![GitHub repo size](https://img.shields.io/github/repo-size/aegisxresearch/AegisX-Skills)
![GitHub last commit](https://img.shields.io/github/last-commit/aegisxresearch/AegisX-Skills)

---

## 📖 Tentang

Repository ini berisi kumpulan panduan teknis terstruktur yang mencakup **Backend API, Frontend, Web Design, Machine Learning, AI Engineering, Database, Data Engineering, DevOps, Cloud, Security, Architecture, dan Programming**.

Setiap skill berada di folder sendiri dengan struktur:

```text
skills/<nama-skill>/
├── README.md          ← Ringkasan kategori, level, dan topik
└── <nama-skill>.md    ← Panduan lengkap, contoh, checklist, dan references
```

Materi ini bersifat referensi engineering. Contoh production-oriented tetap harus disesuaikan dengan stack, threat model, regulasi, dan kebutuhan sistem yang digunakan.

---

<!-- CATALOG_START -->

## 🗂️ Daftar Skills

Katalog ini dihasilkan secara otomatis dari [`skills/manifest.json`](./skills/manifest.json) oleh [`scripts/generate-readme.py`](./scripts/generate-readme.py). Jangan mengedit bagian ini secara manual.

### Backend API dan Realtime

| Skill | Level | Deskripsi |
|-------|-------|-----------|
| [`api-design-patterns`](./skills/api-design-patterns/) | Intermediate–Advanced | RESTful API design, pagination, versioning, rate limiting, filtering, dan sorting. |
| [`api-observability`](./skills/api-observability/) | Intermediate–Advanced | Logs, metrics, traces, SLO, dan alerting untuk API. |
| [`api-testing-strategy`](./skills/api-testing-strategy/) | Intermediate–Advanced | Unit, integration, contract, dan load testing untuk API. |
| [`auth-implementation-guide`](./skills/auth-implementation-guide/) | Intermediate–Advanced | JWT, OAuth2 + PKCE, session management, dan security checklist. |
| [`graphql-api-engineering`](./skills/graphql-api-engineering/) | Intermediate–Advanced | Schema, resolver, authorization, pagination, dan query-cost controls. |
| [`message-queues-events`](./skills/message-queues-events/) | Advanced | Event contracts, idempotency, retries, DLQ, dan outbox. |
| [`websocket-realtime`](./skills/websocket-realtime/) | Intermediate–Advanced | Connection lifecycle, reconnect, backpressure, dan fanout. |

### Machine Learning dan AI

| Skill | Level | Deskripsi |
|-------|-------|-----------|
| [`llm-application-engineering`](./skills/llm-application-engineering/) | Intermediate–Advanced | Structured output, tool use, safety, cost, dan fallback. |
| [`ml-evaluation-mlops`](./skills/ml-evaluation-mlops/) | Advanced | Dataset lineage, model registry, deployment, drift, dan rollback. |
| [`pytorch-training-playbook`](./skills/pytorch-training-playbook/) | Intermediate–Advanced | Training loop, mixed precision, gradient accumulation, dan debugging. |
| [`rag-pipeline-architect`](./skills/rag-pipeline-architect/) | Advanced | Chunking, embeddings, vector DB, hybrid search, dan evaluation. |

### Frontend dan Web Design

| Skill | Level | Deskripsi |
|-------|-------|-----------|
| [`accessibility-wcag`](./skills/accessibility-wcag/) | Intermediate–Advanced | Semantic HTML, keyboard UX, ARIA, WCAG, dan testing. |
| [`animation-performance-guide`](./skills/animation-performance-guide/) | Intermediate | GPU animation, will-change, dan reduced motion. |
| [`design-system-builder`](./skills/design-system-builder/) | Intermediate–Advanced | Design tokens, components, documentation, dan WCAG. |
| [`frontend-testing-playbook`](./skills/frontend-testing-playbook/) | Intermediate–Advanced | Component, integration, E2E, accessibility, dan visual tests. |
| [`react-nextjs-patterns`](./skills/react-nextjs-patterns/) | Intermediate–Advanced | Server Components, App Router, Server Actions, dan state management. |
| [`responsive-layout-master`](./skills/responsive-layout-master/) | Beginner–Intermediate | Mobile-first, fluid typography, container queries, dan layout. |
| [`seo-programmatic`](./skills/seo-programmatic/) | Intermediate–Advanced | Metadata, canonical, sitemap, robots, JSON-LD, dan indexability. |
| [`web-performance-core-vitals`](./skills/web-performance-core-vitals/) | Intermediate–Advanced | LCP, INP, CLS, performance budget, dan RUM. |

### Database dan Data Engineering

| Skill | Level | Deskripsi |
|-------|-------|-----------|
| [`data-engineering-pipelines`](./skills/data-engineering-pipelines/) | Intermediate–Advanced | Batch/streaming, contracts, incremental loads, quality, dan lineage. |
| [`postgresql-master`](./skills/postgresql-master/) | Intermediate–Advanced | Indexing, query optimization, partitioning, dan tuning. |
| [`prisma-orm-playbook`](./skills/prisma-orm-playbook/) | Beginner–Intermediate | Schema, relations, CRUD, transactions, dan migrations. |
| [`redis-caching`](./skills/redis-caching/) | Intermediate–Advanced | Cache-aside, TTL, rate limiting, locks, memory, dan security. |

### Architecture dan Reliability

| Skill | Level | Deskripsi |
|-------|-------|-----------|
| [`incident-response-sre`](./skills/incident-response-sre/) | Intermediate–Advanced | Incident command, mitigation, runbooks, SLO, dan postmortems. |
| [`system-design-architect`](./skills/system-design-architect/) | Advanced | Scalability, microservices, queues, circuit breaker, dan resilience. |

### DevOps dan Cloud

| Skill | Level | Deskripsi |
|-------|-------|-----------|
| [`ci-cd-production`](./skills/ci-cd-production/) | Intermediate–Advanced | Immutable artifacts, deployment strategy, scanning, dan rollback. |
| [`docker-production-checklist`](./skills/docker-production-checklist/) | Intermediate | Multi-stage builds, non-root, health checks, dan resource limits. |
| [`kubernetes-production`](./skills/kubernetes-production/) | Advanced | Probes, resources, RBAC, rollout, disruption, dan observability. |
| [`linux-cli-mastery`](./skills/linux-cli-mastery/) | Beginner–Intermediate | File operations, grep/sed/awk, proses, dan Bash scripting. |
| [`terraform-infrastructure`](./skills/terraform-infrastructure/) | Intermediate–Advanced | Modules, remote state, plan review, drift, dan safe changes. |

### Security

| Skill | Level | Deskripsi |
|-------|-------|-----------|
| [`cybersecurity-fundamentals`](./skills/cybersecurity-fundamentals/) | Intermediate–Advanced | OWASP Top 10, secure coding, dan penetration testing. |
| [`secrets-management`](./skills/secrets-management/) | Intermediate–Advanced | Secret lifecycle, rotation, vault, access control, dan incident response. |
| [`supply-chain-security`](./skills/supply-chain-security/) | Intermediate–Advanced | Dependency, SBOM, provenance, signing, dan artifact verification. |
| [`threat-modeling-stride`](./skills/threat-modeling-stride/) | Intermediate–Advanced | Assets, trust boundaries, STRIDE, abuse cases, dan mitigasi. |
| [`zero-trust-application-security`](./skills/zero-trust-application-security/) | Advanced | Workload identity, least privilege, segmentation, dan continuous verification. |

### Anti-AI-Slop dan Quality

| Skill | Level | Deskripsi |
|-------|-------|-----------|
| [`anti-hallucinated-dependencies`](./skills/anti-hallucinated-dependencies/) | Intermediate–Advanced | Verifikasi package, API, versi, lockfile, dan dependency necessity. |
| [`anti-slop-agent-output`](./skills/anti-slop-agent-output/) | Intermediate–Advanced | Pelaporan perubahan, test, asumsi, risiko, dan keterbatasan secara faktual. |
| [`anti-slop-code-review`](./skills/anti-slop-code-review/) | Intermediate–Advanced | Review berbasis behavior, complexity, error handling, dan evidence. |
| [`anti-slop-documentation`](./skills/anti-slop-documentation/) | Intermediate–Advanced | Klaim berbukti, contoh jujur, trade-off, dan dokumentasi terawat. |
| [`anti-slop-test-quality`](./skills/anti-slop-test-quality/) | Intermediate–Advanced | Assertion kuat, failure cases, mock boundaries, dan flake prevention. |

### Programming dan Workflow

| Skill | Level | Deskripsi |
|-------|-------|-----------|
| [`git-workflow-master`](./skills/git-workflow-master/) | Beginner–Advanced | Branching, rebase, cherry-pick, bisect, worktree, dan commits. |
| [`typescript-advanced-patterns`](./skills/typescript-advanced-patterns/) | Intermediate–Advanced | Generics, utility types, type guards, dan design patterns. |
<!-- CATALOG_END -->

---

## 🧭 Jalur Belajar yang Disarankan

### Membangun aplikasi web
```text
System Design → API Design → Authentication → PostgreSQL/Prisma
→ React/Next.js → Design System → Accessibility → Testing
→ Observability → Docker/CI/CD
```

### Membangun aplikasi AI
```text
Data Engineering → RAG Pipeline atau LLM Application
→ Evaluation/MLOps → API Observability → Security
```

### Menyiapkan production platform
```text
Threat Modeling → Secrets Management → Terraform → Kubernetes
→ CI/CD → Supply-Chain Security → Incident Response/SRE
```

---

## 🚀 Cara Menggunakan

### 1. Clone repository
```bash
git clone https://github.com/aegisxresearch/AegisX-Skills.git
cd AegisX-Skills
```

### 2. Baca skill yang dibutuhkan
Mulai dari `README.md` pada folder skill, kemudian baca panduan utama untuk contoh dan checklist.

### 3. Gunakan sebagai referensi
- 📋 **Checklist** — verifikasi pekerjaan sebelum deploy
- 💻 **Code examples** — template yang harus disesuaikan dengan stack
- ✅ **Best practices** — panduan desain, testing, security, dan operasi

---

## 🤝 Kontribusi

1. Buat folder baru: `skills/<nama-skill>/`
2. Tambahkan `README.md` dengan kategori, level, deskripsi, dan references.
3. Tambahkan file skill utama `<nama-skill>.md`.
4. Sertakan contoh, trade-off, failure modes, checklist, dan referensi resmi.
5. Tambahkan entri di `skills/manifest.json` (id, category, level, summary, tags, overview, guide, status).
6. Jalankan `python3 scripts/generate-readme.py` dan `python3 scripts/validate-skills.py`.
7. Submit Pull Request.

---

## 📄 License

MIT License — bebas digunakan untuk belajar dan pengembangan.

---

<div align="center">

**Dibuat dengan ❤️ oleh [AegisX Research](https://github.com/aegisxresearch)**

</div>
