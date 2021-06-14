from model.db_connection import *

ma = Marshmallow(app)

#------------Persona--------------

class PersonaSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'CI', 'nombre', 'apellido_Paterno', 'apellido_Materno', 'sexo', 'telefono', 'email', 'fecha_Nacimiento')

persona_schema_single = PersonaSchema()
persona_schema_multiple = PersonaSchema(many=True)

class Persona(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    CI = mysql.Column(mysql.String(18), unique=True, nullable=False)
    nombre = mysql.Column(mysql.String(16), nullable=False)
    apellido_Paterno = mysql.Column(mysql.String(18), nullable=False)
    apellido_Materno = mysql.Column(mysql.String(18), nullable=False)
    sexo = mysql.Column(mysql.String(1), nullable=False)
    telefono = mysql.Column(mysql.Integer, nullable=False)
    email = mysql.Column(mysql.String(38), nullable=False)
    fecha_Nacimiento = mysql.Column(mysql.Date(), nullable=False)
    
    def __init__(self, CI, nombre, apellido_Paterno, apellido_Materno, sexo, telefono, email, fecha_Nacimiento):
        self.CI = CI
        self.nombre = nombre
        self.apellido_Paterno = apellido_Paterno
        self.apellido_Materno = apellido_Materno
        self.sexo = sexo
        self.telefono = telefono
        self.email = email
        self.fecha_Nacimiento = fecha_Nacimiento
        
    def __repr__(self):
        return '<Persona %r>' % self.nombre+' '+self.apellido_Paterno+' '+self.apellido_Materno

#---------------------------------

#----------Tipo Empleado----------
class Tipo_EmpleadoSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'nombre', 'descripcion')
        
tipo_empleado_schema_single = Tipo_EmpleadoSchema()
tipo_empleado_schema_multiple = Tipo_EmpleadoSchema(many=True)

class Tipo_Empleado(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    nombre = mysql.Column(mysql.String(30), nullable=False)
    descripcion = mysql.Column(mysql.String(160), nullable=False)
    
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
        
    def __repr__(self):
        return '<Tipo Empleado %r>' % self.nombre
    
#---------------------------------

#------------Sucursal-------------

class SucursalSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'nombre', 'direccion')
        
sucursal_schema_single = SucursalSchema()
sucursal_schema_multiple = SucursalSchema(many=True)

class Sucursal(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    nombre = mysql.Column(mysql.String(45), nullable=False)
    direccion = mysql.Column(mysql.String(125), nullable=False)
    
    def __init__(self, nombre,direccion):
        self.nombre = nombre
        self.direccion = direccion
        
    def __repr__(self):
        return '<Sucursal nombre=%r>' % self.nombre

#---------------------------------

#-----------Empleado--------------

class EmpleadoSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'estado', 'id_Persona', 'id_TipoEmpleado', 'id_Sucursal')

empleado_schema_single = EmpleadoSchema()
empleado_schema_multiple = EmpleadoSchema(many=True)

class Empleado(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    estado = mysql.Column(mysql.Integer, nullable=False)
    id_Persona = mysql.Column(mysql.Integer, mysql.ForeignKey('persona.ID'), nullable=False)
    id_TipoEmpleado = mysql.Column(mysql.Integer, mysql.ForeignKey('tipo_empleado.ID'), nullable=False)
    id_Sucursal = mysql.Column(mysql.Integer, mysql.ForeignKey('sucursal.ID'), nullable=False)
    
    def __init__(self, estado, id_Persona, id_TipoEmpleado, id_Sucursal):
        self.estado = estado
        self.id_Persona = id_Persona
        self.id_TipoEmpleado = id_TipoEmpleado
        self.id_Sucursal = id_Sucursal
        
    def __repr__(self):
        return '<Empleado id_persona=%r>' % self.id_Persona

#---------------------------------

#------------Cuenta---------------

class CuentaSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'nombre_Cuenta', 'urs_Password', 'url_Photo', 'estado', 'id_Empleado')

cuenta_schema_single = CuentaSchema()
cuenta_schema_multiple = CuentaSchema(many=True)

