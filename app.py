from flask import Flask
from flask_migrate import Migrate
from fastapi import FastAPI
from Endpoints import *
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

database_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

flask_app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(flask_app)
migrate = Migrate(flask_app, db)

app = FastAPI()

app.include_router(descuentos_bp)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    
    


