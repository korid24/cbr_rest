from fastapi import APIRouter

from .endpoints.routes import router

api_router = APIRouter()
api_router.include_router(
    router,
    tags=['rate-conversion'],
)
