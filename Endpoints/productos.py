from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Models.models import Producto, get_db
from sqlalchemy import Text, text, and_

productos_bp = APIRouter()

@productos_bp.get("/search")
async def buscar_producto(producto: str = Query(None), db: Session = Depends(get_db)):
    conditions = []
    params = {}

    if producto:
        conditions.append("producto LIKE :producto")
        params["producto"] = f"%{producto}%"

    query = text('SELECT * FROM productos')
    
    if conditions:
        query = text(str(query) + " WHERE " + " AND ".join(conditions))

    result = db.execute(query, params)
    productos_list = [dict(row._asdict()) for row in result.fetchall()]

    return productos_list

@productos_bp.get("/all_productos")
async def get_productos(id: int = Query(None), producto: str = Query(None), db: Session = Depends(get_db)):
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id
        
    if producto is not None:
        conditions.append("producto = :producto")
        params['producto'] = producto
    
    query = text('SELECT * FROM productos')
    if conditions:
        query = text(str(query) + " WHERE " + " AND ".join(conditions))

    result = db.execute(query, params)
    categorias_list = [dict(row._asdict()) for row in result.fetchall()]

    return categorias_list

@productos_bp.post("/create_producto")
async def create_producto(producto_data: dict, db: Session = Depends(get_db)):
    try:
        new_producto = Producto(**producto_data)
        db.add(new_producto)
        db.commit()
        db.refresh(new_producto)
        return {"message": "Producto created successfully", "data": new_producto}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


