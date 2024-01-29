from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from Models.models import Usuario, get_db
from sqlalchemy import Text, text
from pydantic import BaseModel
from passlib.hash import bcrypt
from typing import Optional

usuarios_bp = APIRouter()

@usuarios_bp.get("/all_usuarios")
async def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return [{"id": usuario.id, "nombre": usuario.nombre, "apellido": usuario.apellido,
             "correo": usuario.correo, "contrasena": usuario.contrasena, "admin": usuario.admin} for usuario in usuarios]
    

class CreateUser(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    correo: Optional[str] = None
    contrasena: Optional[str] = None
    admin: Optional[bool] = None
    
@usuarios_bp.post("/register")
async def create_usuario(user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hash(user.contrasena)
    db_user = Usuario(nombre=user.nombre, apellido=user.apellido, correo=user.correo,
                      contrasena=hashed_password, admin=user.admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"result": "Usuario created successfully", "user": db_user.__dict__} 

class UpdateUser(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    correo: Optional[str] = None
    contrasena: Optional[str] = None
    admin: Optional[bool] = None

@usuarios_bp.put("/usuarios/{user_id}")
async def update_usuario(user_id: int, updated_user: UpdateUser, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(Usuario.id == user_id).first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if updated_user.nombre is not None:
        existing_user.nombre = updated_user.nombre
    if updated_user.apellido is not None:
        existing_user.apellido = updated_user.apellido
    if updated_user.correo is not None:
        existing_user.correo = updated_user.correo
    if updated_user.contrasena is not None:
        # Hash and update password only if a new password is provided
        existing_user.contrasena = bcrypt.hash(updated_user.contrasena)
    if updated_user.admin is not None:
        existing_user.admin = updated_user.admin

    db.commit()
    db.refresh(existing_user)

    return {"result": "Usuario updated successfully", "updated_user": existing_user.__dict__, "created":"true"}


@usuarios_bp.delete("/usuarios/{user_id}")
async def delete_usuario(user_id: int, db: Session = Depends(get_db)):
    # Delete Resenas related to the user
    db.execute(text("DELETE FROM resena WHERE id_usuario = :user_id"), {"user_id": user_id})

    # Delete the Usuario
    result = db.execute(text("DELETE FROM usuarios WHERE id = :user_id"), {"user_id": user_id})

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")

    db.commit()

    return {"result": "Usuario deleted successfully", "deleted_user_id": user_id}