from controller.session import *

ma = Marshmallow(app)

#------------Persona--------------

class PersonaSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'CI', 'nombre', 'apellido_Paterno', 'apellido_Materno', 'sexo', 'telefono', 'email', 'fecha_Nacimiento')

persona_schema_single = PersonaSchema()
persona_schema_multiple = PersonaSchema(many=True)

class Persona(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    CI = mysql.Column(mysql.Integer, unique=True, nullable=False)
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

#-----------Empleado--------------

class EmpleadoSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'estado', 'id_persona')

empleado_schema_single = EmpleadoSchema()
empleado_schema_multiple = EmpleadoSchema(many=True)

class Empleado(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    estado = mysql.Column(mysql.Integer, nullable=False)
    id_persona = mysql.Column(mysql.Integer, mysql.ForeignKey('persona.id'), nullable=False)
    
    def __init__(self, estado, id_persona):
        self.estado = estado
        self.id_persona = id_persona
        
    def __repr__(self):
        return '<Empleado id_persona=%r>' % self.id_persona

#---------------------------------

#------------Cuenta---------------

class CuentaSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'nombre_Cuenta', 'urs_Password', 'urs_Llave', 'estado', 'id_Empleado')

cuenta_schema_single = CuentaSchema()
cuenta_schema_multiple = CuentaSchema(many=True)

