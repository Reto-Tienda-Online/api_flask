from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import MetodoPago, get_db
from sqlalchemy import Text, text

metodopago_bp = APIRouter()

