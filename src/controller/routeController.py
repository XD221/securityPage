from route.route import *

i_session = Session()

@app.route('/')
def ro_home():
    return home()
    
@app.route('/login')
def ro_login():
    return login()
    
@app.route('/restricted/register_Sales', methods=['GET'])
def ro_register_Sales():
    return register_Sales()

@app.route('/restricted/show_Sales', methods=['GET'])
def ro_show_Sales():
    return show_Sales()

#------------------Requests--------------------

#------------------Persona---------------------
@app.route('/request/persona/<number>', methods=['PUT'])
def req_put_persona(number):
    res_persona = Persona.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'CI' in request.json.keys():
        res_persona.CI = request.json['CI']
    if 'nombre' in request.json.keys():
        res_persona.nombre = request.json['nombre']
    if 'apellido_Paterno' in request.json.keys():
        res_persona.apellido_Paterno = request.json['apellido_Paterno']
    if 'apellido_Materno' in request.json.keys():
        res_persona.apellido_Materno = request.json['apellido_Materno']
    if 'sexo' in request.json.keys():
        res_persona.sexo = request.json['sexo']
    if 'telefono' in request.json.keys():
        res_persona.telefono = request.json['telefono']
    if 'email' in request.json.keys():
        res_persona.email = request.json['email']
    if 'fecha_Nacimiento' in request.json.keys():
        res_persona.fecha_Nacimiento = request.json['fecha_Nacimiento']
    mysql.session.commit()
    return "True"

@app.route('/request/persona', methods=['GET'])
def req_get_persona():
    all_persona = Persona.query.all()
    result = persona_schema_multiple.dump(all_persona)
    return jsonify(result)

@app.route('/request/persona/<number>', methods=['GET'])
def req_get_persona_select(number):
    res_persona = Persona.query.get(number)
    return persona_schema_single.jsonify(res_persona)

@app.route('/request/persona', methods=['POST'])
def req_post_persona():
    try:
        ci = request.json['CI']
        nombre = request.json['nombre']
        ap_P = request.json['apellido_Paterno']
        ap_M = request.json['apellido_Materno']
        sex = request.json['sexo']
        telef = request.json['telefono']
        email = request.json['email']
        fech_N = request.json['fecha_Nacimiento']
        new_persona = Persona(ci, nombre, ap_P, ap_M, sex, telef, email, fech_N)
        mysql.session.add(new_persona)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------    

#------------------Empleado---------------------
@app.route('/request/empleado/<number>', methods=['PUT'])
def req_put_empleado(number):
    res_empleado = Empleado.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'estado' in request.json.keys():
        res_empleado.estado = request.json['estado']
    #if 'id_persona' in request.json.keys():
    #    res_empleado.id_persona = request.json['id_persona']
    mysql.session.commit()
    return "True"

@app.route('/request/empleado', methods=['GET'])
def req_get_empleado():
    all_empleado = Empleado.query.all()
    result = empleado_schema_multiple.dump(all_empleado)
    return jsonify(result)

@app.route('/request/empleado/<number>', methods=['GET'])
def req_get_empleado_select(number):
    res_empleado = Empleado.query.get(number)
    return empleado_schema_single.jsonify(res_empleado)

@app.route('/request/empleado', methods=['POST'])
def req_post_empleado():
    try:
        estado = request.json['estado']
        id_persona = request.json['id_persona']
        new_empleado = Empleado(estado, id_persona)
        mysql.session.add(new_empleado)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#---------------------------------------------- 

#------------------Cuenta---------------------
@app.route('/request/cuenta/<number>', methods=['PUT'])
def req_put_cuenta(number):
    res_cuenta = Cuenta.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'nombre_Cuenta' in request.json.keys():
        res_cuenta.nombre_Cuenta = request.json['nombre_Cuenta']
    if 'urs_Password' in request.json.keys():
        res_cuenta.urs_Password = request.json['urs_Password']
    if 'urs_Llave' in request.json.keys():
        res_cuenta.urs_Llave = request.json['urs_Llave']
    if 'estado' in request.json.keys():
        res_cuenta.estado = request.json['estado']
    if 'id_empleado' in request.json.keys():
        res_cuenta.id_Empleado = request.json['id_Empleado']
    mysql.session.commit()
    return "True"

