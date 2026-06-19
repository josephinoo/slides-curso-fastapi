# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

import models, schemas
from database import engine, get_db

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Inmobiliaria con SQLAlchemy")

@app.get("/casas/estadisticas")
def estadisticas_casas(db: Session = Depends(get_db)):
    result = db.query(
        func.count(models.Casa.id).label("total_casas"),
        func.avg(models.Casa.price_usd).label("precio_promedio"),
        func.min(models.Casa.price_usd).label("precio_minimo"),
        func.max(models.Casa.price_usd).label("precio_maximo")
    ).first()
    
    return {
        "total_casas": result.total_casas,
        "precio_promedio": result.precio_promedio,
        "precio_minimo": result.precio_minimo,
        "precio_maximo": result.precio_maximo
    }

@app.get("/casas", response_model=List[schemas.CasaResponse])
def listar_casas(
    city: Optional[str] = Query(None),
    price_max: Optional[float] = Query(None),
    bedrooms: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Casa)
    
    if city:
        query = query.filter(models.Casa.city.ilike(f"%{city}%"))
    if price_max is not None:
        query = query.filter(models.Casa.price_usd <= price_max)
    if bedrooms is not None:
        query = query.filter(models.Casa.bedrooms == bedrooms)
        
    return query.all()

@app.get("/casas/{id}", response_model=schemas.CasaResponse)
def detalle_casa(id: str, db: Session = Depends(get_db)):
    casa = db.query(models.Casa).filter(models.Casa.id == id).first()
    if not casa:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    return casa

@app.post("/casas", response_model=schemas.CasaResponse, status_code=201)
def crear_casa(casa: schemas.CasaCreate, db: Session = Depends(get_db)):
    db_casa = models.Casa(**casa.model_dump())
    db.add(db_casa)
    db.commit()
    db.refresh(db_casa)
    return db_casa

@app.put("/casas/{id}", response_model=schemas.CasaResponse)
def actualizar(id: str, updates: schemas.CasaUpdate, db: Session = Depends(get_db)):
    db_casa = db.query(models.Casa).filter(models.Casa.id == id).first()
    if not db_casa:
        raise HTTPException(status_code=404, detail="Casa no encontrada")
        
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_casa, key, value)
        
    db.commit()
    db.refresh(db_casa)
    return db_casa

@app.delete("/casas/{id}", status_code=204)
def eliminar(id: str, db: Session = Depends(get_db)):
    db_casa = db.query(models.Casa).filter(models.Casa.id == id).first()
    if not db_casa:
        raise HTTPException(status_code=404, detail="Casa no encontrada")
        
    db.delete(db_casa)
    db.commit()
    return None