class Cuenta(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    nombre_Cuenta = mysql.Column(mysql.String(25), nullable=False)
    urs_Password = mysql.Column(mysql.String(256), nullable=False)
    urs_Llave = mysql.Column(mysql.String(30), nullable=False)
    estado = mysql.Column(mysql.Integer, nullable=False)
    id_Empleado = mysql.Column(mysql.Integer, mysql.ForeignKey('empleado.id'), nullable=False)
    
    def __init__(self, nombre_Cuenta, urs_Password, urs_Llave, estado, id_Empleado):
        self.nombre_Cuenta = nombre_Cuenta
        self.urs_Password = urs_Password
        self.urs_Llave = urs_Llave
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
    NIT = mysql.Column(mysql.Integer)
    razon_Social = mysql.Column(mysql.String(45))
    id_Persona = mysql.Column(mysql.Integer, mysql.ForeignKey('persona.id'), nullable=False)
    
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
        fields = ('ID', 'direccion', 'id_Persona')
        
tecnico_schema_single = TecnicoSchema()
tecnico_schema_multiple = TecnicoSchema(many=True)

class Tecnico(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    direccion = mysql.Column(mysql.String(125), nullable=False)
    id_Persona = mysql.Column(mysql.Integer, mysql.ForeignKey('persona.id'), nullable=False)
    
    def __init__(self, direccion, id_Persona):
        self.direccion = direccion
        self.id_Persona = id_Persona
        
    def __repr__(self):
        return '<Tecnico id_Persona= %r>' % self.id_Persona

#---------------------------------

#------------Producto-------------

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'nombre', 'descripcion', 'marca', 'tiene_Garantia', 'precio_SinFactura', 'precio_ConFactura', 'precio_Tecnico', 'id_Tecnico')
        
producto_schema_single = ProductoSchema()
producto_schema_multiple = ProductoSchema(many=True)

class Producto(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    nombre = mysql.Column(mysql.String(30), nullable=False)
    descripcion = mysql.Column(mysql.String(100), nullable=False)
    marca = mysql.Column(mysql.String(30), nullable=False)
    tiene_Garantia = mysql.Column(mysql.Integer, nullable=False)
    precio_SinFactura = mysql.Column(mysql.Numeric(6,2), nullable=False)
    precio_ConFactura = mysql.Column(mysql.Numeric(6,2), nullable=False)
    precio_Tecnico = mysql.Column(mysql.Numeric(6,2), nullable=False)
    id_Tecnico = mysql.Column(mysql.Integer, mysql.ForeignKey('tecnico.id'))

#---------------------------------

#------------Garantia-------------

class GarantiaSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'COD_Fabrica_Producto', 'fecha_Registro', 'meses_Valido', 'descripcion', 'estado', 'id_Producto')
        
garantia_schema_single = GarantiaSchema()
garantia_schema_multiple = GarantiaSchema(many=True)

class Garantia(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    COD_Fabrica_Producto = mysql.Column(mysql.String(45), nullable=False)
    fecha_Registro = mysql.Column(mysql.Date(), nullable=False)
    meses_Valido = mysql.Column(mysql.Integer, mullable=False)
    descripcion = mysql.Column(mysql.String(50), nullable=False)
    estado = mysql.Column(mysql.Integer, nullable=False)
    id_Producto = mysql.Column(mysql.Integer, mysql.ForeignKey('producto.id'), nullable=False)
    
    def __init__(self, COD_Fabrica_Producto, fecha_Registro, meses_Valido, descripcion, estado, id_Producto):
        self.COD_Fabrica_Producto = COD_Fabrica_Producto
        self.fecha_Registro = fecha_Registro
        self.meses_Valido = meses_Valido
        self.descripcion = descripcion
        self.estado = estado
        self.id_Persona = id_Persona
        
    def __repr__(self):
        return '<Garantia codigo_Producto=%r>' % self.COD_Fabrica_Producto

#---------------------------------

#--------Producto_Devuelto--------

class Producto_DevueltoSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'descripcion', 'id_Garantia', 'id_Producto')
        
producto_devuelto_schema_single = Producto_DevueltoSchema()
producto_devuelto_schema_multiple = Producto_DevueltoSchema(many=True)

class Producto_Devuelto(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    descripcion = mysql.Column(mysql.String(60), nullable=False)
    id_Garantia = mysql.Column(mysql.Integer, mysql.ForeignKey('garantia.id'), nullable=False)
    id_Producto = mysql.Column(mysql.Integer, mysql.ForeignKey('producto.id'), nullable=False)
    
    def __init__(self, ID, descripcion, id_Garantia, id_Producto):
        self.ID = ID
        self.decripcion = descripcion
        self.id_Garantia = id_Garantia
        self.id_Producto = id_Producto
        
    def __repr__(self):
        return '<Producto_Devuelto id_Garantia=%g, id_Producto=%p>' % self.id_Garantia, self.id_Producto

#---------------------------------

#-------------Venta---------------

class VentaSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'total', 'estado', 'id_Cliente', 'id_Empleado', 'id_Producto')

venta_schema_single = VentaSchema()
venta_schema_multiple = VentaSchema(many=True)

class Venta(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    total = mysql.Column(mysql.Numeric(6,2), nullable=False)
    estado = mysql.Column(mysql.Integer, nullable=False)
    id_Cliente = mysql.Column(mysql.Integer, mysql.ForeignKey('cliente.id'),nullable=False)
    id_Empleado = mysql.Column(mysql.Integer, mysql.ForeignKey('empleado.id'),nullable=False)
    id_Producto = mysql.Column(mysql.Integer, mysql.ForeignKey('producto.id'), nullable=False)
    
    def __init__(self, total, estado, id_Cliente, id_Empleado, id_Producto):
        self.total = total
        self.estado = estado
        self.id_Cliente = id_Cliente
        self.id_Empleado = id_Empleado
        self.id_Producto = id_Producto
    
    def __repr__(self):
        return '<Venta id_Producto=%r>' % self.id_Producto

#---------------------------------

#--------Producto_Vendido---------

class Producto_VendidoSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'cantidad', 'total', 'id_Producto', 'id_Venta')
        
producto_vendido_schema_single = Producto_VendidoSchema()
producto_vendido_schema_multiple = Producto_VendidoSchema(many=True)

class Producto_Vendido(mysql.Model):
    ID = mysql.Column(mysql.Integer, primary_key=True)
    cantidad = mysql.Column(mysql.Integer, nullable=True)
    total = mysql.Column(mysql.Numeric(6,2), nullable=True)
    id_Producto = mysql.Column(mysql.Integer, mysql.ForeignKey('producto.id'), nullable=False)
    id_Venta = mysql.Column(mysql.Integer, mysql.ForeignKey('venta.id', nullable=False))
    
    def __init__(self, cantidad, total, id_Producto, id_Venta):
        self.cantidad = cantidad
        self.total = total
        self.id_Producto = id_Producto
        self.id_Venta = id_Venta
        
    def __repr__(self):
        return '<Producto_Vendido id_Venta=%r>' % self.id_Venta

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

#-----------Inventario------------

class InventarioSchema(ma.Schema):
    class Meta:
        fields = ('cantidad', 'id_Sucursal', 'id_Producto')
        
inventario_schema_single = InventarioSchema()
inventario_schema_multiple = InventarioSchema(many=True)

class Inventario(mysql.Model):
    cantidad = mysql.Column(mysql.Integer, nullable = False)
    id_Sucursal = mysql.Column(mysql.Integer, mysql.ForeignKey('sucursal.id'), primary_key=True)
    id_Producto = mysql.Column(mysql.Integer, mysql.ForeignKey('producto.id'), primary_key=True)
    
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

class Permiso_AsignadoSchema(ma.Schema):
    class Meta:
        fields = ('estado', 'id_Permiso', 'id_Cuenta')
        
permiso_asignado_schema_single = Permiso_AsignadoSchema()
permiso_asignado_schema_multiple = Permiso_AsignadoSchema(many=True)

class Permiso_Asignado(mysql.Model):
    estado = mysql.Column(mysql.Integer, nullable=False)
    id_Permiso = mysql.Column(mysql.Integer, mysql.ForeignKey('permiso.id'), primary_key=True)
    id_Cuenta = mysql.Column(mysql.Integer, mysql.ForeignKey('cuenta.id'), primary_key=True)
    
    def __init__(self, estado, id_Permiso, id_Cuenta):
        self.estado = estado
        self.id_Permiso = id_Permiso
        self.id_Cuenta = id_Cuenta
        
    def __repr__(self):
        return '<Permiso_Asignado estado=$r>' % self.estado

#---------------------------------

mysql.create_all()