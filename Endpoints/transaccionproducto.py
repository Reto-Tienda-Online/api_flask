from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import TransaccionProducto, get_db
from sqlalchemy import Text, text

transaccionproducto_bp = APIRouter()