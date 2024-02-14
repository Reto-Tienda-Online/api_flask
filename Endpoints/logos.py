from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from Models.models import get_db
from sqlalchemy import text

logos_bp = APIRouter()

@logos_bp.get("/logos")
async def get_logos(id: int = Query(None), rutalogo: str = Query(None), db: Session = Depends(get_db)):
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id
        
    if rutalogo is not None:
        conditions.append("rutalogo = :rutalogo")
        params['rutalogo'] = rutalogo
    
    query = text('SELECT * FROM logos')
    if conditions:
        query = text(str(query) + " WHERE " + " AND ".join(conditions))

    result = db.execute(query, params)
    logos_list = [dict(row._asdict()) for row in result.fetchall()]

    return logos_list
