from datetime import datetime, timezone
from typing import Optional

from pydantic import model_validator, field_validator, ConfigDict
from sqlmodel import Field, SQLModel


class GeolocationBase(SQLModel):
    model_config = ConfigDict(extra="forbid")

    ip: Optional[str] = None
    url: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None


class Geolocation(GeolocationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"

    class Meta:
        ordering = ["-created_at"]


class GeolocationCreate(SQLModel):
    ip: Optional[str] = None
    url: Optional[str] = None

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        ip = values.get("ip")
        url = values.get("url")
        if not ip and not url:
            raise ValueError("At least one of 'ip' or 'url' must be provided.")
        if ip and url:
            raise ValueError("Use url or ip, not both.")
        return values

    @field_validator("ip")
    def validate_ip(cls, v):
        if v is None:
            return v
        parts = v.split(".")
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


class GeolocationResponse(GeolocationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
