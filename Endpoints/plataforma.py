from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import Plataforma, get_db
from sqlalchemy import Text, text

plataforma_bp = APIRouter()