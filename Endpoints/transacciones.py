from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import Transaccion, get_db
from sqlalchemy import Text, text

transacciones_bp = APIRouter()

# CREAR GET, POST, PUT Y DELETE
# Lista de compras, por id_usuario, por pedidos, listar compras por productos, la cantidad de 
# veces que un producto ha sido comprado por mes. 