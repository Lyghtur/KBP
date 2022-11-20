from fastapi import APIRouter

from . import practice


router = APIRouter(prefix="/v1", tags=["v1"])


router.include_router(practice.router)
