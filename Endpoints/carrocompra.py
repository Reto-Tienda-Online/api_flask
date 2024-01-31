from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import CarroCompra, get_db
from sqlalchemy import Text, text
from pydantic import BaseModel
from typing import List, Optional

carrocompra_bp = APIRouter()

class DescuentoOut(BaseModel):
    id: int
class PlataformaOut(BaseModel):
    id: int

class ProductoOut(BaseModel):
    id: int
    producto: str
    precio_unitario: str
    descuento: DescuentoOut
    plataforma: PlataformaOut
    rutavideo: str
    iframetrailer: str
    descripcion: str

class CarroCompraOut(BaseModel):
    id: int
    id_usuario: int
    id_producto: int
    pagado: bool
    cantidad: int
    producto: ProductoOut
    
class CarroCompraCreate(BaseModel):
    id_usuario: int
    id_producto: int
    pagado: Optional[bool] = False
    cantidad: Optional[int] = 1

from sqlalchemy.orm import joinedload

@carrocompra_bp.get("/carrocompra", response_model=List[CarroCompraOut])
async def get_carrocompra(id_usuario: int, db: Session = Depends(get_db)):
    carrocompra_list = db.query(CarroCompra).filter(
        CarroCompra.id_usuario == id_usuario,
        CarroCompra.isdeleted == False,
        CarroCompra.pagado == False
    ).options(joinedload(CarroCompra.producto)).all()

    return carrocompra_list


@carrocompra_bp.post("/carrocompra", response_model=CarroCompraOut)
async def create_carrocompra(carrocompra: CarroCompraCreate, db: Session = Depends(get_db)):
    new_carrocompra = CarroCompra(**carrocompra.dict(), isdeleted=False)
    db.add(new_carrocompra)
    db.commit()
    db.refresh(new_carrocompra)
    return new_carrocompra


@carrocompra_bp.delete("/carrocompra/{carrocompra_id}")
async def delete_categoria(carrocompra_id: int, db: Session = Depends(get_db)):
    existing_carrocompra = db.query(CarroCompra).filter(CarroCompra.id == carrocompra_id).first()

    if existing_carrocompra is None:
        return {"error": "Carrocompra not found"}

    db.delete(existing_carrocompra)
    db.commit()

    return {"result": "Producto deleted successfully", "deleted_categoria": existing_carrocompra.__dict__}