class Cuenta(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    nombre_Cuenta = mysql.Column(mysql.String(25), nullable = False)
    urs_Password = mysql.Column(mysql.String(256), nullable = False)
    url_Photo = mysql.Column(mysql.String(2000), nullable = False)
    estado = mysql.Column(mysql.Integer, nullable=False)
    id_Empleado = mysql.Column(mysql.Integer, mysql.ForeignKey('empleado.ID'), nullable=False)
    
    def __init__(self, nombre_Cuenta, urs_Password, url_Photo, estado, id_Empleado):
        self.nombre_Cuenta = nombre_Cuenta
        self.urs_Password = urs_Password
        self.url_Photo = url_Photo
        self.estado = estado
        self.id_Empleado = id_Empleado
        
    def __repr__(self):
        return '<Cuenta username=%r>' % self.nombre_Cuenta

#---------------------------------

#-------------Cliente-------------

class ClienteSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'NIT', 'razon_Social', 'id_Persona',)    
    
cliente_schema_single = ClienteSchema()
cliente_schema_multiple = ClienteSchema(many=True)

class Cliente(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    NIT = mysql.Column(mysql.BigInteger, default=0)
    razon_Social = mysql.Column(mysql.String(45))
    id_Persona = mysql.Column(mysql.Integer, mysql.ForeignKey('persona.ID'), nullable=False)
    
    def __init__(self, NIT, razon_Social, id_Persona):
        self.NIT = NIT
        self.razon_Social = razon_Social
        self.id_Persona = id_Persona
        
    def __repr__(self):
        return '<Cliente id_Persona=%r>' % self.id_Persona

#---------------------------------

#------------Tecnico--------------

class TecnicoSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'direccion', 'estado', 'id_Persona')
        
tecnico_schema_single = TecnicoSchema()
tecnico_schema_multiple = TecnicoSchema(many=True)

