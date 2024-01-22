from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import Producto, get_db
from sqlalchemy import Text, text

productos_bp = APIRouter()