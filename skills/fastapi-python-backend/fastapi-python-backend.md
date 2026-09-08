# `FastAPI` Python Backend

## Tujuan

Membangun REST API Python yang aman, teruji, dan siap produksi dengan `FastAPI` + Pydantic v2 + `SQLAlchemy` 2.0 async.

## Prasyarat

- Python 3.11+
- Pemahaman dasar HTTP/REST dan asyncio

## Konsep inti

1. **Pydantic v2** — validasi input/output dan serialisasi; gunakan `model_config = ConfigDict(from_attributes=True)` untuk ORM.
2. **Dependency Injection** — `Depends()` untuk auth, DB session, dan komponen yang bisa di-mock saat testing.
3. **Async DB** — `SQLAlchemy` 2.0 `AsyncSession` + `asyncpg`; jangan blokir event loop dengan I/O sinkron.
4. **Error handling** — exception handler global agar format error konsisten; jangan bocorkan detail internal.
5. **Pagination** — berbasis cursor untuk dataset besar, offset untuk dataset kecil.
6. **Background tasks** — gunakan task queue nyata (Celery/ARQ) untuk pekerjaan yang butuh retry; `BackgroundTasks` hanya untuk pekerjaan ringan.

## Struktur proyek (contoh)

```text
app/
├── main.py            # `FastAPI` instance + router mounting
├── config.py          # Settings (pydantic-settings) dari env
├── api/
│   └── v1/
│       ├── router.py
│       └── endpoints/
│           └── users.py
├── core/
│   ├── db.py          # Async engine + session factory
│   └── security.py    # hashing, JWT
├── models/            # `SQLAlchemy` models
├── schemas/           # Pydantic schemas
└── services/          # business logic
```python

## Contoh dasar

```python
# app/main.py
from fastapi import `FastAPI`
from app.api.v1.router import api_router

app = `FastAPI`(title="Example API", version="1.0.0")
app.include_router(api_router, prefix="/api/v1")
```python

```python
# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.services import users as user_service
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_session)):
    user = await user_service.create_user(db, payload)
    return user
```

## Checklist produksi

- [ ] `pydantic-settings` untuk konfigurasi; tidak ada secret di kode
- [ ] CORS dikonfigurasi eksplisit sesuai domain yang diizinkan
- [ ] Rate limiting di balik reverse proxy atau middleware (slowapi)
- [ ] `response_model` eksplisit di semua endpoint (tidak membocorkan field)
- [ ] SQL parameterized — jangan string interpolation query
- [ ] Exception handler global; log error dengan konteks (request id)
- [ ] Migrasi dengan Alembic; schema database tidak dibuat manual
- [ ] Test: unit (pydantic/validator), integration (TestClient + DB test), minimal 1 happy path + 2 edge case
- [ ] Health endpoint `/healthz` tanpa auth untuk orchestrator
- [ ] Dependency ter-pin dan audit rutin (`pip-audit`)

## Kesalahan umum

- Memakai `async def` tetapi memanggil fungsi DB sinkron di dalamnya.
- Menaruh logic berat di endpoint, bukan di service layer.
- `from_attributes` tidak diaktifkan sehingga ORM object gagal serialisasi.
- Menangkap semua exception lalu mengembalikan 200 — mask error.
- Tanpa pagination; endpoint list memuat seluruh tabel.

## Trade-off dan Kapan Tidak Pakai

- `FastAPI` is fast to build but async adds complexity — sync endpoints are fine for I/O-bound work.
- Pydantic v2 is faster but has migration cost — plan it.
- Starlette's test client is sync — async tests need care.

## Referensi

- https://fastapi.tiangolo.com/ — dokumentasi resmi
- https://docs.pydantic.dev/ — Pydantic v2
- https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html — async `SQLAlchemy`

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
