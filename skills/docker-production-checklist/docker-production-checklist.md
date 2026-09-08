# `Docker` Production Checklist

## Overview
Panduan `Docker` untuk production: multi-stage builds, security, health checks, dan best practices.

---

## ️ Multi-Stage Build

### Python App
```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy only needed files
COPY --from=builder /root/.local /root/.local
COPY . .

# Set environment
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "main.py"]
```bash

### Node.js App
```dockerfile
# Stage 1: Build
FROM node:20-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Runtime
FROM node:20-alpine as runtime

RUN addgroup -g 1001 -S appgroup
RUN adduser -S appuser -u 1001 -G appgroup

WORKDIR /app

COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/package.json .

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/main.js"]
```bash

---

## Security Best Practices

### Dockerfile Security
```dockerfile
# Use specific version tags
FROM python:3.11.7-slim

# Run as non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Don't store secrets in image
# Use environment variables or `Docker` secrets

# Scan for vulnerabilities
# Run: docker scout cves <image>

# Don't use latest tag
# FROM python:latest  ← BAD

# Don't run as root
# USER root  ← BAD
```yaml

### Environment Variables
```yaml
# docker-compose.yml
services:
  app:
    environment:
      - DATABASE_URL=${DATABASE_URL}  # From .env file
      - SECRET_KEY=${SECRET_KEY}
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```python

---

## Health Checks

### Application Health Endpoint
```python
# `FastAPI` example
from fastapi import `FastAPI`
import psutil

app = `FastAPI`()

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health/ready")
async def readiness():
    # Check dependencies
    db_ok = await check_database()
    redis_ok = await check_redis()
    
    return {
        "status": "ready" if db_ok and redis_ok else "not_ready",
        "checks": {
            "database": "ok" if db_ok else "failed",
            "redis": "ok" if redis_ok else "failed"
        }
    }
```bash

### `Docker` Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 --start-period=10s \
  CMD curl -f http://localhost:8000/health || exit 1
```yaml

---

## `Docker` Compose Production

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
```

---

## Production Checklist

### Security
- [ ] Running as non-root user
- [ ] No secrets in Dockerfile or image
- [ ] Using specific version tags (not :latest)
- [ ] Scanned for vulnerabilities
- [ ] Read-only filesystem where possible

### Performance
- [ ] Multi-stage build (smaller image)
- [ ] .dockerignore configured
- [ ] No unnecessary files in image
- [ ] Layer caching optimized

### Reliability
- [ ] Health check configured
- [ ] Graceful shutdown handling
- [ ] Log rotation configured
- [ ] Resource limits set
- [ ] Restart policy defined

### Monitoring
- [ ] Logs accessible (stdout/stderr)
- [ ] Metrics endpoint available
- [ ] Distributed tracing configured

---

## References
- https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- https://docs.docker.com/compose/production/
- https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
