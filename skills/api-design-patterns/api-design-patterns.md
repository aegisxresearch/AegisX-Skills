# API Design Patterns

## Overview
Panduan lengkap merancang RESTful API yang konsisten, didesain untuk skala yang dibutuhkan, dan mudah dipelajari developer lain.

---

## Core Principles

### 1. Naming Conventions
```sql
✅ GOOD                          ❌ BAD
GET /users                        GET /getUsers
POST /users                       POST /createUser
GET /users/123                    GET /getUserById?id=123
DELETE /users/123                 POST /deleteUser
```

### 2. Resource-Oriented URLs
```text
# Nested resources (max 2 levels)
GET /users/123/orders             ← User's orders
GET /users/123/orders/456         ← Specific order

# Use plural nouns
✅ /users, /orders, /products
❌ /user, /order, /product
```

---

## Standard Response Format

### Success Response
```json
{
  "status": "success",
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Error Response
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid"
      }
    ]
  },
  "meta": {
    "request_id": "req_abc123"
  }
}
```

---

## HTTP Methods

| Method | Purpose | Idempotent | Body |
|--------|---------|------------|------|
| `GET` | Read resource | ✅ Yes | No |
| `POST` | Create resource | ❌ No | Yes |
| `PUT` | Full update | ✅ Yes | Yes |
| `PATCH` | Partial update | ✅ Yes | Yes |
| `DELETE` | Remove resource | ✅ Yes | No |

---

## Pagination

### Cursor-Based (Recommended)
```json
{
  "data": [...],
  "pagination": {
    "cursor": "eyJpZCI6MTIzfQ==",
    "has_more": true,
    "next_url": "/users?cursor=eyJpZCI6MTIzfQ==&limit=20"
  }
}
```

### Offset-Based
```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

---

## ️ Versioning Strategies

### 1. URL Path (Recommended for public API)
```http
/api/v1/users
/api/v2/users
```

### 2. Header
```yaml
Accept: application/vnd.myapi.v2+json
```

### 3. Query Parameter
```http
/users?version=2
```

---

## ️ Security Headers

```yaml
# Essential security headers
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

---

## Rate Limiting

### Headers to Include
```yaml
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642252800
Retry-After: 60  ← When rate limited
```

### Response When Limited
```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests",
    "retry_after": 60
  }
}
```

---

## Filtering & Sorting

```text
# Filtering
GET /users?status=active&role=admin

# Multiple values
GET /users?status=active,pending

# Sorting
GET /users?sort=-created_at,name
         ↑ minus = descending

# Field selection (sparse fieldsets)
GET /users?fields=id,name,email
```

---

## Quick Checklist

- [ ] Use plural nouns for resources
- [ ] Use HTTP methods correctly (GET=read, POST=create, etc.)
- [ ] Consistent error response format
- [ ] Include request_id in all responses
- [ ] Implement pagination for list endpoints
- [ ] Version your API from day one
- [ ] Rate limit all public endpoints
- [ ] Use HTTPS everywhere
- [ ] Document with OpenAPI/Swagger

---

## Kesalahan Umum / Pitfalls

- Breaking changes on every release — no versioning strategy.
- Exposing internal database IDs in URLs without considering enumeration.
- Ignoring pagination — unbounded responses kill mobile clients and DBs.
- Rate limiting only at the gateway — bypassable by direct service access.

## Trade-off dan Kapan Tidak Pakai

- REST is not the only option — GraphQL or gRPC may fit better for some clients.
- Strict contracts help stability but slow iteration — version early, not late.
- Pagination with deep offsets is slow on large tables — consider keyset pagination.

## References
- https://restfulapi.net/
- https://jsonapi.org/
- https://github.com/microsoft/api-guidelines

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
