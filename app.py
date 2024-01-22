from flask import Flask
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from flask_migrate import Migrate
from pydantic import BaseModel
from starlette.requests import Request
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from Endpoints.descuentos import descuentos_bp
from Endpoints.categorias import categorias_bp
from Endpoints.carrocompra import carrocompra_bp
from Endpoints.imagenes import imagenes_bp
from Endpoints.listadeseo import listadeseo_bp
from Endpoints.maquina import maquinas_bp
from Endpoints.metodopago import metodopago_bp
from Endpoints.plataforma import plataforma_bp
from Endpoints.productoresena import productoresena_bp
from Endpoints.productos import productos_bp
from Endpoints.productoscategorias import productoscategorias_bp
from Endpoints.resena import resena_bp
from Endpoints.transacciones import transacciones_bp
from Endpoints.transaccionproducto import transaccionproducto_bp
from Endpoints.usuarios import usuarios_bp 
from Models.models import db
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session

flask_app = Flask(__name__)

db_user = "postgres"
db_password = "12345"
db_host = "localhost"
db_port = "5432"
db_name = "2retodevelop"

'''class APIKeyHeader(db.Model):
    apikey: str
'''
database_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

flask_app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(flask_app)
migrate = Migrate(flask_app, db)

app = FastAPI()

routers = [descuentos_bp, categorias_bp]
for router in routers:
    app.include_router(router)

'''

@app.middleware("http")
async def api_key_middleware(request: Request, call_next, apikey: str = Depends(APIKeyHeader(name="apikey", auto_error=False))):
    if apikey != "12345":
        raise HTTPException(status_code=403, detail="API Key is invalid")

    response = await call_next(request)
    return response

# Use the middleware in the app
app.middleware("http")(api_key_middleware)
# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

'''
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")