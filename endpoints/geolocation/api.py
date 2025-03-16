from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Dict

from core.database import get_async_db
from endpoints.geolocation.models import (
    Geolocation,
    GeolocationCreate,
    GeolocationResponse,
)
from services.geolocation import fetch_geolocation, get_ip_from_domain, get_domain_from_ip

router = APIRouter()


@router.post("/", response_model=GeolocationResponse)
async def add_geolocation(
    data: GeolocationCreate, db: AsyncSession = Depends(get_async_db)
):
    if data.url:
        data.ip = get_ip_from_domain(data.url)
    if data.ip is None:
        raise HTTPException(status_code=400, detail="DONS lookup failed")
    # todo: check if ip already in db
    geolocation_data = await fetch_geolocation(ip=data.ip, domain=data.url if data.url else None)
    if not geolocation_data:
        raise HTTPException(status_code=400, detail="Could not fetch geolocation data")

    # Save to DB
    geo_entry = Geolocation(**geolocation_data)
    db.add(geo_entry)
    await db.commit()
    await db.refresh(geo_entry)
    return geo_entry


@router.get("/{query}", response_model=GeolocationResponse)
async def get_geolocation(query: str, db: AsyncSession = Depends(get_async_db)):
    statement = select(Geolocation).where(
        (Geolocation.ip == query) | (Geolocation.url == query)
    )
    result = await db.execute(statement)
    geo_entry = result.scalars().first()
    if not geo_entry:
        raise HTTPException(status_code=404, detail="Geolocation data not found")
    return geo_entry


@router.delete("/{query}", response_model=Dict[str, str])
async def delete_geolocation(id: int, db: AsyncSession = Depends(get_async_db)):
    statement = select(Geolocation).where((Geolocation.id == id))
    result = await db.execute(statement)
    geo_entry = result.scalars().first()
    if not geo_entry:
        raise HTTPException(status_code=404, detail="Geolocation data not found")

    await db.delete(geo_entry)
    await db.commit()
    return {"message": "Geolocation data deleted"}
