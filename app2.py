from flask import Flask
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
from Models.models import db, get_db
from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from flask_migrate import Migrate
from passlib.context import CryptContext
from Models.models import db, Usuario
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

flask_app = Flask(__name__)

db_user = "postgres"
db_password = "12345"
db_host = "localhost"
db_port = "5432"
db_name = "2retodevelop"

database_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

flask_app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(flask_app)
migrate = Migrate(flask_app, db)

app = FastAPI()

# Configure JWT settings
SECRET_KEY = "your-secret-key"  # Change this to a strong, random secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Set the expiration time for the access token

# OAuth2PasswordBearer is a class for handling OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Hashing helper
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Set up CORS middleware
origins = ["*"]  # Replace with your actual frontend URL(s)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Secret key to sign JWT
SECRET_KEY = "your_secret_key"

# Algorithm to sign JWT
ALGORITHM = "HS256"

# OAuth2PasswordBearer for handling token in the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(token: str = Depends(oauth2_scheme), db1: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
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


# Example protected route
@app.get("/protected")
async def protected_route(current_user: Usuario = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user.nombre}
# Dependency to get current user from the token

# Function to create a new JWT token
def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


from sqlalchemy.orm import Session as SqlSession
from Models.models import get_db
# Route to handle token creation

@app.post("/token")
async def login_for_access_token(    form_data: OAuth2PasswordRequestForm = Depends(), db: SqlSession = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.correo == form_data.username).first()
    if user and pwd_context.verify(form_data.password, user.contrasena):
        # Create a JWT token
        token_data = {"sub": user.correo}
        access_token = create_jwt_token(token_data)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        
# Include other routers as you did before
routers = [descuentos_bp, categorias_bp, productoresena_bp,
           productos_bp, productoscategorias_bp, usuarios_bp, maquinas_bp, plataforma_bp]
for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
