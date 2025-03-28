from fastapi import APIRouter

from .v1 import tron_router

api_router = APIRouter()

api_router.include_router(tron_router, prefix="/v1/tron", tags=["tron"])