from app.api.v1 import auth, tasks
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(tasks.router)
