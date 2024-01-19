from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import Descuento, get_db
from sqlalchemy import Text, text

descuentos_bp = APIRouter()

@descuentos_bp.get("/descuentos")
async def get_descuentos(db: Session = Depends(get_db)):
    query = text('SELECT * FROM descuentos')
    result = db.execute(query)

    # Fetch all rows as a list of dictionaries
    descuentos_list = [dict(row._asdict()) for row in result.fetchall()]

    return descuentos_list
