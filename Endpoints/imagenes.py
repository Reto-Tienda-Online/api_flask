from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import Imagen, get_db
from sqlalchemy import Text, text

imagenes_bp = APIRouter()