from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.models import Resena, get_db
from sqlalchemy import Text, text

resena_bp = APIRouter()


@resena_bp.get("/resena/{juego_id}")
async def read_resena(juego_id: int, db: Session = Depends(get_db)):
    resena = db.query(Resena).filter(Resena.id_juego == juego_id).first()
    if resena is None:
        raise HTTPException(status_code=404, detail="Resena not found")
    return resena
