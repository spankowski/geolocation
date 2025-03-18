from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Geolocation


async def get_geolocation_or_404(db: AsyncSession, id: int) -> Geolocation:
    """Retrieves a Geolocation object by its ID, or raises a 404 error."""
    statement = select(Geolocation).where(Geolocation.id == id)
    geo_entry = (await db.execute(statement)).scalar_one_or_none()
    if geo_entry is None:
        raise HTTPException(
            status_code=404, detail=f"Geolocation with ID {id} not found"
        )
    return geo_entry
