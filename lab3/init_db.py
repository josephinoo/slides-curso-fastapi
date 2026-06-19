import csv
import os
from database import engine, SessionLocal, Base
from models import Casa

CSV_PATH = "../plusvalia_filtered.csv"

def init_db():
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if we already have data
    if db.query(Casa).first():
        print("La base de datos ya contiene datos.")
        db.close()
        return
        
    print(f"Cargando datos desde {CSV_PATH}...")
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        casas_data = list(reader)
        
    nuevas_casas = []
    for data in casas_data:
        casa = Casa(
            id=data["ID"],
            city=data["CITY"],
            price_usd=float(data["PRICE_USD"]) if data["PRICE_USD"] else None,
            bedrooms=int(float(data["BEDROOMS"])) if data["BEDROOMS"] else None,
            bathrooms=int(float(data["BATHROOMS"])) if data["BATHROOMS"] else None,
            parking_spots=int(float(data["PARKING_SPOTS"])) if data["PARKING_SPOTS"] else None,
            construction_area_sqm=float(data["CONSTRUCTION_AREA_SQM"]) if data["CONSTRUCTION_AREA_SQM"] else None,
            latitude=float(data["LATITUDE"]) if data["LATITUDE"] else None,
            longitude=float(data["LONGITUDE"]) if data["LONGITUDE"] else None,
            link=data["LINK"]
        )
        nuevas_casas.append(casa)
        
    # Bulk save is faster
    db.bulk_save_objects(nuevas_casas)
    db.commit()
    print(f"Éxito: Se migraron {len(nuevas_casas)} casas usando SQLAlchemy.")
    db.close()

if __name__ == "__main__":
    init_db()