@app.route('/request/cuenta', methods=['GET'])
def req_get_cuenta():
    all_cuenta = Cuenta.query.all()
    result = cuenta_schema_multiple.dump(all_cuenta)
    return jsonify(result)

@app.route('/request/cuenta/<number>', methods=['GET'])
def req_get_cuenta_select(number):
    res_cuenta = Cuenta.query.get(number)
    return cuenta_schema_single.jsonify(res_cuenta)

@app.route('/request/cuenta', methods=['POST'])
def req_post_cuenta():
    try:
        nombre_C = request.json['nombre_Cuenta']
        passw = request.json['urs_Password']
        llav = request.json['urs_Llave']
        estado = request.json['estado']
        idEmpleado = request.json['id_Empleado']
        new_cuenta = Cuenta(nombre_C, passw, llav, estado, idEmpleado)
        mysql.session.add(new_cuenta)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------    

#------------------Cliente---------------------
@app.route('/request/cliente/<number>', methods=['PUT'])
def req_put_cliente(number):
    res_cliente = Cliente.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'NIT' in request.json.keys():
        res_cliente.NIT = request.json['NIT']
    if 'razon_Social' in request.json.keys():
        res_cliente.razon_Social = request.json['razon_Social']
    #if 'id_Persona' in request.json.keys():
    #    res_cliente.id_Persona = request.json['id_Persona']
    mysql.session.commit()
    return "True"

@app.route('/request/cliente', methods=['GET'])
def req_get_cliente():
    all_cliente = cliente.query.all()
    result = cliente_schema_multiple.dump(all_cliente)
    return jsonify(result)

@app.route('/request/cliente/<number>', methods=['GET'])
def req_get_cliente_select(number):
    res_cliente = Cliente.query.get(number)
    return cliente_schema_single.jsonify(res_cliente)

@app.route('/request/cliente', methods=['POST'])
def req_post_cliente():
    try:
        NIT = request.json['NIT']
        razon_S = request.json['razon_Social']
        id_P = request.json['id_Persona']
        new_cliente = Cliente(NIT, razon_S, id_P)
        mysql.session.add(new_cliente)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#------------------Tecnico---------------------
@app.route('/request/tecnico/<number>', methods=['PUT'])
def req_put_tecnico(number):
    res_tecnico = Tecnico.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'direccion' in request.json.keys():
        res_tecnico.direccion = request.json['direccion']
    if 'id_Persona' in request.json.keys():
        res_tecnico.id_Persona = request.json['id_Persona']
    mysql.session.commit()
    return "True"

@app.route('/request/tecnico', methods=['GET'])
def req_get_tecnico():
    all_tecnico = Tecnico.query.all()
    result = tecnico_schema_multiple.dump(all_tecnico)
    return jsonify(result)

@app.route('/request/tecnico/<number>', methods=['GET'])
def req_get_tecnico_select(number):
    res_tecnico = Tecnico.query.get(number)
    return tecnico_schema_single.jsonify(res_tecnico)

@app.route('/request/tecnico', methods=['POST'])
def req_post_tecnico():
    try:
        NIT = request.json['NIT']
        razon_S = request.json['razon_Social']
        id_P = request.json['id_Persona']
        new_tecnico = tecnico(NIT, razon_S, id_P)
        mysql.session.add(new_tecnico)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#------------------Producto---------------------
@app.route('/request/producto/<number>', methods=['PUT'])
def req_put_producto(number):
    res_producto = Producto.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'nombre' in request.json.keys():
        res_producto.nombre = request.json['nombre']
    if 'descripcion' in request.json.keys():
        res_producto.descripcion = request.json['descripcion']
    if 'marca' in request.json.keys():
        res_producto.marca = request.json['marca']
    if 'tiene_producto_Devolver' in request.json.keys():
        res_producto.tiene_producto_Devolver = request.json['tiene_producto_Devolver']
    if 'precio_SinFactura' in request.json.keys():
        res_producto.precio_SinFactura = request.json['precio_SinFactura']
    if 'precio_ConFactura' in request.json.keys():
        res_producto.precio_ConFactura = request.json['precio_ConFactura']
    if 'precio_Tecnico' in request.json.keys():
        res_producto.precio_Tecnico = request.json['precio_Tecnico']
    #if 'id_Tecnico' in request.json.keys():
    #    res_producto.id_Tecnico = request.json['id_Tecnico']
    mysql.session.commit()
    return "True"

