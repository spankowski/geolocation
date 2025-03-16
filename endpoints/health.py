from fastapi import APIRouter
from typing import Dict

router = APIRouter()


@router.get("/", response_model=Dict[str, str])
def health_check():
    """Health check endpoint to verify the service is running"""
    return {"status": "ok"}
