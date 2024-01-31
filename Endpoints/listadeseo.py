from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import ListaDeseos, get_db
from sqlalchemy import Text, text
from typing import Optional, List
from pydantic import BaseModel

'''
class ListaDeseos(db.Model):
    __tablename__ = "listadeseos"
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)
    favorito = Column(Boolean, nullable=False)

    usuario = relationship("Usuario")
    producto = relationship("Producto")
'''

listadeseo_bp = APIRouter()

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
    new_listadeseo = ListaDeseos(**carrocompra.dict(), isdeleted=False)
    db.add(new_listadeseo)
    db.commit()
    db.refresh(new_listadeseo)
    return new_listadeseo


@listadeseo_bp.delete("/listadeseo/{listadeseo_id}")
async def delete_categoria(listadeseo_id: int, db: Session = Depends(get_db)):
    existing_listadeseo = db.query(ListaDeseos).filter(ListaDeseos.id == listadeseo_id).first()

    if existing_listadeseo is None:
        return {"error": "Listadeseo not found"}

    db.delete(existing_listadeseo)
    db.commit()

    return {"result": "Producto deleted successfully", "deleted_categoria": existing_listadeseo.__dict__}
