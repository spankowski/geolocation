from endpoints.geolocation import api
from endpoints.geolocation import api
from fastapi import APIRouter

from endpoints import health

api_router = APIRouter()
api_router.include_router(api.router, prefix="/geolocation", tags=["geolocation"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
