from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import validator

# Base model with shared fields
class GeolocationBase(SQLModel):
    ip: Optional[str] = None
    url: Optional[str] = None
    latitude: float
    longitude: float
    country: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None

# Database model for storing geolocation data
class Geolocation(GeolocationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"

    class Meta:
        ordering = ['-created_at']

# Schema for creating a new geolocation
class GeolocationCreate(GeolocationBase):
    @validator('ip')
    def validate_ip(cls, v):
        if v is None:
            return v
        # Basic IPv4 validation
        parts = v.split('.')
        if len(parts) != 4:
            raise ValueError("Invalid IPv4 address format")
        for part in parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    raise ValueError("IP address parts must be between 0 and 255")
            except ValueError:
                raise ValueError("IP address parts must be integers")
        return v

# Schema for returning geolocation data
class GeolocationResponse(GeolocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 