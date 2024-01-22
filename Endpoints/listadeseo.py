from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import ListaDeseos, get_db
from sqlalchemy import Text, text

listadeseo_bp = APIRouter()