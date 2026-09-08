# `Docker` Production Checklist

> 🎯 **Kategori:** DevOps | **Level:** Intermediate

## Deskripsi
Panduan `Docker` untuk production: multi-stage builds, security, health checks.

## Yang Dipelajari
- Multi-stage builds (Python & Node.js)
- Non-root user setup
- Health checks
- `Docker` Compose production config
- Security best practices
- Resource limits & logging

## File
📄 [`docker-production-checklist.md`](./docker-production-checklist.md) — Isi skill lengkap

## Multi-Stage Pattern
```text
Builder Stage (install deps) → Runtime Stage (copy only needed files) → Run as non-root
```

## References
- https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
