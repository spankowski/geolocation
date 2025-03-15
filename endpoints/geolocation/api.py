from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Dict

from core.database import get_db
from endpoints.geolocation.models import Geolocation, GeolocationCreate, GeolocationResponse
from services.geolocation import fetch_geolocation

router = APIRouter()

@router.post("/", response_model=GeolocationResponse)
def add_geolocation(data: GeolocationCreate, db: Session = Depends(get_db)):
    # Fetch geolocation data
    geolocation_data = fetch_geolocation(data.ip_or_url)
    if not geolocation_data:
        raise HTTPException(status_code=400, detail="Could not fetch geolocation data")
    
    # Save to DB
    geo_entry = Geolocation(**geolocation_data)
    db.add(geo_entry)
    db.commit()
    db.refresh(geo_entry)
    return geo_entry

@router.get("/{query}", response_model=GeolocationResponse)
def get_geolocation(query: str, db: Session = Depends(get_db)):
    statement = select(Geolocation).where(
        (Geolocation.ip == query) | (Geolocation.url == query)
    )
    geo_entry = db.exec(statement).first()
    if not geo_entry:
        raise HTTPException(status_code=404, detail="Geolocation data not found")
    return geo_entry

@router.delete("/{query}", response_model=Dict[str, str])
def delete_geolocation(query: str, db: Session = Depends(get_db)):
    statement = select(Geolocation).where(
        (Geolocation.ip == query) | (Geolocation.url == query)
    )
    geo_entry = db.exec(statement).first()
    if not geo_entry:
        raise HTTPException(status_code=404, detail="Geolocation data not found")
    
    db.delete(geo_entry)
    db.commit()
    return {"message": "Geolocation data deleted"} 