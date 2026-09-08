# Cybersecurity Fundamentals

## Overview
Panduan keamanan siber: OWASP Top 10, secure coding, penetration testing, dan defense strategies.

---

## ️ OWASP Top 10 (2021)

### 1. Broken Access Control
```python
# BAD: No authorization check
@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    return await db.get_user(user_id)

# GOOD: Check authorization
@app.get("/api/users/{user_id}")
async def get_user(user_id: int, current_user = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403)
    return await db.get_user(user_id)
```python

### 2. Cryptographic Failures
```python
# BAD: Weak hashing
import hashlib
hashed = hashlib.md5(password.encode()).hexdigest()

# GOOD: Strong hashing
from argon2 import PasswordHasher
ph = PasswordHasher()
hashed = ph.hash(password)
```sql

### 3. Injection
```python
# BAD: SQL Injection
query = f"SELECT * FROM users WHERE id = {user_id}"

# GOOD: Parameterized query
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```python

### 4. Insecure Design
```python
# BAD: No rate limiting
@app.post("/login")
async def login(credentials: LoginRequest):
    return await authenticate(credentials)

# GOOD: Rate limiting + account lockout
@app.post("/login")
@limiter.limit("5/minute")
async def login(credentials: LoginRequest):
    user = await get_user_by_email(credentials.email)
    if user and user.failed_login_attempts >= 5:
        raise HTTPException(423, "Account locked")
    return await authenticate(credentials)
```python

### 5. Security Misconfiguration
```python
# BAD: Debug mode in production
app.run(debug=True)

# GOOD: Environment-based config
import os
debug = os.getenv("DEBUG", "false").lower() == "true"
app.run(debug=debug)
```bash

### 6. Vulnerable Components
```bash
# Check for vulnerabilities
npm audit
pip-audit
safety check

# Update dependencies
npm update
pip install --upgrade package-name
```

### 7. Authentication Failures
```python
# GOOD: Secure authentication
- Use Multi-Factor Authentication (MFA)
- Implement account lockout after failed attempts
- Use secure password reset flow
- Log authentication events
```python

### 8. Software & Data Integrity
```python
# GOOD: Verify integrity
import hashlib

def verify_file_integrity(file_path: str, expected_hash: str) -> bool:
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash == expected_hash
```python

### 9. Logging & Monitoring
```python
# GOOD: Security logging
import logging

logger = logging.getLogger("security")

def log_auth_event(event: str, user_id: int, success: bool):
    logger.info(f"Auth event: {event}", extra={
        "user_id": user_id,
        "success": success,
        "timestamp": datetime.now().isoformat()
    })
```python

### 10. Server-Side Request Forgery (SSRF)
```python
# BAD: Unvalidated URL
@app.get("/fetch")
async def fetch_url(url: str):
    return await httpx.get(url)

# GOOD: Validate URL
from urllib.parse import urlparse

ALLOWED_HOSTS = ["api.example.com", "cdn.example.com"]

@app.get("/fetch")
async def fetch_url(url: str):
    parsed = urlparse(url)
    if parsed.hostname not in ALLOWED_HOSTS:
        raise HTTPException(400, "Invalid URL")
    return await httpx.get(url)
```python

---

## Secure Coding Practices

### Input Validation
```python
from pydantic import BaseModel, EmailStr, validator

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str
    age: int
    
    @validator('name')
    def validate_name(cls, v):
        if len(v) < 2:
            raise ValueError('Name must be at least 2 characters')
        if not v.isalnum():
            raise ValueError('Name must be alphanumeric')
        return v
    
    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Invalid age')
        return v
```python

### Output Encoding
```python
from markupsafe import escape

# XSS Prevention
user_input = request.get("name")
safe_output = escape(user_input)
```python

### Session Management
```python
# GOOD: Secure session
from datetime import timedelta

session_config = {
    "secure": True,      # HTTPS only
    "httponly": True,     # No JavaScript access
    "samesite": "lax",   # CSRF protection
    "max_age": 1800,     # 30 minutes
}
```

---

## Penetration Testing Checklist

### Reconnaissance
- [ ] Identify target scope
- [ ] Enumerate subdomains
- [ ] Scan for open ports
- [ ] Identify technologies used

### Testing
- [ ] Test for SQL injection
- [ ] Test for XSS (reflected, stored, DOM)
- [ ] Test for CSRF
- [ ] Test for broken authentication
- [ ] Test for IDOR (Insecure Direct Object References)
- [ ] Test for SSRF
- [ ] Test for file upload vulnerabilities

### Tools
| Tool | Purpose |
|------|---------|
| Burp Suite | Web application testing |
| Nmap | Port scanning |
| OWASP ZAP | Automated security testing |
| sqlmap | SQL injection testing |
| Nikto | Web server scanner |

---

## Security Checklist

### Application
- [ ] Input validation on all endpoints
- [ ] Parameterized queries (no SQL injection)
- [ ] Output encoding (no XSS)
- [ ] CSRF protection enabled
- [ ] Rate limiting implemented
- [ ] Secure session management

### Infrastructure
- [ ] HTTPS everywhere
- [ ] Security headers configured
- [ ] Firewall rules in place
- [ ] Regular security updates
- [ ] Backup and recovery plan

### Code
- [ ] No secrets in code
- [ ] Dependencies scanned for vulnerabilities
- [ ] Code review for security issues
- [ ] Static analysis tools configured

---

## References
- https://owasp.org/www-project-top-ten/
- https://cheatsheetseries.owasp.org/
- https://portswigger.net/web-security

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
