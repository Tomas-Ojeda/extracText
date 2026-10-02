from fastapi import APIRouter

from app.api.v1 import extract

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(extract.router)
