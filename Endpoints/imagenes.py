from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from Models.models import get_db
from sqlalchemy import text

imagenes_bp = APIRouter()

@imagenes_bp.get("/imagenes")
async def get_categorias(id: int = Query(None), rutaimagen: str = Query(None), db: Session = Depends(get_db)):
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id
        
    if rutaimagen is not None:
        conditions.append("rutaimagen = :rutaimagen")
        params['rutaimagen'] = rutaimagen
    
    query = text('SELECT * FROM imagenes')
    if conditions:
        query = text(str(query) + " WHERE " + " AND ".join(conditions))

    result = db.execute(query, params)
    categorias_list = [dict(row._asdict()) for row in result.fetchall()]

    return categorias_list
