from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.models import Transaccion, get_db, CarroCompra, TransaccionProducto
from sqlalchemy import Text, text, DateTime
from sqlalchemy.sql import func

transacciones_bp = APIRouter()



def create_transaction_and_products(db: Session, id_usuario: int):
    shopping_cart_items = db.query(CarroCompra).filter(
        CarroCompra.id_usuario == id_usuario,
        CarroCompra.isdeleted == False,
        CarroCompra.pagado == False
    ).all()

    if not shopping_cart_items:
        raise HTTPException(status_code=404, detail="Shopping cart is empty")

    # Calculate the total price and create a transaction
    total_price = sum(float(item.producto.precio_unitario) * item.cantidad for item in shopping_cart_items)
    transaction = Transaccion(
        id_usuario=id_usuario,
        id_metodopago=1,  
        importe=total_price,
        fechahora = func.current_timestamp()
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # Create entries in the TransaccionProducto table
    for item in shopping_cart_items:
        transaction_product = TransaccionProducto(
            id_transaccion=transaction.id,
            id_producto=item.id_producto,
            cantidad=item.cantidad,
            precio=item.producto.precio_unitario
        )
        db.add(transaction_product)

    # Mark the items as paid
    for item in shopping_cart_items:
        item.pagado = True

    db.commit()

    return transaction

# Example usage in FastAPI endpoint
@transacciones_bp.post("/process_transaction/{id_usuario}")
async def process_transaction(id_usuario: int, db: Session = Depends(get_db)):
    transaction = create_transaction_and_products(db, id_usuario)
    return {"result": "Transaction processed successfully", "transaction_id": transaction.id}