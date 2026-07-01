from app.api.v1.router import api_router
from app.core.config import settings
from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Production API Starter",
    description="Tasks API with JWT auth, async SQLAlchemy, and OpenAPI docs.",
    version="0.1.0",
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
