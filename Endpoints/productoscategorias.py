from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import ProductoCategoria, get_db
from sqlalchemy import Text, text

productoscategorias_bp = APIRouter()