from datetime import date, time
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Visit


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SIU Visitas API",
    description="API para el registro de visitas a colegios",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Schemas
# -------------------------

class VisitCreate(BaseModel):
    colegio: str
    ubicacion: str
    distrito: str
    distritoOtro: Optional[str] = None
    estudiantes: int
    dia: date
    hora: time
    persona: str
    observacion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None


class VisitResponse(VisitCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

# -------------------------
# General
# -------------------------

@app.get("/")
def root():
    return {
        "message": "SIU Visitas API funcionando"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# -------------------------
# CREATE
# -------------------------

@app.post("/visits", response_model=VisitResponse)
def create_visit(
    visit: VisitCreate,
    db: Session = Depends(get_db),
):
    new_visit = Visit(
        nombre_colegio=visit.colegio,
        ubicacion=visit.ubicacion,
        distrito=visit.distrito,
        cantidad_estudiantes=visit.estudiantes,
        dia=visit.dia,
        hora=visit.hora,
        nombre_persona=visit.persona,
        observacion=visit.observacion,
        latitud=visit.latitud,
        longitud=visit.longitud,
    )

    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)

    return {
        "id": new_visit.id,
        "colegio": new_visit.nombre_colegio,
        "ubicacion": new_visit.ubicacion,
        "distrito": new_visit.distrito,
        "distritoOtro": visit.distritoOtro,
        "estudiantes": new_visit.cantidad_estudiantes,
        "dia": new_visit.dia,
        "hora": new_visit.hora,
        "persona": new_visit.nombre_persona,
        "observacion": new_visit.observacion,
        "latitud": new_visit.latitud,
        "longitud": new_visit.longitud,
    }


# -------------------------
# READ ALL
# -------------------------

@app.get("/visits", response_model=list[VisitResponse])
def get_visits(
    db: Session = Depends(get_db),
):
    visits = db.query(Visit).all()

    return [
        {
            "id": v.id,
            "colegio": v.nombre_colegio,
            "ubicacion": v.ubicacion,
            "distrito": v.distrito,
            "distritoOtro": None,
            "estudiantes": v.cantidad_estudiantes,
            "dia": v.dia,
            "hora": v.hora,
            "persona": v.nombre_persona,
            "observacion": v.observacion,
            "latitud": v.latitud,
            "longitud": v.longitud,
        }
        for v in visits
    ]

# -------------------------
# READ ONE
# -------------------------

@app.get("/visits/{visit_id}", response_model=VisitResponse)
def get_visit(
    visit_id: int,
    db: Session = Depends(get_db),
):
    visit = db.query(Visit).filter(
        Visit.id == visit_id
    ).first()

    if visit is None:
        raise HTTPException(
            status_code=404,
            detail="Visita no encontrada",
        )

    return {
        "id": visit.id,
        "colegio": visit.nombre_colegio,
        "ubicacion": visit.ubicacion,
        "distrito": visit.distrito,
        "distritoOtro": None,
        "estudiantes": visit.cantidad_estudiantes,
        "dia": visit.dia,
        "hora": visit.hora,
        "persona": visit.nombre_persona,
        "observacion": visit.observacion,
        "latitud": visit.latitud,
        "longitud": visit.longitud,
    }

# -------------------------
# UPDATE
# -------------------------

@app.put("/visits/{visit_id}", response_model=VisitResponse)
def update_visit(
    visit_id: int,
    updated_visit: VisitCreate,
    db: Session = Depends(get_db),
):
    visit = db.query(Visit).filter(
        Visit.id == visit_id
    ).first()

    if visit is None:
        raise HTTPException(
            status_code=404,
            detail="Visita no encontrada",
        )

    visit.nombre_colegio = updated_visit.colegio
    visit.ubicacion = updated_visit.ubicacion
    visit.distrito = updated_visit.distrito
    visit.cantidad_estudiantes = updated_visit.estudiantes
    visit.dia = updated_visit.dia
    visit.hora = updated_visit.hora
    visit.nombre_persona = updated_visit.persona
    visit.observacion = updated_visit.observacion
    visit.latitud = updated_visit.latitud
    visit.longitud = updated_visit.longitud

    db.commit()
    db.refresh(visit)

    return {
        "id": visit.id,
        "colegio": visit.nombre_colegio,
        "ubicacion": visit.ubicacion,
        "distrito": visit.distrito,
        "distritoOtro": updated_visit.distritoOtro,
        "estudiantes": visit.cantidad_estudiantes,
        "dia": visit.dia,
        "hora": visit.hora,
        "persona": visit.nombre_persona,
        "observacion": visit.observacion,
        "latitud": visit.latitud,
        "longitud": visit.longitud,
    }

# -------------------------
# DELETE
# -------------------------

@app.delete("/visits/{visit_id}")
def delete_visit(
    visit_id: int,
    db: Session = Depends(get_db),
):
    visit = db.query(Visit).filter(
        Visit.id == visit_id
    ).first()

    if visit is None:
        raise HTTPException(
            status_code=404,
            detail="Visita no encontrada",
        )

    db.delete(visit)
    db.commit()

    return {
        "message": "Visita eliminada correctamente",
        "id": visit_id,
    }