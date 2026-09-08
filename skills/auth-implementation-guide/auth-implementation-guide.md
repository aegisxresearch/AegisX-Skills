# Authentication Implementation Guide

## Overview
Panduan implementasi autentikasi yang aman: JWT, OAuth2, session management, dan best practices.

---

## Authentication Methods Comparison

| Method | Stateless | didesain untuk skala yang dibutuhkan | Secure | Use Case |
|--------|-----------|----------|--------|----------|
| Session + Cookie | ❌ | ⚠️ | ✅ | Traditional web apps |
| JWT (JSON Web Token) | ✅ | ✅ | ✅ | APIs, SPAs |
| OAuth2 + OIDC | ✅ | ✅ | ✅✅ | Third-party login |
| API Keys | ✅ | ✅ | ⚠️ | Service-to-service |

---

## JWT Implementation

### Token Structure
```text
Header.Payload.Signature
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjN9.abc123signature
```

### Access + Refresh Token Pattern
```json
// Access Token (short-lived: 15 min)
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 900
}

// Refresh Token (long-lived: 7 days, httpOnly cookie)
// Stored in httpOnly, secure, sameSite cookie
```

### Token Storage
```text
✅ ACCESS TOKEN  → Memory (JavaScript variable)
✅ REFRESH TOKEN → httpOnly cookie (not accessible by JS)
❌ NEVER         → localStorage (XSS vulnerable)
❌ NEVER         → sessionStorage (XSS vulnerable)
```

---

## OAuth2 Flow (Authorization Code + PKCE)

```text
┌─────────┐     ┌─────────┐     ┌─────────┐
│  User   │────▶│  Your   │────▶│ Provider│
│ Browser │     │  App    │     │(Google) │
└─────────┘     └─────────┘     └─────────┘
     │               │               │
     │  1. Click     │               │
     │  "Login"      │               │
     │──────────────▶│               │
     │               │  2. Redirect  │
     │◀──────────────│──────────────▶│
     │               │               │
     │  3. User      │               │
     │  Authorizes   │               │
     │───────────────────────────────▶│
     │               │               │
     │  4. Auth Code │               │
     │◀──────────────│◀──────────────│
     │               │               │
     │  5. Exchange  │               │
     │  Code + PKCE  │               │
     │──────────────▶│──────────────▶│
     │               │               │
     │  6. Tokens    │               │
     │◀──────────────│◀──────────────│
```typescript

### PKCE Implementation
```javascript
// 1. Generate code verifier & challenge
const codeVerifier = generateRandomString(128);
const codeChallenge = await sha256(codeVerifier)
  .then(buf => base64UrlEncode(buf));

// 2. Redirect to authorization URL
const authUrl = new URL('https://accounts.google.com/o/oauth2/v2/auth');
authUrl.searchParams.set('code_challenge', codeChallenge);
authUrl.searchParams.set('code_challenge_method', 'S256');

// 3. Exchange code for tokens
const tokens = await fetch(tokenUrl, {
  method: 'POST',
  body: JSON.stringify({
    code: authorizationCode,
    code_verifier: codeVerifier,
  })
});
```python

---

## ️ Security Checklist

### Password Hashing
```python
# USE bcrypt, argon2, or scrypt
from argon2 import PasswordHasher
ph = PasswordHasher()
hashed = ph.hash(password)
is_valid = ph.verify(hashed, password)

# NEVER use MD5, SHA1, SHA256 for passwords
# NEVER store plaintext passwords
```

### Rate Limiting Auth Endpoints
```python
# Login endpoint: 5 attempts per minute
# Password reset: 3 attempts per hour
# Registration: 3 per IP per hour
```

### Session Management
```text
✅ Regenerate session ID after login
✅ Set session timeout (15-30 min idle)
✅ Invalidate session on logout
✅ Store session server-side (not in JWT)
✅ Use secure, httpOnly, sameSite cookies
```

---

## Common Vulnerabilities to Prevent

### 1. JWT None Algorithm Attack
```python
# ALWAYS validate algorithm
if header['alg'] == 'none':
    raise InvalidTokenError("Algorithm 'none' not allowed")

# Explicitly set allowed algorithms
decode(token, key, algorithms=['HS256'])
```

### 2. Token Leakage
```text
❌ Don't put sensitive data in JWT payload (it's readable!)
❌ Don't log tokens
❌ Don't include tokens in URLs
✅ Use short-lived access tokens (15 min)
✅ Implement token revocation for logout
```

### 3. CSRF Protection
```python
# SameSite cookie attribute
Set-Cookie: session=abc; SameSite=Lax; Secure; HttpOnly

# Additional CSRF token for state-changing operations
X-CSRF-Token: random-token-here
```

---

## Auth Flow Checklist

- [ ] Passwords hashed with argon2/bcrypt
- [ ] JWT uses RS256 (asymmetric) for public APIs
- [ ] Access token expires in 15 minutes
- [ ] Refresh token in httpOnly cookie
- [ ] Rate limiting on all auth endpoints
- [ ] Account lockout after 5 failed attempts
- [ ] Email verification on registration
- [ ] Password reset via secure token
- [ ] Session invalidation on logout
- [ ] Audit logging for auth events

---

## References
- https://auth0.com/docs/secure/tokens
- https://owasp.org/www-community/attacks/csrf
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
