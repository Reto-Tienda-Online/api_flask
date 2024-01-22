from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import CarroCompra, get_db
from sqlalchemy import Text, text

carrocompra_bp = APIRouter()