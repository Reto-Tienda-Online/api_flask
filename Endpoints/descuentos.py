from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import Descuento, get_db
from sqlalchemy import Text, text

descuentos_bp = APIRouter()

# GET REQUEST

@descuentos_bp.get("/all_Descuentos")
async def get_descuentos(db: Session = Depends(get_db)):
    query = text('SELECT * FROM descuentos')
    result = db.execute(query)
    descuentos_list = [dict(row._asdict()) for row in result.fetchall()]

    return descuentos_list


# POST REQUEST

@descuentos_bp.post("/descuentos")
async def create_descuento(descuento: dict, db: Session = Depends(get_db)):
    new_descuento = Descuento(**descuento)
    db.add(new_descuento)
    db.commit()
    db.refresh(new_descuento)
    
    return {"result": "Descuento created successfully", **descuento}

