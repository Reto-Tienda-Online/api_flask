from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import Usuario, get_db
from sqlalchemy import Text, text

usuarios_bp = APIRouter()

