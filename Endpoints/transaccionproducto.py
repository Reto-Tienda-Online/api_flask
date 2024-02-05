from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.models import TransaccionProducto, get_db, Producto, Transaccion
from sqlalchemy import Text, text, func, join

transaccionproducto_bp = APIRouter()


'''@transaccionproducto_bp.get("/all_compras")
async def read_transaccionproducto( db: Session = Depends(get_db)):
    transaccionproductos = db.query(TransaccionProducto).all()
    if not transaccionproductos:
        raise HTTPException(status_code=404, detail="TransaccionProducto not found")
    return transaccionproductos'''


@transaccionproducto_bp.get("/all_compras")
async def read_transaccionproducto(db: Session = Depends(get_db)):
    results = db.query(
        Producto.id,
        Producto.producto,
        func.sum(TransaccionProducto.cantidad).label('cantidad'),
        func.sum(TransaccionProducto.precio).label('importe')
    ).join(TransaccionProducto).group_by(Producto.id).all()

    if not results:
        raise HTTPException(status_code=404, detail="Sales not found")

    grouped_sales = [
        {
            'id_producto': result.id,
            'producto': result.producto,
            'cantidad': result.cantidad,
            'importe': result.importe
        }
        for result in results
    ]

    return grouped_sales



@transaccionproducto_bp.get("/compras_usuario/{id_usuario}")
async def read_compras_by_usuario(id_usuario: int, db: Session = Depends(get_db)):
    query = db.query(
        Producto.id,
        Producto.producto,
        func.sum(TransaccionProducto.cantidad).label('cantidad'),
        func.sum(TransaccionProducto.precio).label('importe'),
        Transaccion.fechahora
    ).select_from(TransaccionProducto).join(Producto).join(Transaccion)

    query = query.filter(Transaccion.id_usuario == id_usuario).group_by(Producto.id, Transaccion.fechahora)

    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="Purchases not found for the specified user")

    purchases_by_user = [
        {
            'id_producto': result.id,
            'producto': result.producto,
            'cantidad': result.cantidad,
            'importe': (result.importe * result.cantidad),
            'fechacompra': result.fechahora
        }
        for result in results
    ]

    return purchases_by_user




@transaccionproducto_bp.get("/compras_by_fecha/{id_producto}")
async def read_compras_by_fecha(id_producto: int, fechainicio: str, fechafin: str, db: Session = Depends(get_db)):
    results = (
        db.query(
            Producto.id,
            Producto.producto,
            TransaccionProducto.id_transaccion,
            func.sum(TransaccionProducto.cantidad).label('cantidad'),
            func.sum(TransaccionProducto.precio).label('importe'),
            func.max(Transaccion.fechahora).label('fechacompra')  # Use an aggregate function for fechacompra
        )
        .join(TransaccionProducto, Producto.id == TransaccionProducto.id_producto)
        .join(Transaccion, TransaccionProducto.id_transaccion == Transaccion.id)
        .filter(
            Producto.id == id_producto,
            Transaccion.fechahora.between(fechainicio, fechafin)
        )
        .group_by(Producto.id, TransaccionProducto.id_transaccion)
        .all()
    )

    if not results:
        raise HTTPException(status_code=404, detail=f"Purchases for product with id {id_producto} not found within the specified date range")

    purchases_by_fecha = [
        {
            'id_producto': result.id,
            'producto': result.producto,
            'id_transaccion': result.id_transaccion,
            'cantidad': result.cantidad,
            'importe': result.importe,
            'fechacompra': result.fechacompra
        }
        for result in results
    ]

    return purchases_by_fecha