@app.route('/request/producto', methods=['GET'])
def req_get_producto():
    all_producto = Producto.query.all()
    result = producto_schema_multiple.dump(all_producto)
    return jsonify(result)

@app.route('/request/producto/<number>', methods=['GET'])
def req_get_producto_select(number):
    res_producto = Producto.query.get(number)
    return producto_schema_single.jsonify(res_producto)

@app.route('/request/producto', methods=['POST'])
def req_post_producto():
    try:
        nombre = request.json['nombre']
        descripcion = request.json['descripcion']
        marca = request.json['marca']
        tiene_G = request.json['tiene_producto_Devolver']
        precio_SF = request.json['precio_SinFactura']
        precio_CF = request.json['precio_ConFactura']
        precio_T = request.json['precio_Tecnico']
        id_Pers = request.json['id_Persona']
        new_producto = Producto(nombre, descripcion, marca, tiene_G, precio_SF, precio_CF, precio_T, id_Pers)
        mysql.session.add(new_producto)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#------------------Garantia---------------------
@app.route('/request/garantia/<number>', methods=['PUT'])
def req_put_garantia(number):
    res_garantia = garantia.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'COD_Fabrica_Producto' in request.json.keys():
        res_garantia.COD_Fabrica_Producto = request.json['COD_Fabrica_Producto']
    if 'fecha_Registro' in request.json.keys():
        res_garantia.fecha_Registro = request.json['fecha_Registro']
    if 'meses_Valido' in request.json.keys():
        res_garantia.meses_Valido = request.json['meses_Valido']
    if 'descripcion' in request.json.keys():
        res_garantia.descripcion = request.json['descripcion']
    if 'estado' in request.json.keys():
        res_garantia.estado = request.json['estado']
    if 'id_Producto' in request.json.keys():
        res_garantia.id_Producto = request.json['id_Producto']
    mysql.session.commit()
    return "True"

@app.route('/request/garantia', methods=['GET'])
def req_get_garantia():
    all_garantia = Garantia.query.all()
    result = garantia_schema_multiple.dump(all_garantia)
    return jsonify(result)

@app.route('/request/garantia/<number>', methods=['GET'])
def req_get_garantia_select(number):
    res_garantia = Garantia.query.get(number)
    return garantia_schema_single.jsonify(res_garantia)

@app.route('/request/garantia', methods=['POST'])
def req_post_garantia():
    try:
        cod_F = request.json['COD_Fabrica_Producto']
        fecha_R = request.json['fecha_Registro']
        meses_V = request.json['meses_Valido']
        descripcion = request.json['descripcion']
        estado = request.json['estado']
        id_P = request.json['id_Producto']
        new_garantia = Garantia(cod_F, fecha_R, meses_V, descripcion, estado, id_P)
        mysql.session.add(new_garantia)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#----------------Producto_Devuelto-------------
@app.route('/request/producto_Devolver/<number>', methods=['PUT'])
def req_put_producto_Devolver(number):
    res_producto_Devolver = Producto_Devolver.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'descripcion' in request.json.keys():
        res_producto_Devolver.descripcion = request.json['descripcion']
    #if 'id_Garantia' in request.json.keys():
    #    res_producto_Devolver.id_Garamtia = request.json['id_Garantia']
    #if 'id_Producto' in request.json.keys():
    #    res_producto_Devolver.id_Producto = request.json['id_Producto']
    mysql.session.commit()
    return "True"

@app.route('/request/producto_Devolver', methods=['GET'])
def req_get_producto_Devolver():
    all_producto_Devolver = Producto_Devolver.query.all()
    result = producto_devolver_schema_multiple.dump(all_producto_Devolver)
    return jsonify(result)

@app.route('/request/producto_Devolver/<number>', methods=['GET'])
def req_get_producto_Devolver_select(number):
    res_producto_Devolver = Producto_Devolver.query.get(number)
    return producto_devolver_schema_single.jsonify(res_producto_Devolver)

