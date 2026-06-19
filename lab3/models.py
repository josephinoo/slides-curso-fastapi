from sqlalchemy import Column, String, Float, Integer
from database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Casa(Base):
    __tablename__ = "casas"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    city = Column(String, index=True)
    price_usd = Column(Float, index=True)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    parking_spots = Column(Integer)
    construction_area_sqm = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    link = Column(String)
