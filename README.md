# RecordVault API

A **FastAPI** service with **SQLAlchemy**, **JWT** authentication, **dependency injection** for route protection, and **Pydantic** models for request validation.

## Tech stack

- **FastAPI** — HTTP API and dependency injection
- **Pydantic v2** — request/response validation
- **PyJWT** — access tokens (`HS256`)
- **SQLAlchemy 2** — database access
- **Uvicorn** — ASGI server

## Prerequisites

- Python 3.10+ (recommended)
- A PostgreSQL (or other) database URL compatible with SQLAlchemy

## Setup

1. **Clone the repository** and create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment variables** — create a `.env` file in the project root:

   | Variable        | Purpose                           |
   |-----------------|-----------------------------------|
   | `DATABASE_URL`  | SQLAlchemy engine URL             |
   | `SECRET_KEY`    | Symmetric key for signing JWTs    |
   | `admin_name`    | Admin Name For Creting Admin      |
   | `admin_password`| Admin password For Creting Admin  |
   | `admin_email`   | Admin email For Creting Admin     |

4. **Database tables** are created on application startup (`Base.metadata.create_all` in `app/main.py`).

5. **Create an admin user** — edit placeholders in `create_admin.py`, then run:

   ```bash
   python create_admin.py
   ```

6. **Run the API**:

   ```bash
   uvicorn run:app --reload
   ```

   Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API layout

| Prefix    | Tag      | Purpose                    |
|-----------|----------|----------------------------|
| `/users`  | `users`  | Login, user CRUD (role-gated) |
| `/records`| `records`| Financial-style records    |

---

## How routes are protected (dependency injection)

Protection is implemented in `dependencies/depends.py` and wired into route handlers with FastAPI’s **`Depends()`**.

### 1. Bearer token extraction

`HTTPBearer()` reads the **`Authorization: Bearer <token>`** header. Any route that depends on `get_current_user` implicitly requires a valid bearer token.

### 2. `get_current_user`

- Depends on **`HTTPBearer()`** to obtain the raw JWT.
- Calls **`verify_token()`** (`auth/jwt_token.py`) to decode and validate the token (signature, expiry).
- If the token is missing, invalid, or expired → **`401`** with `"Invalid Token"`.
- On success, returns the **JWT payload** (e.g. `user_id`, `role`).

### 3. `is_admin`

- Depends on **`get_current_user`**.
- If `user["role"] != "admin"` → **`403`** with `"not enough permission"`.
- Otherwise returns `True`. Admin-only handlers use `Depends(is_admin)` so only admins pass through.

**Example** (`apis/v1/users.py`): creating, updating, deleting users and listing users all use `Depends(is_admin)`.

### 4. `require_role(*roles)`

A **factory** that returns an inner dependency:

- Inner dependency again depends on **`get_current_user`**.
- If `user["role"]` is not in the allowed `roles` → **`403`** `"Forbidden"`.
- If allowed, returns the **full user payload** (so handlers can read `user_id`, etc.).

**Example** (`apis/v1/records.py`):

- `GET /records/summary` — `Depends(require_role("user", "admin", "analyst"))`
- `GET /records/` — `Depends(require_role("analyst", "admin"))`
- Mutations on records — `Depends(is_admin)` (admin only)

### 5. Public vs protected routes

- **`POST /users/login`** — no `Depends` auth dependency; accepts credentials and issues a JWT after successful login.
- All other user/record endpoints listed above require the appropriate dependency chain before the route body runs.

This pattern keeps **auth and authorization out of business logic**: services receive a flag or user context only after FastAPI has already enforced the dependency.

---

## How input is validated (Pydantic)

Request bodies (and compatible parameters) are declared with **Pydantic `BaseModel` subclasses** in `schemas/`. FastAPI uses them to:

1. **Parse** JSON into Python objects.
2. **Validate** types and required fields.
3. Return **`422 Unprocessable Entity`** with a structured error payload when validation fails.

### User schemas (`schemas/user_schemas.py`)

| Model        | Used for              | Notes                                      |
|-------------|------------------------|--------------------------------------------|
| `Login`     | Login                  | `user_email`, `user_password`              |
| `adduser`   | Create user            | Name, email, password, role, status        |
| `Updateuser`| Update user            | Optional `new_role`, `new_status`          |
| `GetUsers`  | Filter/list users      | Optional `role`, `status`                  |

### Record schemas (`schemas/records_schemas.py`)

| Model          | Used for    | Notes                                                |
|----------------|-------------|------------------------------------------------------|
| `addrecords`   | Create      | `user_id`, `type`, `category`, `amount`, dates, etc. |
| `updaterecords`| Update      | `user_id` plus optional fields                     |
| `getrecords`   | List/filter | Optional `type`, `category`                         |

Using **`Optional[...] = None`** marks fields that may be omitted; required fields must be present and correctly typed (e.g. `amount: float`, `create_date: datetime`), which Pydantic enforces automatically.

---

## Project structure (overview)

```
app/main.py           # FastAPI app, routers, startup (DB tables)
run.py                # ASGI entry: `uvicorn run:app`
apis/v1/              # Route modules (users, records)
dependencies/depends.py # JWT + role dependencies
auth/jwt_token.py     # Create / verify JWT
schemas/              # Pydantic models
services/             # Business logic
models/               # SQLAlchemy models / DB helpers
repo/db.py            # Engine and session factory
```

---

## Security notes

- Keep **`SECRET_KEY`** long, random, and private in production.
- Prefer **HTTPS** in production so bearer tokens are not sent in clear text.
- Tokens expire after **1 hour** (see `create_token` in `auth/jwt_token.py`).
