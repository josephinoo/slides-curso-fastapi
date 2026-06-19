# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict
from typing import Optional

class CasaBase(BaseModel):
    city: str
    price_usd: float
    bedrooms: int
    bathrooms: int
    parking_spots: int
    construction_area_sqm: float
    latitude: float
    longitude: float
    link: Optional[str] = None

class CasaCreate(CasaBase):
    pass

class CasaUpdate(BaseModel):
    city: Optional[str] = None
    price_usd: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    parking_spots: Optional[int] = None
    construction_area_sqm: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    link: Optional[str] = None

class CasaResponse(CasaBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
