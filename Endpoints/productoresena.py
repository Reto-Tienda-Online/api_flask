from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import ProductoResena, get_db
from sqlalchemy import Text, text

productoresena_bp = APIRouter()