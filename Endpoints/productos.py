from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Models.models import Producto, get_db
from sqlalchemy import Text, text, and_
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path

productos_bp = APIRouter()

@productos_bp.get("/search")
async def buscar_producto(producto: str = Query(None), db: Session = Depends(get_db)):
    conditions = []
    params = {}

    if producto:
        conditions.append("producto LIKE :producto")
        params["producto"] = f"%{producto}%"

    query = text('''
        SELECT productos.*, plataforma.plataforma as nombreplataforma
        FROM productos
        LEFT JOIN plataforma ON productos.id_plataforma = plataforma.id
    ''')

    
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
        conditions.append("productos.id = :id")
        params['id'] = id

    if producto is not None:
        conditions.append("productos.producto = :producto")
        params['producto'] = producto

    query = text('''
        SELECT productos.*, plataforma.plataforma as nombreplataforma, categorias.categoria as nombrecategoria
        FROM productos
        LEFT JOIN plataforma ON productos.id_plataforma = plataforma.id
        LEFT JOIN producto_categoria ON productos.id = producto_categoria.id_producto
        LEFT JOIN categorias ON producto_categoria.id_categoria = categorias.id
    ''')

    if conditions:
        query = text(str(query) + " WHERE " + " AND ".join(conditions))

    result = db.execute(query, params)
    productos_list = [dict(row._asdict()) for row in result.fetchall()]

    return productos_list


@productos_bp.get("/productoresena")
async def buscar_producto(producto_id: int = Query(None), db: Session = Depends(get_db)):
    conditions = []
    params = {}

    if producto_id is not None:
        conditions.append("id_juego = :producto_id")
        params["producto_id"] = producto_id

    query = text('SELECT * FROM resena')
    
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


upload_dir = Path('/var/www/web/frontend/reto_final/public/imgs/juegos')
upload_dir.mkdir(exist_ok=True)

@productos_bp.post("/upload")
async def create_upload_file(id_juego: int, file: UploadFile = File(...)):
    file_path = upload_dir / str(id_juego) / file.filename
    file_path.parent.mkdir(parents=True, exist_ok=True)  # Create parent directories if not exist

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "file_path": str(file_path)}


class ProductoUpdate(BaseModel):
    producto: Optional[str] = None
    precio_unitario: Optional[str] = None
    id_descuento: Optional[int] = None
    id_plataforma: Optional[int] = None
    rutavideo: Optional[str] = None
    iframetrailer: Optional[str] = None
    descripcion: Optional[str] = None
    

@productos_bp.put("/update_producto/{producto_id}")
async def update_producto(producto_id: int, producto_update: ProductoUpdate, db: Session = Depends(get_db)):
    existing_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if existing_producto is None:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_producto.producto = producto_update.producto
    existing_producto.precio_unitario = producto_update.precio_unitario

    existing_producto.rutavideo = producto_update.rutavideo
    existing_producto.iframetrailer = producto_update.iframetrailer
  

    db.commit()

    return existing_producto


@productos_bp.delete("/productos/{producto_id}")
async def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM resena WHERE id_juego = :producto_id"), {"producto_id": producto_id})

    result = db.execute(text("DELETE FROM productos WHERE id = :producto_id"), {"producto_id": producto_id})

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    db.commit()

    return {"result": "Product deleted successfully", "deleted_producto_id": producto_id}