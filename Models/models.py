from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime, Double
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine


db_user = "admin123"
db_password = "Admin.123"
db_host = "pgsql03.dinaserver.com"
db_port = "5432"
db_name = "tienda_juegos"

database_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

db = SQLAlchemy()

engine = create_engine(database_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class Descuento(db.Model):  
    __tablename__ = "descuentos"
    id = Column(Integer, primary_key=True)
    descuento = Column(Integer, nullable=False)

class Categoria(db.Model):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    categoria = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=False)

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    correo = Column(String(255), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    admin = Column(Boolean, nullable=False)
    
    resenas = relationship("Resena", back_populates="usuario", cascade="all, delete-orphan")

class Producto(db.Model):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    producto = Column(String(255), nullable=False)
    precio_unitario = Column(String(255), nullable=False)
    id_descuento = Column(Integer, ForeignKey('descuentos.id'), nullable=False)
    id_plataforma = Column(Integer, ForeignKey('plataforma.id'), nullable=False)
    rutavideo = Column(String(255), nullable=False)
    iframetrailer = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=False)

    descuento = relationship("Descuento")
    plataforma = relationship("Plataforma")

class ProductoCategoria(db.Model):
    __tablename__ = "producto_categoria"
    id = Column(Integer, primary_key=True)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)
    id_categoria = Column(Integer, ForeignKey('categorias.id'), nullable=False)

    producto = relationship("Producto")
    categoria = relationship("Categoria")

class CarroCompra(db.Model):
    __tablename__ = "carrocompra"
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)
    pagado = Column(Boolean, nullable=False)
    isdeleted = Column(Boolean, nullable=False)
    cantidad = Column(Integer, nullable=False)

    usuario = relationship("Usuario")
    producto = relationship("Producto")
   

class Logos(db.Model):
    __tablename__ = "logos"
    id = Column(Integer, primary_key=True)
    rutalogo = Column(String(255))
    tipo = Column(String(30))
    nombre = Column(String(255))
    id_plataforma = Column(Integer, ForeignKey('plataforma.id'), nullable=False)
    id_maquina = Column(Integer, ForeignKey('maquina.id'), nullable=False)
    
    plataforma = relationship("Plataforma")
    maquina = relationship("Maquina")

class Imagen(db.Model):
    __tablename__ = "imagenes"
    id = Column(Integer, primary_key=True)
    rutaimagen = Column(Text, nullable=False)
    id_juego = Column(Integer, ForeignKey('productos.id'), nullable=False)
   
    producto = relationship("Producto")

class MetodoPago(db.Model):
    __tablename__ = "metodopago"
    id = Column(Integer, primary_key=True)
    tipo = Column(String(50), nullable=False)

class Transaccion(db.Model):
    __tablename__ = "transaccion"
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_metodopago = Column(Integer, ForeignKey('metodopago.id'), nullable=False)
    importe = Column(Double, nullable=False) 
    fechahora = Column(DateTime(timezone=True), nullable=False)
    
    usuario = relationship("Usuario")
    metodopago = relationship("MetodoPago")
  
class TransaccionProducto(db.Model):
    __tablename__ = "transacionproducto"
    id = Column(Integer, primary_key=True)
    id_transaccion = Column(Integer, ForeignKey('transaccion.id'),nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)
    cantidad = Column(Integer,nullable=False) 
    precio = Column(Double, nullable=False) 
    
    transaccion = relationship("Transaccion")
    producto = relationship("Producto")

class ListaDeseos(db.Model):
    __tablename__ = "listadeseos"
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)
    favorito = Column(Boolean, nullable=False)

    usuario = relationship("Usuario")
    producto = relationship("Producto")

class Maquina(db.Model):
    __tablename__ = "maquina"
    id = Column(Integer, primary_key=True)
    maquina = Column(String(60), nullable=False)
    
    
class Plataforma(db.Model):
    __tablename__ = "plataforma"
    id = Column(Integer, primary_key=True)
    plataforma = Column(String(60), nullable=False)
    id_maquina = Column(Integer, ForeignKey('maquina.id'), nullable=False)

    maquina = relationship("Maquina")

class Resena(db.Model):
    __tablename__ = "resena"
    id = Column(Integer, primary_key=True)
    contenido = Column(Text, nullable=False)
    id_juego = Column(Integer, ForeignKey('productos.id'), nullable=False)
    resena = Column(Text, nullable=False)
    valoracion = Column(Integer, nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    usuario = relationship("Usuario", back_populates="resenas")
    producto = relationship("Producto")

class ProductoResena(db.Model):
    __tablename__ = "producto_resena"
    id = Column(Integer, primary_key=True)
    id_resena = Column(Integer, ForeignKey('resena.id'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)

    resena = relationship("Resena")
    producto = relationship("Producto")




