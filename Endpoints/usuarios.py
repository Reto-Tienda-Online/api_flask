from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.models import Usuario, get_db
from sqlalchemy import Text, text
from pydantic import BaseModel
from passlib.hash import bcrypt

usuarios_bp = APIRouter()

@usuarios_bp.get("/all_usuarios")
async def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return [{"id": usuario.id, "nombre": usuario.nombre, "apellido": usuario.apellido,
             "correo": usuario.correo, "admin": usuario.admin} for usuario in usuarios]
    

class CreateUser(BaseModel):
    nombre: str
    apellido: str
    correo: str
    contrasena: str
    admin: bool

@usuarios_bp.post("/usuarios")
async def create_usuario(user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hash(user.contrasena)
    db_user = Usuario(nombre=user.nombre, apellido=user.apellido, correo=user.correo,
                      contrasena=hashed_password, admin=user.admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"result": "Usuario created successfully", "user": db_user.__dict__} 


class UpdateUser(BaseModel):
    nombre: str
    apellido: str
    correo: str
    contrasena: str
    admin: bool
    
    
@usuarios_bp.put("/usuarios/{user_id}")
async def update_usuario(user_id: int, updated_user: UpdateUser, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(Usuario.id == user_id).first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user data
    existing_user.nombre = updated_user.nombre
    existing_user.apellido = updated_user.apellido
    existing_user.correo = updated_user.correo

    # Hash and update password only if a new password is provided
    if updated_user.contrasena:
        existing_user.contrasena = bcrypt.hash(updated_user.contrasena)

    existing_user.admin = updated_user.admin

    db.commit()
    db.refresh(existing_user)

    return {"result": "Usuario updated successfully", "updated_user": existing_user.__dict__}


@usuarios_bp.delete("/usuarios/{user_id}")
async def delete_usuario(user_id: int, db: Session = Depends(get_db)):
    user_to_delete = db.query(Usuario).filter(Usuario.id == user_id).first()

    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user_to_delete)
    db.commit()

    return {"result": "Usuario deleted successfully", "deleted_user": user_to_delete.__dict__}