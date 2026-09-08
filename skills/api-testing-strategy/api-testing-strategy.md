# API Testing Strategy

## Overview
Panduan testing API: unit tests, integration tests, contract testing, dan load testing.

---

## Testing Pyramid

```
           ╱╲
          ╱  ╲         E2E Tests
         ╱    ╲        (Few, slow, expensive)
        ╱──────╲
       ╱        ╲      Integration Tests
      ╱          ╲     (Moderate, test API + DB)
     ╱────────────╲
    ╱              ╲    Unit Tests
   ╱                ╲   (Many, fast, cheap)
  ╱──────────────────╲
```python

### Test Distribution
| Type | Amount | Speed | Cost |
|------|--------|-------|------|
| Unit | 70% | ⚡ Fast | 💰 Low |
| Integration | 25% | 🐢 Medium | 💰💰 Medium |
| E2E | 5% | 🐌 Slow | 💰💰💰 High |

---

## Unit Tests

### Python (pytest)
```python
import pytest
from app.services.user_service import UserService

class TestUserService:
    def setup_method(self):
        self.service = UserService()
    
    def test_create_user_success(self):
        user = self.service.create_user(
            email="test@example.com",
            name="Test User"
        )
        assert user.email == "test@example.com"
        assert user.name == "Test User"
    
    def test_create_user_invalid_email(self):
        with pytest.raises(ValueError, match="Invalid email"):
            self.service.create_user(
                email="not-an-email",
                name="Test"
            )
    
    def test_get_user_not_found(self):
        with pytest.raises(UserNotFoundError):
            self.service.get_user(user_id=999)
```python

### JavaScript (Jest)
```javascript
const UserService = require('../services/user_service');

describe('UserService', () => {
  let service;
  
  beforeEach(() => {
    service = new UserService();
  });
  
  test('create user success', async () => {
    const user = await service.createUser({
      email: 'test@example.com',
      name: 'Test User'
    });
    
    expect(user.email).toBe('test@example.com');
    expect(user.name).toBe('Test User');
  });
  
  test('create user invalid email', async () => {
    await expect(
      service.createUser({ email: 'invalid', name: 'Test' })
    ).rejects.toThrow('Invalid email');
  });
});
```python

---

## Integration Tests

### API Endpoint Tests (`FastAPI`)
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestUserAPI:
    def test_create_user(self):
        response = client.post(
            "/api/v1/users",
            json={
                "email": "test@example.com",
                "name": "Test User"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
    
    def test_get_user(self):
        # Create user first
        create_response = client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "Test"}
        )
        user_id = create_response.json()["id"]
        
        # Get user
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"
    
    def test_get_user_not_found(self):
        response = client.get("/api/v1/users/999")
        assert response.status_code == 404
    
    def test_create_user_duplicate_email(self):
        # Create first user
        client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "Test"}
        )
        
        # Try duplicate
        response = client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "Test 2"}
        )
        assert response.status_code == 409
```python

### API Endpoint Tests (Express/Supertest)
```javascript
const request = require('supertest');
const app = require('../app');

describe('POST /api/v1/users', () => {
  test('create user success', async () => {
    const response = await request(app)
      .post('/api/v1/users')
      .send({
        email: 'test@example.com',
        name: 'Test User'
      });
    
    expect(response.status).toBe(201);
    expect(response.body.email).toBe('test@example.com');
  });
  
  test('create user invalid email', async () => {
    const response = await request(app)
      .post('/api/v1/users')
      .send({ email: 'invalid', name: 'Test' });
    
    expect(response.status).toBe(400);
  });
});
```python

---

## Contract Testing

### Schema Validation
```python
from pydantic import BaseModel, EmailStr, ValidationError

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str
    age: int | None = None

# Test contract
def test_create_user_request_schema():
    # Valid
    valid = CreateUserRequest(email="test@example.com", name="Test")
    assert valid.email == "test@example.com"
    
    # Invalid
    with pytest.raises(ValidationError):
        CreateUserRequest(email="not-email", name="")
```python

### Response Schema Test
```python
def test_user_response_schema():
    response = client.get("/api/v1/users/1")
    data = response.json()
    
    # Check required fields
    assert "id" in data
    assert "email" in data
    assert "name" in data
    assert "created_at" in data
    
    # Check types
    assert isinstance(data["id"], int)
    assert isinstance(data["email"], str)
```python

---

## Load Testing

### k6 Script
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Ramp up
    { duration: '1m', target: 20 },   // Stay at 20
    { duration: '30s', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.01'],    // Less than 1% errors
  },
};

export default function () {
  const res = http.get('http://localhost:8000/api/v1/users');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}
```

### Artillery Config
```yaml
config:
  target: "http://localhost:8000"
  phases:
    - duration: 60
      arrivalRate: 10
    - duration: 120
      arrivalRate: 50

scenarios:
  - name: "Get Users"
    flow:
      - get:
          url: "/api/v1/users"
      - think: 1
      - get:
          url: "/api/v1/users/{{ userId }}"
```

---

## Testing Checklist

### Unit Tests
- [ ] Test happy path
- [ ] Test error cases
- [ ] Test edge cases
- [ ] Mock external dependencies

### Integration Tests
- [ ] Test full request/response cycle
- [ ] Test with real database
- [ ] Test authentication
- [ ] Test authorization

### Contract Tests
- [ ] Validate request schema
- [ ] Validate response schema
- [ ] Test API versioning

### Load Tests
- [ ] Define performance thresholds
- [ ] Test normal load
- [ ] Test peak load
- [ ] Test stress limits

---

## References
- https://docs.pytest.org/
- https://k6.io/docs/
- https://docs.docker.com/compose/testing/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
