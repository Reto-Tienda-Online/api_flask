from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.models import Resena, get_db
from sqlalchemy import Text, text

resena_bp = APIRouter()