@app.route('/request/producto_Devolver', methods=['POST'])
def req_post_producto_Devolver():
    try:
        descripcion = request.json['descripcion']
        id_Garantia = request.json['id_Garantia']
        id_Producto = request.json['id_Producto']
        new_producto_Devolver = Producto_Devolver(descripcion, id_Garantia, id_Producto)
        mysql.session.add(new_producto_Devolver)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#------------------Venta---------------------
@app.route('/request/venta/<number>', methods=['PUT'])
def req_put_venta(number):
    res_venta = Venta.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'total' in request.json.keys():
        res_venta.total = request.json['total']
    if 'estado' in request.json.keys():
        res_venta.estado = request.json['estado']
    #if 'id_Cliente' in request.json.keys():
    #    res_venta.id_Cliente = request.json['id_Cliente']
    #if 'id_Empleado' in request.json.keys():
    #    res_venta.id_Empleado = request.json['id_Empleado']
    #if 'id_Producto' in request.json.keys():
    #    res_venta.id_Producto = request.json['id_Producto']
    mysql.session.commit()
    return "True"

@app.route('/request/venta', methods=['GET'])
def req_get_venta():
    all_venta = Venta.query.all()
    result = venta_schema_multiple.dump(all_venta)
    return jsonify(result)

@app.route('/request/venta/<number>', methods=['GET'])
def req_get_venta_select(number):
    res_venta = Venta.query.get(number)
    return venta_schema_single.jsonify(res_venta)

@app.route('/request/venta', methods=['POST'])
def req_post_venta():
    try:
        total = request.json['total']
        estado = request.json['estado']
        id_Cliente = request.json['id_Cliente']
        id_Empleado = request.json['id_Empleado']
        id_Producto = request.json['id_Producto']
        new_venta = Venta(total, estado, id_Cliente, id_Empleado, id_Producto)
        mysql.session.add(new_venta)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#------------------Producto_Vendido---------------------
@app.route('/request/producto_Vendido/<number>', methods=['PUT'])
def req_put_producto_Vendido(number):
    res_producto_Vendido = Producto_Vendido.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'cantidad' in request.json.keys():
        res_producto_Vendido.cantidad = request.json['cantidad']
    if 'total' in request.json.keys():
        res_producto_Vendido.total = request.json['total']
    #if 'id_Producto' in request.json.keys():
    #    res_producto_Vendido.id_Producto = request.json['id_Producto']
    #if 'id_Venta' in request.json.keys():
    #    res_producto_Vendido.id_Venta = request.json['id_Venta']
    mysql.session.commit()
    return "True"

@app.route('/request/producto_Vendido', methods=['GET'])
def req_get_producto_Vendido():
    all_producto_Vendido = Producto_Vendido.query.all()
    result = producto_vendido_schema_multiple.dump(all_producto_Vendido)
    return jsonify(result)

@app.route('/request/producto_Vendido/<number>', methods=['GET'])
def req_get_producto_Vendido_select(number):
    res_producto_Vendido = Producto_Vendido.query.get(number)
    return producto_vendido_schema_single.jsonify(res_producto_Vendido)

@app.route('/request/producto_Vendido', methods=['POST'])
def req_post_producto_Vendido():
    try:
        cantidad = request.json['cantidad']
        total = request.json['total']
        id_Producto = request.json['id_Producto']
        id_Venta = request.json['id_Venta']
        new_producto_Vendido = Producto_Vendido(camtidad, total, id_Producto, id_Venta)
        mysql.session.add(new_producto_Vendido)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#--------------------Sucursal------------------
@app.route('/request/sucursal/<number>', methods=['PUT'])
def req_put_sucursal(number):
    res_sucursal = Sucursal.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'nombre' in request.json.keys():
        res_sucursal.nombre = request.json['nombre']
    if 'direccion' in request.json.keys():
        res_sucursal.direccion = request.json['direccion']
    mysql.session.commit()
    return "True"

@app.route('/request/sucursal', methods=['GET'])
def req_get_sucursal():
    all_sucursal = Sucursal.query.all()
    result = sucursal_schema_multiple.dump(all_sucursal)
    return jsonify(result)

@app.route('/request/sucursal/<number>', methods=['GET'])
def req_get_sucursal_select(number):
    res_sucursal = Sucursal.query.get(number)
    return sucursal_schema_single.jsonify(res_sucursal)

