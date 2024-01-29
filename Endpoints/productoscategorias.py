from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from Models.models import ProductoCategoria, get_db, Producto
from sqlalchemy import Text, text

productoscategorias_bp = APIRouter()

@productoscategorias_bp.get("/producto_categoria")
async def read_producto_categoria(
    id_producto: int = Query(None, description="Filter by producto id"),
    id_categoria: int = Query(None, description="Filter by categoria id"),
    db: Session = Depends(get_db)
):
    query = db.query(ProductoCategoria)

    if id_producto is not None:
        query = query.filter(ProductoCategoria.id_producto == id_producto)

    if id_categoria is not None:
        query = query.filter(ProductoCategoria.id_categoria == id_categoria)

    producto_categorias = query.all()

    if not producto_categorias:
        raise HTTPException(status_code=404, detail="No matching ProductoCategoria found")

    combined_data_list = []

    for producto_categoria in producto_categorias:
        producto_data = db.query(Producto).filter(Producto.id == producto_categoria.id_producto).first()

        if producto_data is not None:
            combined_data = {
                "producto_categoria_id": producto_categoria.id,
                "id_producto": producto_categoria.id_producto,
                "id_categoria": producto_categoria.id_categoria,
                "producto_data": {
                    "producto_id": producto_data.id,
                    "producto_name": producto_data.producto,
                }
            }
            combined_data_list.append(combined_data)

    return combined_data_list