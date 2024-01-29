from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.models import Resena, get_db, Usuario, Producto
from sqlalchemy import Text, text

resena_bp = APIRouter()


@resena_bp.get("/resena/{juego_id}")
async def read_resena(juego_id: int, db: Session = Depends(get_db)):
    resena = db.query(Resena).filter(Resena.id_juego == juego_id).first()
    if resena is None:
        raise HTTPException(status_code=404, detail="Resena not found")
    return resena


@resena_bp.post("/resenas/", response_model=dict)
async def create_resena(resena_data: dict, db: Session = Depends(get_db)):
    # Create Resena
    new_resena = Resena(**resena_data)
    db.add(new_resena)
    db.commit()
    db.refresh(new_resena)

    # Convert the SQLAlchemy model instance to a dictionary
    created_resena_dict = {**new_resena.__dict__}
    # Remove the '_sa_instance_state' key, which causes the serialization issue
    created_resena_dict.pop('_sa_instance_state', None)

    return {"result": "Resena created successfully", "created_resena": created_resena_dict}