@app.route('/request/sucursal', methods=['POST'])
def req_post_sucursal():
    try:
        nombre = request.json['nombre']
        descripcion = request.json['descripcion']
        new_sucursal = Sucursal(nombre, descripcion)
        mysql.session.add(new_sucursal)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#-------------------Invetario------------------
@app.route('/request/invetario/<number>', methods=['PUT'])
def req_put_invetario(number):
    res_invetario = Invetario.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'cantidad' in request.json.keys():
        res_invetario.cantidad = request.json['cantidad']
    #if 'id_Sucursal' in request.json.keys():
    #    res_invetario.id_Sucursal = request.json['id_Sucursal']
    #if 'id_Producto' in request.json.keys():
    #    res_invetario.id_Producto = request.json['id_Producto']
    mysql.session.commit()
    return "True"

@app.route('/request/invetario', methods=['GET'])
def req_get_invetario():
    all_invetario = Invetario.query.all()
    result = invetario_schema_multiple.dump(all_invetario)
    return jsonify(result)

@app.route('/request/invetario/<number>', methods=['GET'])
def req_get_invetario_select(number):
    res_invetario = Invetario.query.get(number)
    return invetario_schema_single.jsonify(res_invetario)

@app.route('/request/invetario', methods=['POST'])
def req_post_invetario():
    try:
        cantidad = request.json['cantidad']
        id_Sucursal = request.json['id_Sucursal']
        id_Producto = request.json['id_Producto']
        new_invetario = Invetario(camtidad, id_Sucursal, id_Producto)
        mysql.session.add(new_invetario)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#-------------------Permiso------------------
@app.route('/request/permiso/<number>', methods=['PUT'])
def req_put_permiso(number):
    res_permiso = Permiso.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'nombre' in request.json.keys():
        res_permiso.nombre = request.json['nombre']
    if 'descripcion' in request.json.keys():
        res_permiso.descripcion = request.json['descripcion']
    mysql.session.commit()
    return "True"

@app.route('/request/permiso', methods=['GET'])
def req_get_permiso():
    all_permiso = Permiso.query.all()
    result = permiso_schema_multiple.dump(all_permiso)
    return jsonify(result)

@app.route('/request/permiso/<number>', methods=['GET'])
def req_get_permiso_select(number):
    res_permiso = Permiso.query.get(number)
    return permiso_schema_single.jsonify(res_permiso)

@app.route('/request/permiso', methods=['POST'])
def req_post_permiso():
    try:
        nombre = request.json['nombre']
        descripcion = request.json['descripcion']
        new_permiso = Permiso(nombre, descripcion)
        mysql.session.add(new_permiso)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#-------------------permiso_Asignado------------------
@app.route('/request/permiso_Asignado/<number>', methods=['PUT'])
def req_put_permiso_Asignado(number):
    res_permiso_Asignado = Permiso_Asignado.query.filter_by(id=number).first()
    if request.json is None:
        return "False"
    if 'estado' in request.json.keys():
        res_permiso_Asignado.estado = request.json['estado']
    if 'id_Permiso' in request.json.keys():
        res_permiso_Asignado.id_Permiso = request.json['id_Permiso']
    if 'id_Cuenta' in request.json.keys():
        res_permiso_Asignado.id_Cuenta = request.json['id_Cuenta']
    mysql.session.commit()
    return "True"

@app.route('/request/permiso_Asignado', methods=['GET'])
def req_get_permiso_Asignado():
    all_permiso_Asignado = Permiso_Asignado.query.all()
    result = permiso_asignado_schema_multiple.dump(all_permiso_Asignado)
    return jsonify(result)

@app.route('/request/permiso_Asignado/<number>', methods=['GET'])
def req_get_permiso_Asignado_select(number):
    res_permiso_Asignado = Permiso_Asignado.query.get(number)
    return permiso_asignado_schema_single.jsonify(res_permiso_Asignado)

@app.route('/request/permiso_Asignado', methods=['POST'])
def req_post_permiso_Asignado():
    try:
        estado = request.json['estado']
        id_P = request.json['id_Permiso']
        id_C = request.json['id_Cuenta']
        new_permiso_Asignado = Permiso_Asignado(estado, id_P, id_C)
        mysql.session.add(new_permiso_Asignado)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#----------------------------------------------