from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, TIMESTAMP, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    correo = Column(String(255), nullable=False)
    admin = Column(Boolean, nullable=False)

class Producto(db.Model):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    producto = Column(String(255), nullable=False)
    precio_unitario = Column(String(255), nullable=False)
    id_descuento = Column(Integer, ForeignKey('descuentos.id'), nullable=False)
    id_plataforma = Column(Integer, ForeignKey('plataforma.id'), nullable=False)
    descripcion = Column(String(255), nullable=False)

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
    cantidad = Column(Integer, nullable=False)

    usuario = relationship("Usuario")
    producto = relationship("Producto")
    
class HistorialCompras(db.Model):
    __tablename__ = "historial_compras"
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_compra = Column(DateTime, nullable=False)

    usuario = relationship("Usuario")
    producto = relationship("Producto")

class Imagen(db.Model):
    __tablename__ = "imagenes"
    id = Column(Integer, primary_key=True)
    rutaimagen = Column(Text, nullable=False)
    id_juego = Column(Integer, ForeignKey('productos.id'), nullable=False)

    producto = relationship("Producto")

class MetodoPago(db.Model):
    __tablename__ = "metodopago"
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    metodo = Column(String(60), nullable=False)
    numero_tarjeta = Column(String(24), nullable=False)
    fecha_caduc = Column(Integer, nullable=False)
    direccion_fact = Column(String(255), nullable=False)

    usuario = relationship("Usuario")

class Transaccion(db.Model):
    __tablename__ = "transaccion"
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_metodopago = Column(Integer, ForeignKey('metodopago.id'), nullable=False)
    id_carrocompra = Column(Integer, ForeignKey('carrocompra.id'), nullable=False)
    hora = Column(TIMESTAMP, nullable=False)

    usuario = relationship("Usuario")
    metodopago = relationship("MetodoPago")
    carrocompra = relationship("CarroCompra")

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
    resena = Column(Text, nullable=False)
    valoracion = Column(Boolean, nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    usuario = relationship("Usuario")

class ProductoResena(db.Model):
    __tablename__ = "producto_resena"
    id = Column(Integer, primary_key=True)
    id_resena = Column(Integer, ForeignKey('resena.id'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)

    resena = relationship("Resena")
    producto = relationship("Producto")
