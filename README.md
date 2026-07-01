# FastAPI Production API Starter

![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)

A small but realistic FastAPI service showing patterns I use on client projects:
async SQLAlchemy, JWT auth, versioned routes, OpenAPI docs, Docker, and pytest.

Not a tutorial CRUD — structured for teams that need to extend it.

## Features

- FastAPI + Pydantic v2 + async SQLAlchemy 2.0
- JWT authentication (register / login / me)
- Paginated, filterable task endpoints
- Alembic migrations
- Docker Compose (API + PostgreSQL)
- pytest + httpx integration tests
- OpenAPI at `/docs`

## Quick start

```bash
git clone https://github.com/sparkscribe/fastapi-production-api-starter.git
cd fastapi-production-api-starter
cp .env.example .env
docker compose up --build
# Open http://localhost:8000/docs
```

### Local development (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Start PostgreSQL and set DATABASE_URL in .env
alembic upgrade head
uvicorn app.main:app --reload
```

Run tests:

```bash
pytest
```

## Project layout

```
app/
├── main.py              # FastAPI app + health route
├── core/                # config, database, security
├── models/              # SQLAlchemy models (User, Task)
├── schemas/             # Pydantic request/response models
├── api/
│   ├── deps.py          # auth + DB dependencies
│   └── v1/              # versioned routes
└── services/            # query/business logic
alembic/                 # migrations
tests/                   # pytest integration tests
```

## Design notes

- **Versioned API** — routes live under `/api/v1` so you can ship breaking changes without breaking clients.
- **Dependency injection** — `get_db` and `get_current_user` keep route handlers thin.
- **Session per request** — one async SQLAlchemy session per HTTP request, committed in the service layer.
- **Service layer** — pagination and filtering live in `task_service.py`, not in route handlers.
- **Typical next step** — deploy behind a reverse proxy (nginx/Caddy), add refresh tokens, and wire CI to run migrations + tests.

## Author

<table>
  <tr>
    <td><strong>Name</strong></td>
    <td>Ankit Vaghani</td>
  </tr>
  <tr>
    <td><strong>Organization</strong></td>
    <td><a href="https://sparkscribetech.com">SparkScribe Technologies</a></td>
  </tr>
  <tr>
    <td><strong>GitHub</strong></td>
    <td><a href="https://github.com/vaghaniankit">@vaghaniankit</a> · <a href="https://github.com/SparkScribe">@SparkScribe</a></td>
  </tr>
  <tr>
    <td><strong>LinkedIn</strong></td>
    <td><a href="https://www.linkedin.com/in/ankit-vaghani/">linkedin.com/in/ankit-vaghani</a></td>
  </tr>
  <tr>
    <td><strong>Website</strong></td>
    <td><a href="https://sparkscribetech.com">sparkscribetech.com</a></td>
  </tr>
</table>

Built and maintained by **Ankit Vaghani** · [SparkScribe Technologies](https://sparkscribetech.com)

---

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Ankit Vaghani, SparkScribe Technologies.