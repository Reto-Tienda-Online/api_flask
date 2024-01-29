from flask import Flask
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware  
from flask_migrate import Migrate
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session as SqlSession
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
from Endpoints.usuarios import usuarios_bp, Usuario
from Endpoints.logos import logos_bp
from Models.models import db, get_db
from fastapi import FastAPI, Depends
from jose import JWTError, jwt
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta


flask_app = Flask(__name__)

db_user = "admin123"
db_password = "Admin.123"
db_host = "pgsql03.dinaserver.com"
db_port = "5432"
db_name = "tienda_juegos"


database_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

flask_app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(flask_app)
migrate = Migrate(flask_app, db)

app = FastAPI()

SECRET_KEY = "your-secret-key"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(token: str = Depends(oauth2_scheme), db1: SqlSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db1.query(Usuario).filter(Usuario.correo == correo).first()
    if user is None:
        raise credentials_exception

    return user

@app.get("/protected")
async def protected_route(current_user: Usuario = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user.nombre}

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: SqlSession = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.correo == form_data.username).first()
    
    if user and pwd_context.verify(form_data.password, user.contrasena):
        token_data = {"sub": user.correo}
        access_token = create_jwt_token(token_data)
        
        return {"access_token": access_token, "token_type": "bearer", "usuario": user}
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )



routers = [descuentos_bp, categorias_bp, productoresena_bp, 
productos_bp,productoscategorias_bp, usuarios_bp, 
maquinas_bp, plataforma_bp, productos_bp, imagenes_bp,
logos_bp, carrocompra_bp, listadeseo_bp, metodopago_bp,
resena_bp, transacciones_bp, transaccionproducto_bp]


for router in routers:
    app.include_router(router)


origins = ["*"]  
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

'''

class APIKeyHeader(BaseModel):
    apikey: str


apikey = "apikey"


@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    
    #if (request.url.path == "/basket/users" and request.method == "GET") or request.method != "GET":
        # Check if the API key is provided in the "apikey" header
    api_key_header = request.headers.get("apikey")
    if api_key_header != app.state.api_key:
        raise HTTPException(status_code=403, detail="API Key is invalid")

    response = await call_next(request)
    return response
@app.on_event("startup")
async def startup_db_client():
    
    app.state.api_key = apikey


'''

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")



# Julio Augusto

# Productos --> Nombre Get.  XXXXXXX
# Que se vea la contraseña en el Get y en el Put  
# Sacar la plataforma dentro de producto en modo diccionario  XXXXXXXX


# Diego

# Get de ProductosCategorias
# Lo mismo para las plataformas
# Recibir 3 reseñas dentro del producto

