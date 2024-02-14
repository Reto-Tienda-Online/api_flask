from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from Models.models import Categoria, get_db
from sqlalchemy import text


categorias_bp = APIRouter()


from fastapi import Query

@categorias_bp.get("/all_categorias")
async def get_categorias(id: int = Query(None), categoria: str = Query(None), db: Session = Depends(get_db)):
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id
        
    if categoria is not None:
        conditions.append("categoria = :categoria")
        params['categoria'] = categoria
    
    query = text('SELECT * FROM categorias')
    if conditions:
        query = text(str(query) + " WHERE " + " AND ".join(conditions))

    result = db.execute(query, params)
    categorias_list = [dict(row._asdict()) for row in result.fetchall()]

    return categorias_list

@categorias_bp.post("/categorias")
async def create_categoria(categoria: dict, db: Session = Depends(get_db)):
    new_categoria = Categoria(**categoria)
    db.add(new_categoria)
    db.commit()
    db.refresh(new_categoria)
    
    return {"result": "Categoria created successfully", **categoria}

@categorias_bp.put("/categorias/{categoria_id}")
async def update_categoria(categoria_id: int, updated_categoria: dict, db: Session = Depends(get_db)):
    existing_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()

    if existing_categoria is None:
        return {"error": "Categoria not found"}

    for key, value in updated_categoria.items():
        setattr(existing_categoria, key, value)

    db.commit()
    db.refresh(existing_categoria)

    return {"result": "Categoria updated successfully", "updated_categoria": existing_categoria.__dict__}

@categorias_bp.delete("/categorias/{categoria_id}")
async def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    existing_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()

    if existing_categoria is None:
        return {"error": "Categoria not found"}

    db.delete(existing_categoria)
    db.commit()

    return {"result": "Categoria deleted successfully", "deleted_categoria": existing_categoria.__dict__}
