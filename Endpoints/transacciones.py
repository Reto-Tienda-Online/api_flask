from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import Transaccion, get_db
from sqlalchemy import Text, text

transacciones_bp = APIRouter()