class Tecnico(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    direccion = mysql.Column(mysql.String(125), nullable=False)
    estado = mysql.Column(mysql.Integer, nullable=False)
    id_Persona = mysql.Column(mysql.Integer, mysql.ForeignKey('persona.ID'), nullable=False)
    
    def __init__(self, direccion, estado, id_Persona):
        self.direccion = direccion
        self.estado = estado
        self.id_Persona = id_Persona
        
    def __repr__(self):
        return '<Tecnico direccion=%r>' % self.direccion

#---------------------------------

#-------------Marca---------------

class MarcaSchema(ma.Schema):
    class Meta:
        fields = ['ID', 'nombre']

marca_schema_single = MarcaSchema()
marca_schema_multiple = MarcaSchema(many=True)

class Marca(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    nombre = mysql.Column(mysql.String(40), nullable=False)
    
    def __init__(self, nombre):
        self.nombre = nombre
        
    def __repr__(self):
        return '<Marca %r>' % self.nombre

#---------------------------------

#------------Categoria------------

class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'nombre')

categoria_schema_single = CategoriaSchema()
categoria_schema_multiple = CategoriaSchema(many=True)

class Categoria(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    nombre = mysql.Column(mysql.String)
    
    def __init__(self, nombre):
        self.nombre = nombre
    
    def __repr__(self):
        return '<Categoria %r>' % self.nombre

#------------Producto-------------

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'nombre', 'descripcion', 'precio_SinFactura', 'precio_ConFactura', 'precio_Tecnico', 'garantia_Meses_Valido', 'id_Marca', 'id_Categoria', 'id_Tecnico')
        
producto_schema_single = ProductoSchema()
producto_schema_multiple = ProductoSchema(many=True)

class Producto(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    nombre = mysql.Column(mysql.String(30), nullable=False)
    descripcion = mysql.Column(mysql.String(100), nullable=False)
    precio_SinFactura = mysql.Column(mysql.Numeric(6,2), nullable=False)
    precio_ConFactura = mysql.Column(mysql.Numeric(6,2), nullable=False)
    precio_Tecnico = mysql.Column(mysql.Numeric(6,2), nullable=False)
    garantia_Meses_Valido = mysql.Column(mysql.Integer, nullable=False)
    id_Marca = mysql.Column(mysql.Integer, mysql.ForeignKey('marca.ID'))
    id_Categoria = mysql.Column(mysql.Integer, mysql.ForeignKey('categoria.ID'))
    id_Tecnico = mysql.Column(mysql.Integer, mysql.ForeignKey('tecnico.ID'))
    
    def __init__(self, nombre, descripcion, precio_SinFactura, precio_ConFactura, precio_Tecnico, garantia_Meses_Valido, id_Marca, id_Categoria, id_Tecnico):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_SinFactura = precio_SinFactura
        self.precio_ConFactura = precio_ConFactura
        self.precio_Tecnico = precio_Tecnico
        self.garantia_Meses_Valido = garantia_Meses_Valido
        self.id_Marca = id_Marca
        self.id_Categoria = id_Categoria
        self.id_Tecnico = id_Tecnico
        
    def __repr__(self):
        return '<Producto %r>' % self.nombre

#---------------------------------

#-------------Venta---------------

class VentaSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'total', 'fecha_Venta', 'tiene_Factura', 'estado', 'id_Cliente', 'id_Empleado', 'id_Sucursal')

venta_schema_single = VentaSchema()
venta_schema_multiple = VentaSchema(many=True)

class Venta(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    total = mysql.Column(mysql.Numeric(6,2), nullable=False)
    fecha_Venta = mysql.Column(mysql.Date(), nullable=False)
    tiene_Factura = mysql.Column(mysql.Boolean, nullable=False)
    estado = mysql.Column(mysql.Integer, nullable=False)
    id_Cliente = mysql.Column(mysql.Integer, mysql.ForeignKey('cliente.ID'),nullable=False)
    id_Empleado = mysql.Column(mysql.Integer, mysql.ForeignKey('empleado.ID'),nullable=False)
    id_Sucursal = mysql.Column(mysql.Integer, mysql.ForeignKey('sucursal.ID'))
    
    def __init__(self, total, fecha_Venta, tiene_Factura,estado, id_Cliente, id_Empleado, id_Sucursal):
        self.total = total
        self.fecha_Venta = fecha_Venta
        self.tiene_Factura = tiene_Factura
        self.estado = estado
        self.id_Cliente = id_Cliente
        self.id_Empleado = id_Empleado
        self.id_Sucursal = id_Sucursal
    
    def __repr__(self):
        return '<Venta total=%r>' % self.total

#---------------------------------

#--------Producto_Vendido---------

class Producto_vendidoSchema(ma.Schema):
    class Meta:
        fields = ('precio_Unitario','cantidad', 'total', 'id_Producto', 'id_Venta')
        
producto_vendido_schema_single = Producto_vendidoSchema()
producto_vendido_schema_multiple = Producto_vendidoSchema(many=True)

class Producto_vendido(mysql.Model):
    precio_Unitario = mysql.Column(mysql.Numeric(6,2))
    cantidad = mysql.Column(mysql.Integer, nullable=True)
    total = mysql.Column(mysql.Numeric(6,2), nullable=True)
    id_Producto = mysql.Column(mysql.Integer, mysql.ForeignKey('producto.ID'), primary_key=True)
    id_Venta = mysql.Column(mysql.Integer, mysql.ForeignKey('venta.ID'), primary_key=True)
    
    def __init__(self, precio_Unitario, cantidad, total, id_Producto, id_Venta):
        self.precio_Unitario = precio_Unitario
        self.cantidad = cantidad
        self.total = total
        self.id_Producto = id_Producto
        self.id_Venta = id_Venta
        
    def __repr__(self):
        return '<Producto_Vendido id_Venta=%r>' % self.id_Venta

#---------------------------------

#------------Garantia-------------

class GarantiaSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'COD_Fabrica_Producto', 'fecha_Registro', 'fecha_Vencimiento', 'estado', 'id_Venta', 'id_Producto')
        
garantia_schema_single = GarantiaSchema()
garantia_schema_multiple = GarantiaSchema(many=True)

class Garantia(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    COD_Fabrica_Producto = mysql.Column(mysql.String(45), nullable=False)
    fecha_Registro = mysql.Column(mysql.Date(), nullable=False)
    fecha_Vencimiento = mysql.Column(mysql.Integer, nullable=False)
    estado = mysql.Column(mysql.Integer, nullable=False)
    id_Venta = mysql.Column(mysql.Integer, mysql.ForeignKey('venta.ID'), nullable=False)
    id_Producto = mysql.Column(mysql.Integer, mysql.ForeignKey('producto.ID'), nullable=False)
    
    def __init__(self, COD_Fabrica_Producto, fecha_Registro, fecha_Vencimiento, estado, id_Venta, id_Producto):
        self.COD_Fabrica_Producto = COD_Fabrica_Producto
        self.fecha_Registro = fecha_Registro
        self.fecha_Vencimiento = fecha_Vencimiento
        self.estado = estado
        self.id_Venta = id_Venta
        self.id_Producto = id_Producto
        
    def __repr__(self):
        return '<Garantia codigo_Producto=%r>' % self.COD_Fabrica_Producto

#---------------------------------

#--------Producto_Devuelto--------

class Producto_devueltoSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'descripcion', 'id_Garantia', 'id_Producto')
        
producto_devuelto_schema_single = Producto_devueltoSchema()
producto_devuelto_schema_multiple = Producto_devueltoSchema(many=True)

class Producto_devuelto(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    descripcion = mysql.Column(mysql.String(60), nullable=False)
    id_Garantia = mysql.Column(mysql.Integer, mysql.ForeignKey('garantia.ID'), nullable=False)
    id_Producto = mysql.Column(mysql.Integer, mysql.ForeignKey('producto.ID'), nullable=False)
    
    def __init__(self, ID, descripcion, id_Garantia, id_Producto):
        self.ID = ID
        self.decripcion = descripcion
        self.id_Garantia = id_Garantia
        self.id_Producto = id_Producto
        
    def __repr__(self):
        return '<Producto_Devuelto id_Garantia=%g, id_Producto=%p>' % self.id_Garantia, self.id_Producto

#---------------------------------

#-----------Inventario------------

class InventarioSchema(ma.Schema):
    class Meta:
        fields = ('cantidad', 'id_Sucursal', 'id_Producto')
        
inventario_schema_single = InventarioSchema()
inventario_schema_multiple = InventarioSchema(many=True)

class Inventario(mysql.Model):
    cantidad = mysql.Column(mysql.Integer, nullable = False)
    id_Sucursal = mysql.Column(mysql.Integer, mysql.ForeignKey('sucursal.ID'), primary_key=True)
    id_Producto = mysql.Column(mysql.Integer, mysql.ForeignKey('producto.ID'), primary_key=True)
    
    def __init__(self, cantidad, id_Sucursal, id_Producto):
        self.cantidad = cantidad
        self.id_Sucursal = id_Sucursal
        self.id_Producto = id_Producto
        
    def __repr__(self):
        return '<Inventario id_Sucursal=%s, id_Producto=%p>' % self.id_Sucursal, self.id_Producto

#---------------------------------

#-------------Permiso-------------

class PermisoSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'nombre', 'descripcion')
        
permiso_schema_single = PermisoSchema()
permiso_schema_multiple = PermisoSchema(many=True)

class Permiso(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    nombre = mysql.Column(mysql.String(32), nullable=False)
    descripcion = mysql.Column(mysql.String(45), nullable=False)
    
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
        
    def __repr__(self):
        return '<Permiso nombre=%r>' % self.nombre

#---------------------------------

#--------Permiso_Asignado---------

class Permiso_asignadoSchema(ma.Schema):
    class Meta:
        fields = ('estado', 'id_Permiso', 'id_Cuenta')
        
permiso_asignado_schema_single = Permiso_asignadoSchema()
permiso_asignado_schema_multiple = Permiso_asignadoSchema(many=True)

class Permiso_asignado(mysql.Model):
    estado = mysql.Column(mysql.Integer, nullable=False)
    id_Permiso = mysql.Column(mysql.Integer, mysql.ForeignKey('permiso.ID'), primary_key=True)
    id_Cuenta = mysql.Column(mysql.Integer, mysql.ForeignKey('cuenta.ID'), primary_key=True)
    
    def __init__(self, estado, id_Permiso, id_Cuenta):
        self.estado = estado
        self.id_Permiso = id_Permiso
        self.id_Cuenta = id_Cuenta
        
    def __repr__(self):
        return '<Permiso_Asignado estado=%r>' % self.estado

#---------------------------------

#-------------Factura-------------

class FacturaSchema(ma.Schema):
    class Meta:
        fields = ('NRO', 'NIT', 'razon_Social', 'id_Venta')
    
factura_schema_single = FacturaSchema()
factura_schema_multiple = FacturaSchema(many=True)

class Factura(mysql.Model):
    NRO = mysql.Column(mysql.Integer, primary_key=True)
    NIT = mysql.Column(mysql.Integer, nullable=False)
    razon_Social = mysql.Column(mysql.String(45), nullable=False)
    id_Venta = mysql.Column(mysql.Integer, nullable=False)
    
    def __init__(self, NIT, razon_Social, id_Venta):
        self.NIT = NIT
        self.razon_Social = razon_Social
        self.id_Venta = id_Venta
        
    def __repr__(self):
        return '<Factura NIT=%r>' % self.NIT

#---------------------------------

mysql.create_all()