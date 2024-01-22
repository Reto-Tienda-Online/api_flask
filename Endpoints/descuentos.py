from fastapi import APIRouter, Depends, HTTPException
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

# PUT REQUEST

@descuentos_bp.put("/descuentos/{descuento_id}")
async def update_descuento(descuento_id: int, updated_descuento: dict, db: Session = Depends(get_db)):
    existing_descuento = db.query(Descuento).filter(Descuento.id == descuento_id).first()

    if existing_descuento is None:
        raise HTTPException(status_code=404, detail="Descuento not found")

    for key, value in updated_descuento.items():
        setattr(existing_descuento, key, value)

    db.commit()
    db.refresh(existing_descuento)

    return {"result": "Descuento updated successfully", "updated_descuento": existing_descuento.__dict__}

# DELETE REQUEST

@descuentos_bp.delete("/descuentos/{descuento_id}")
async def delete_descuento(descuento_id: int, db: Session = Depends(get_db)):
    existing_descuento = db.query(Descuento).filter(Descuento.id == descuento_id).first()

    if existing_descuento is None:
        raise HTTPException(status_code=404, detail="Descuento not found")

    db.delete(existing_descuento)
    db.commit()

    return {"result": "Descuento deleted successfully", "deleted_descuento": existing_descuento.__dict__}