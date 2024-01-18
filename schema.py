from marshmallow import Schema, fields

class DescuentoSchema(Schema):
    id = fields.Int(dump_only=True)
    descuento = fields.Int(required=True)

class CategoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    categoria = fields.Str(required=True)
    descripcion = fields.Str(required=True)

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    apellido = fields.Str(required=True)
    correo = fields.Str(required=True)
    admin = fields.Bool(required=True)

class ProductoSchema(Schema):
    id = fields.Int(dump_only=True)
    producto = fields.Str(required=True)
    precio_unitario = fields.Str(required=True)
    id_descuento = fields.Int(required=True)
    id_plataforma = fields.Int(required=True)
    descripcion = fields.Str(required=True)

class ProductoCategoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    id_producto = fields.Int(required=True)
    id_categoria = fields.Int(required=True)

class CarroCompraSchema(Schema):
    id = fields.Int(dump_only=True)
    id_usuario = fields.Int(required=True)
    id_producto = fields.Int(required=True)
    cantidad = fields.Int(required=True)

class ImagenSchema(Schema):
    id = fields.Int(dump_only=True)
    rutaimagen = fields.Str(required=True)
    id_juego = fields.Int(required=True)

class MetodoPagoSchema(Schema):
    id = fields.Int(dump_only=True)
    id_usuario = fields.Int(required=True)
    metodo = fields.Str(required=True)
    numero_tarjeta = fields.Str(required=True)
    fecha_caduc = fields.Date(required=True)
    direccion_fact = fields.Str(required=True)

class TransaccionSchema(Schema):
    id = fields.Int(dump_only=True)
    id_usuario = fields.Int(required=True)
    id_metodopago = fields.Int(required=True)
    id_carrocompra = fields.Int(required=True)
    hora = fields.DateTime(required=True)

class ListaDeseosSchema(Schema):
    id = fields.Int(dump_only=True)
    id_usuario = fields.Int(required=True)
    id_producto = fields.Int(required=True)
    favorito = fields.Bool(required=True)

class MaquinaSchema(Schema):
    id = fields.Int(dump_only=True)
    maquina = fields.Str(required=True)

class PlataformaSchema(Schema):
    id = fields.Int(dump_only=True)
    plataforma = fields.Str(required=True)
    id_maquina = fields.Int(required=True)

class ResenaSchema(Schema):
    id = fields.Int(dump_only=True)
    resena = fields.Str(required=True)
    valoracion = fields.Bool(required=True)
    id_usuario = fields.Int(required=True)

class ProductoResenaSchema(Schema):
    id = fields.Int(dump_only=True)
    id_resena = fields.Int(required=True)
    id_producto = fields.Int(required=True)
