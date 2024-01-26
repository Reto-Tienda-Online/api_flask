from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from Models.models import Plataforma, get_db
from sqlalchemy import Text, text

plataforma_bp = APIRouter()

@plataforma_bp.get("/all_plataformas")
async def get_categorias(id: int = Query(None), plataforma: str = Query(None), db: Session = Depends(get_db)):
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id
        
    if plataforma is not None:
        conditions.append("plataforma = :plataforma")
        params['plataforma'] = plataforma
    
    query = text('SELECT * FROM plataforma')
    if conditions:
        query = text(str(query) + " WHERE " + " AND ".join(conditions))

    result = db.execute(query, params)
    plataforma_list = [dict(row._asdict()) for row in result.fetchall()]

    return plataforma_list
