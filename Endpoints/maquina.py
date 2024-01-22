from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import Maquina, get_db
from sqlalchemy import Text, text

maquinas_bp = APIRouter()