from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Models.models import Producto, get_db
from sqlalchemy import Text, text, and_
from pydantic import BaseModel

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

    query = text('SELECT productos.*, plataforma.plataforma as nombreplataforma FROM productos LEFT JOIN plataforma ON productos.id_plataforma = plataforma.id')
    if conditions:
        query = text(str(query) + " WHERE " + " AND ".join(conditions))

    result = db.execute(query, params)
    productos_list = [dict(row._asdict()) for row in result.fetchall()]

    return productos_list

class ProductoCreate(BaseModel):
    producto: str
    precio_unitario: str
    id_descuento: int
    id_plataforma: int
    rutavideo: str
    iframetrailer: str
    descripcion: str
    
    
@productos_bp.post("/create_producto")
async def create_producto(producto_create: ProductoCreate, db: Session = Depends(get_db)):
    new_producto = Producto(
        producto=producto_create.producto,
        precio_unitario=producto_create.precio_unitario,
        id_descuento=producto_create.id_descuento,
        id_plataforma=producto_create.id_plataforma,
        rutavideo=producto_create.rutavideo,
        iframetrailer=producto_create.iframetrailer,
        descripcion=producto_create.descripcion
    )

    db.add(new_producto)
    db.commit()
    db.refresh(new_producto)

    return new_producto

@productos_bp.put("/update_producto/{producto_id}")
async def update_producto(producto_id: int, producto_update: ProductoCreate, db: Session = Depends(get_db)):
    # Check if the product exists
    existing_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if existing_producto is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update the product fields
    existing_producto.producto = producto_update.producto
    existing_producto.precio_unitario = producto_update.precio_unitario
    existing_producto.id_descuento = producto_update.id_descuento
    existing_producto.id_plataforma = producto_update.id_plataforma
    existing_producto.rutavideo = producto_update.rutavideo
    existing_producto.iframetrailer = producto_update.iframetrailer
    existing_producto.descripcion = producto_update.descripcion

    # Commit the changes to the database
    db.commit()

    # Return the updated product
    return existing_producto
