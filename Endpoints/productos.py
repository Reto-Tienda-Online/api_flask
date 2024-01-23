from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.models import Producto, get_db
from sqlalchemy import Text, text

productos_bp = APIRouter()

@productos_bp.get("/all_productos")
async def get_productos(db: Session = Depends(get_db)):
    query = text('SELECT * FROM productos')
    result = db.execute(query)
    productos_list = [dict(row._asdict()) for row in result.fetchall()]

    return productos_list


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


