from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.models import ListaDeseos, get_db
from typing import Optional, List
from pydantic import BaseModel

listadeseo_bp = APIRouter()

class DescuentoOut(BaseModel):
    id: int
    descuento: int
class PlataformaOut(BaseModel):
    id: int
    plataforma: str

class ProductoOut(BaseModel):
    id: int
    producto: str
    precio_unitario: str
    descuento: DescuentoOut
    plataforma: PlataformaOut
    rutavideo: str
    iframetrailer: str
    descripcion: str

class ListaDeseoOut(BaseModel):
    id: int
    id_usuario: int
    id_producto: int
    favorito: Optional[bool] = False
    producto: ProductoOut
    
class ListaDeseoCreate(BaseModel):
    id_usuario: int
    id_producto: int
    favorito: Optional[bool] = False
    

from sqlalchemy.orm import joinedload

@listadeseo_bp.get("/listadeseo", response_model=List[ListaDeseoOut])
async def get_listadeseo(id_usuario: int, db: Session = Depends(get_db)):
    listadeseo_list = db.query(ListaDeseos).filter(
        ListaDeseos.id_usuario == id_usuario,
    ).options(joinedload(ListaDeseos.producto)).all()

    return listadeseo_list


@listadeseo_bp.post("/listadeseo", response_model=ListaDeseoOut)
async def create_listadeseo(carrocompra: ListaDeseoCreate, db: Session = Depends(get_db)):
    new_listadeseo = ListaDeseos(**carrocompra.dict())
    db.add(new_listadeseo)
    db.commit()
    db.refresh(new_listadeseo)
    return new_listadeseo

@listadeseo_bp.delete("/listadeseo/{id_usuario}/{id_producto}")
async def delete_listadeseo(id_usuario: int, id_producto: int, db: Session = Depends(get_db)):
    existing_listadeseo = db.query(ListaDeseos).filter(
        ListaDeseos.id_usuario == id_usuario,
        ListaDeseos.id_producto == id_producto
    ).first()

    if existing_listadeseo is None:
        raise HTTPException(status_code=404, detail="Listadeseo not found")

    deleted_listadeseo = {
        "id": existing_listadeseo.id,
        "id_usuario": existing_listadeseo.id_usuario,
        "id_producto": existing_listadeseo.id_producto
    }

    db.delete(existing_listadeseo)
    db.commit()

    return {"result": "Listadeseo deleted successfully", **deleted_listadeseo}



class ListaDeseoUpdate(BaseModel):
    id_usuario: Optional[int] = None
    id_producto: Optional[int] = None
    favorito: Optional[bool] = None


@listadeseo_bp.put("/listadeseo/{listadeseo_id}", response_model=ListaDeseoOut)
async def update_carrocompra(listadeseo_id: int, listadeseo_update: ListaDeseoUpdate, db: Session = Depends(get_db)):
    existing_listadeseo = db.query(ListaDeseos).filter(ListaDeseos.id == listadeseo_id).first()

    if existing_listadeseo is None:
        raise HTTPException(status_code=404, detail="Listadeseo not found")

    for field, value in listadeseo_update.dict(exclude_unset=True).items():
        setattr(existing_listadeseo, field, value)

    db.commit()
    db.refresh(existing_listadeseo)

    return existing_listadeseo
