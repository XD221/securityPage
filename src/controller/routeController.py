from route.route import *


@app.route('/')
def ro_home():
    if isLogging():
        return home()
    return redirect("/login", code=302)

@app.route('/login', methods=['GET'])
def ro_get_login():
    if not isLogging():
        lg_message = ''
        if request is None:
            lg_message = 'vacio'
        return login(lg_message)
    return redirect("/", code=302)

@app.route('/login', methods=['POST'])
def ro_pos_login():
    lg_message = ''
    if request.form is not None:
        if request.form['lg_user'] is not None and request.form['lg_password'] is not None:
            lg_user = request.form['lg_user']
            lg_password = request.form['lg_password']
            lg_verf = signIn(lg_user, lg_password)
            lg_message = lg_verf
            if lg_verf  == 0:
                return redirect("/", code=302)
            if lg_verf == 1:
                lg_message = 'Your email/password combination is incorrect'
            elif lg_verf == 2:
                lg_message = 'Error: 404, Consult to a administrator'
    return login(lg_message)
    
@app.route('/logout', methods=['GET'])
def ro_logout():
    logout()
    return redirect("/", code=302)

@app.route('/profile', methods=['GET'])
def ro_profile():
    if isLogging():
        return profile('')
    return redirect("/login", code=302)

@app.route('/profile', methods=['POST'])
def ro_pr_chPass():
    if isLogging():
        if 'oldPass_field' not in request.form.keys():
            return profile('Error 500.1')
        if 'newPass_field' not in request.form.keys():
            return profile('Error 500.2')
        if 'confPass_field' not in request.form.keys():
            return profile('Error 500.3')
        oldPass = str(request.form['oldPass_field'])
        newPass = str(request.form['newPass_field'])
        confPass = str(request.form['confPass_field'])
        if newPass != confPass:
            return profile('Password do not match')
        global sess_global
        account_data = Cuenta.query.filter_by(ID=sess_global['user_id'], urs_Password=md5(oldPass.encode()).hexdigest()).first()
        if account_data is None:
            return profile('Password is incorrect')
        account_data.urs_Password = md5(newPass.encode()).hexdigest()
        mysql.session.commit()
        
        return redirect("/logout", code=302)
    return redirect("/login", code=302)

@app.route('/restricted/new_Client', methods=['GET'])
def ro_new_Client():
    return new_Client()
    
@app.route('/restricted/register_Sales', methods=['GET'])
def ro_register_Sales():
    return register_Sales()

@app.route('/restricted/show_Sales', methods=['GET'])
def ro_show_Sales():
    return show_Sales()

@app.route('/restricted/register_Inventory', methods=['GET'])
def ro_register_Inventory():
    return register_Inventory()

@app.route('/restricted/register_Product', methods=['GET'])
def ro_register_Product():
    return register_Product()

@app.errorhandler(404)
def page_not_found(e):
    if isLogging():
        return page_404()
    return redirect("/login", code=302)

#------------------Requests--------------------

#------------------Persona---------------------
@app.route('/request/persona/<number>', methods=['PUT'])
def req_put_persona(number):
    res_persona = Persona.query.filter_by(ID=number).first()
    if request.form is None or res_persona is None:
        return "False"
    if 'ci_field' in request.form.keys():
        res_persona.CI = request.form['ci_field']
    if 'name_field' in request.form.keys():
        res_persona.nombre = request.form['name_field']
    if 'fLast_field' in request.form.keys():
        res_persona.apellido_Paterno = request.form['fLast_field']
    if 'mLast_field' in request.form.keys():
        res_persona.apellido_Materno = request.form['mLast_field']
    if 'sex_field' in request.form.keys():
        res_persona.sexo = request.form['sex_field']
    if 'pNumber_field' in request.form.keys():
        res_persona.telefono = request.form['pNumber_field']
    if 'email_field' in request.form.keys():
        res_persona.email = request.form['email_field']
    if 'dBirth_field' in request.form.keys():
        res_persona.fecha_Nacimiento = request.form['dBirth_field']
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

#@app.route('/request/persona', methods=['POST'])
#def req_post_persona():
#    try:
#        dd_dt = request.form['dd-dt'].upper()
#        ci = request.form['ci_field']
#        nombre = request.form['name_field'].capitalize()
#        ap_P = request.form['fLast_field'].capitalize()
#        ap_M = request.form['mLast_field'].capitalize()
#        sex = request.form['sex_field']
#        telef = request.form['pNumber_field']
#        email = request.form['email_field']
#        fech_N = request.form['dBirth_field']
#        new_persona = Persona((dd_dt + '-' +ci), nombre, ap_P, ap_M, sex, telef, email, fech_N)
#        mysql.session.add(new_persona)
#        mysql.session.commit()
#        return redirect("/", code=302)
#    except KeyError as error:
#        return abort(400, str(error))

#----------------------------------------------    

#---------------Tipo Empleado------------------
@app.route('/request/tipo_Empleado/<number>', methods=['PUT'])
def req_put_tipo_Empleado(number):
    res_tipo_Empleado = Tipo_Empleado.query.filter_by(ID=number).first()
    if request.form is None or res_tipo_Empleado is None:
        return "False"
    if 'nombre' in request.form.keys():
        res_tipo_Empleado.nombre = request.form['nombre']
    if 'descripcion' in request.form.keys():
        res_tipo_Empleado.descripcion = request.form['descripcion']
    
    mysql.session.commit()
    return "True"

@app.route('/request/tipo_Empleado')
def req_get_tipo_Empleado():
    all_empleado = Empleado.query.all()
    result = tipo_empleado_schema_multiple.dump(all_empleado)
    return jsonify(result)

@app.route('/request/tipo_Empleado/<number>', methods=['GET'])
def req_get_tipo_Empleado_select(number):
    res_tipo_Empleado = Tipo_Empleado.query.get(number)
    return tipo_empleado_schema_single.jsonify(res_tipo_Empleado)

@app.route('/request/tipo_Empleado', methods=['POST'])
def req_post_tipo_Empleado():
    try:
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        new_Tipo_Empleado = Tipo_Empleado(nombre, descripcion)
        mysql.session.add(new_Tipo_Empleado)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#--------------------Sucursal------------------
@app.route('/request/sucursal/<number>', methods=['PUT'])
def req_put_sucursal(number):
    res_sucursal = Sucursal.query.filter_by(ID=number).first()
    if request.form is None or res_sucursal is None:
        return "False"
    if 'nombre' in request.form.keys():
        res_sucursal.nombre = request.form['nombre']
    if 'direccion' in request.form.keys():
        res_sucursal.direccion = request.form['direccion']
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
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        new_sucursal = Sucursal(nombre, descripcion)
        mysql.session.add(new_sucursal)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#------------------Empleado---------------------
@app.route('/request/empleado/<number>', methods=['PUT'])
def req_put_empleado(number):
    res_empleado = Empleado.query.filter_by(ID=number).first()
    if request.form is None or res_empleado is None:
        return "False"
    if 'estado' in request.form.keys():
        res_empleado.estado = request.form['estado']
    #if 'id_Persona' in request.form.keys():
    #    res_empleado.id_persona = request.form['id_Persona']
    #if 'id_TipoEmpleado' in request.form.keys():
    #   res_empleado.id_TipoEmpleado  = request.form['id_TipoEmpleado']
    #if 'id_Sucursal' in request.form.keys():
    #   res_empleado.id_Sucursal = request.form['id_Sucursal']
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
        estado = request.form['estado']
        id_Persona = request.form['id_Persona']
        id_TipoEmpleado = request.form['id_TipoEmpleado']
        id_Sucursal = request.form['id_Sucursal']
        new_empleado = Empleado(estado, id_Persona, id_TipoEmpleado, id_Sucursal)
        mysql.session.add(new_empleado)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#---------------------------------------------- 

#-------------------Cuenta---------------------
@app.route('/request/cuenta/<number>', methods=['PUT'])
def req_put_cuenta(number):
    res_cuenta = Cuenta.query.filter_by(ID=number).first()
    if request.form is None or res_cuenta is None:
        return "False"
    if 'nombre_Cuenta' in request.form.keys():
        res_cuenta.nombre_Cuenta = request.form['nombre_Cuenta']
    if 'urs_Password' in request.form.keys():
        res_cuenta.urs_Password = request.form['urs_Password']
    if 'url_Photo' in request.form.keys():
        res_cuenta.url_Photo = request.form['url_Photo']
    if 'estado' in request.form.keys():
        res_cuenta.estado = request.form['estado']
    if 'id_empleado' in request.form.keys():
        res_cuenta.id_Empleado = request.form['id_Empleado']
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
        nombre_C = request.form['nombre_Cuenta']
        passw = request.form['urs_Password']
        url_p = request.form['url_Photo']
        estado = request.form['estado']
        idEmpleado = request.form['id_Empleado']
        new_cuenta = Cuenta(nombre_C, passw, url_p, estado, idEmpleado)
        mysql.session.add(new_cuenta)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------    

#------------------Cliente---------------------
@app.route('/request/cliente/<number>', methods=['PUT'])
def req_put_cliente(number):
    res_cliente = Cliente.query.filter_by(ID=number).first()
    if request.form is None or res_cliente is None:
        return "False"
    if 'NIT' in request.form.keys():
        res_cliente.NIT = request.form['NIT']
    if 'razon_Social' in request.form.keys():
        res_cliente.razon_Social = request.form['razon_Social']
    #if 'id_Persona' in request.form.keys():
    #    res_cliente.id_Persona = request.form['id_Persona']
    mysql.session.commit()
    return "True"

@app.route('/request/cliente', methods=['GET'])
def req_get_cliente():
    all_cliente = Cliente.query.all()
    result = cliente_schema_multiple.dump(all_cliente)
    return jsonify(result)

@app.route('/request/cliente/<number>', methods=['GET'])
def req_get_cliente_select(number):
    res_cliente = Cliente.query.get(number)
    return cliente_schema_single.jsonify(res_cliente)

@app.route('/request/cliente', methods=['POST'])
def req_post_cliente():
    try:
        dd_dt = request.form['dd-dt'].upper()
        ci = request.form['ci_field']
        nombre = request.form['name_field'].capitalize()
        ap_P = request.form['fLast_field'].capitalize()
        ap_M = request.form['mLast_field'].capitalize()
        sex = request.form['sex_field']
        telef = request.form['pNumber_field']
        email = request.form['email_field']
        fech_N = request.form['dBirth_field']
        new_persona = Persona((dd_dt + '-' +ci), nombre, ap_P, ap_M, sex, telef, email, fech_N)
        mysql.session.add(new_persona)
        mysql.session.commit()
        NIT = request.form['nit_field'] if request.form['nit_field'] != '' else 0
        razon_S = request.form['rSocial_field'].capitalize()
        id_P = new_persona.ID #request.form['id_Persona']
        new_cliente = Cliente(NIT, razon_S, id_P)
        mysql.session.add(new_cliente)
        mysql.session.commit()
        return redirect("/", code=302)
    except KeyError as error:
        return abort(400, str(error))

#----------------------------------------------

#------------------Tecnico---------------------
@app.route('/request/tecnico/<number>', methods=['PUT'])
def req_put_tecnico(number):
    res_tecnico = Tecnico.query.filter_by(ID=number).first()
    if request.form is None or res_tecnico is None:
        return "False"
    if 'direccion' in request.form.keys():
        res_tecnico.direccion = request.form['direccion']
    if 'estado' in request.form.keys():
        res_tecnico.estado = request.form['estado']
    if 'id_Persona' in request.form.keys():
        res_tecnico.id_Persona = request.form['id_Persona']
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
        direccion = request.form['direccion']
        estado = request.form['estado']
        id_Persona = request.form['id_Persona']
        new_tecnico = Tecnico(direccion, estado, id_Persona)
        mysql.session.add(new_tecnico)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#-----------------------------------------------

#--------------------Marca----------------------

@app.route('/request/marca/<number>', methods=['PUT'])
def req_put_marca(number):
    res_marca = Marca.query.filter_by(ID=number).first()
    if request.form is not None or res_marca is None:
        return 'False'
    if 'nombre' in request.form.keys():
        res_marca.nombre = request.form['nombre']
    mysql.session.commit()
    return "True"
    
@app.route('/request/marca', methods=['GET'])


#-----------------------------------------------


#------------------Producto---------------------
@app.route('/request/producto/<number>', methods=['PUT'])
def req_put_producto(number):
    res_producto = Producto.query.filter_by(ID=number).first()
    if request.form is None or res_producto is None:
        return "False"
    if 'nombre' in request.form.keys():
        res_producto.nombre = request.form['nombre']
    if 'descripcion' in request.form.keys():
        res_producto.descripcion = request.form['descripcion']
    if 'precio_SinFactura' in request.form.keys():
        res_producto.precio_SinFactura = request.form['precio_SinFactura']
    if 'precio_ConFactura' in request.form.keys():
        res_producto.precio_ConFactura = request.form['precio_ConFactura']
    if 'precio_Tecnico' in request.form.keys():
        res_producto.precio_Tecnico = request.form['precio_Tecnico']
    if 'garantia_Meses_Valido' in request.form.keys():
        res_producto.garantia_Meses_Valido = request.form['garantia_Meses_Valido']
    if 'id_Marca' in request.form.keys():
        res_producto.id_Marca = request.form['id_Marca']
    #if 'id_Tecnico' in request.form.keys():
    #    res_producto.id_Tecnico = request.form['id_Tecnico']
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
        data_Brand = getData('data_Brand')
        
        if data_Brand is None:
            return abort(400)
        
        data_Technician = getData('data_Technician')
        
        if data_Technician is None:
            return "False"
        
        nombre = request.form['name_field']
        descripcion = request.form['description_field']
        request_marca =  request.form['brand_field']
        request_tecnico = str(request.form['technician_field']).split(sep="-", maxsplit=1)
        id_Marca = 0
        id_tec = None
        g_m_v = 0
        
        for i in data_Brand:
            if str(i.nombre) == str(request_marca):
                id_Marca = i.ID
        
        if id_Marca == 0:
           return "False"
           
        for i in data_Technician:
            if str(i.nombre + ' ' + i.apellido_Paterno + ' ' + i.apellido_Materno).lower() == request_tecnico[0].lower().strip():
                if str(i.telefono) == request_tecnico[1 ].strip():
                    id_tec = i.Tecnico.ID
           
        if id_tec is not None:
            g_m_v = int(request.form['gt_field']) 
        
        precio_SF = float(request.form['pwob_field'])
        precio_CF = float(request.form['pwb_field'])
        precio_T = float(request.form['tpr_field'])
        new_producto = Producto(nombre, descripcion, precio_SF, precio_CF, precio_T, g_m_v, id_Marca, id_tec)
        mysql.session.add(new_producto)
        mysql.session.commit()
        return redirect("/", code=302)
    except KeyError as error:
        return abort(400, str(error))

#----------------------------------------------

#-------------------------Venta-------------------------

@app.route('/request/venta/<number>', methods=['PUT'])
def req_put_venta(number):
    res_venta = Venta.query.filter_by(ID=number).first()
    if request.form is None or res_venta is None:
        return "False"
    if 'total' in request.form.keys():
        res_venta.total = request.form['total']
    if 'fecha_Venta' in request.form.keys():
        res_venta.fecha_Venta = request.form['fecha_Venta']
    if 'estado' in request.form.keys():
        res_venta.estado = request.form['estado']
    #if 'id_Cliente' in request.form.keys():
    #    res_venta.id_Cliente = request.form['id_Cliente']
    #if 'id_Empleado' in request.form.keys():
    #    res_venta.id_Empleado = request.form['id_Empleado']
    #if 'id_Sucursal' in request.form.keys():
    #    res_venta.id_Sucursal = request.form['fecha_Venta']
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
        total = request.form['total']
        fecha_V = request.form['fecha_Venta']
        estado = request.form['estado']
        id_Cliente = request.form['id_Cliente']
        id_Empleado = request.form['id_Empleado']
        new_venta = Venta(total, fecha_V, estado, id_Cliente, id_Empleado)
        mysql.session.add(new_venta)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#-------------------------------------------------------

#------------------Producto_Vendido---------------------
@app.route('/request/producto_Vendido/<idproducto>/<idventa>', methods=['PUT'])
def req_put_producto_Vendido(idproducto, idventa):
    res_producto_Vendido = Producto_Vendido.query.filter_by(id_Producto=idproducto, id_Venta=idventa).first()
    if request.form is None or res_producto_Vendido is None:
        return "False"
    if 'cantidad' in request.form.keys():
        res_producto_Vendido.cantidad = request.form['cantidad']
    if 'total' in request.form.keys():
        res_producto_Vendido.total = request.form['total']
    #if 'id_Producto' in request.form.keys():
    #    res_producto_Vendido.id_Producto = request.form['id_Producto']
    #if 'id_Venta' in request.form.keys():
    #    res_producto_Vendido.id_Venta = request.form['id_Venta']
    mysql.session.commit()
    return "True"

@app.route('/request/producto_Vendido', methods=['GET'])
def req_get_producto_Vendido():
    all_producto_Vendido = Producto_Vendido.query.all()
    result = producto_vendido_schema_multiple.dump(all_producto_Vendido)
    return jsonify(result)

@app.route('/request/producto_Vendido/<idproducto>/<idventa>', methods=['GET'])
def req_get_producto_Vendido_select(idproducto, idventa):
    res_producto_Vendido = Producto_Vendido.query.get((idproducto, idventa))
    return producto_vendido_schema_single.jsonify(res_producto_Vendido)

@app.route('/request/producto_Vendido', methods=['POST'])
def req_post_producto_Vendido():
    try:
        cantidad = request.form['cantidad']
        total = request.form['total']
        id_Producto = request.form['id_Producto']
        id_Venta = request.form['id_Venta']
        new_producto_Vendido = Producto_Vendido(cantidad, total, id_Producto, id_Venta)
        mysql.session.add(new_producto_Vendido)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#------------------Garantia---------------------
@app.route('/request/garantia/<number>', methods=['PUT'])
def req_put_garantia(number):
    res_garantia = Garantia.query.filter_by(ID=number).first()
    if request.form is None or res_garantia is None:
        return "False"
    if 'COD_Fabrica_Producto' in request.form.keys():
        res_garantia.COD_Fabrica_Producto = request.form['COD_Fabrica_Producto']
    if 'fecha_Registro' in request.form.keys():
        res_garantia.fecha_Registro = request.form['fecha_Registro']
    if 'fecha_Vencimiento' in request.form.keys():
        res_garantia.fecha_Vencimiento = request.form['fecha_Vencimiento']
    if 'descripcion' in request.form.keys():
        res_garantia.descripcion = request.form['descripcion']
    if 'estado' in request.form.keys():
        res_garantia.estado = request.form['estado']
    #if 'id_Venta' in request.form.keys():
    #    res_garantia.id_Venta = request.form['id_Venta']
    #if 'id_Producto' in request.form.keys():
    #    res_garantia.id_Producto = request.form['id_Producto']
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
        cod_F = request.form['COD_Fabrica_Producto']
        fecha_R = request.form['fecha_Registro']
        fecha_V = request.form['fecha_Vencimiento']
        descripcion = request.form['descripcion']
        estado = request.form['estado']
        id_V = request.form['id_Venta']
        id_P = request.form['id_Producto']
        new_garantia = Garantia(cod_F, fecha_R, fecha_V, descripcion, estado, id_V, id_P)
        mysql.session.add(new_garantia)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#----------------Producto_Devuelto-------------
@app.route('/request/producto_Devolver/<number>', methods=['PUT'])
def req_put_producto_Devolver(number):
    res_producto_Devolver = Producto_Devuelto.query.filter_by(ID=number).first()
    if request.form is None or res_producto_Devolver is None:
        return "False"
    if 'descripcion' in request.form.keys():
        res_producto_Devolver.descripcion = request.form['descripcion']
    #if 'id_Garantia' in request.form.keys():
    #    res_producto_Devolver.id_Garamtia = request.form['id_Garantia']
    #if 'id_Producto' in request.form.keys():
    #    res_producto_Devolver.id_Producto = request.form['id_Producto']
    mysql.session.commit()
    return "True"

@app.route('/request/producto_Devolver', methods=['GET'])
def req_get_producto_Devolver():
    all_producto_Devolver = Producto_Devuelto.query.all()
    result = producto_devuelto_schema_multiple.dump(all_producto_Devolver)
    return jsonify(result)

@app.route('/request/producto_Devolver/<number>', methods=['GET'])
def req_get_producto_Devolver_select(number):
    res_producto_Devolver = Producto_Devuelto.query.get(number)
    return producto_devuelto_schema_single.jsonify(res_producto_Devolver)

@app.route('/request/producto_Devolver', methods=['POST'])
def req_post_producto_Devolver():
    try:
        descripcion = request.form['descripcion']
        id_Garantia = request.form['id_Garantia']
        id_Producto = request.form['id_Producto']
        new_producto_Devolver = Producto_Devuelto(descripcion, id_Garantia, id_Producto)
        mysql.session.add(new_producto_Devolver)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#-------------------------------------------------------

#-------------------Invetario------------------
@app.route('/request/inventario/<number>', methods=['PUT'])
def req_put_invetario(number):
    res_inventario = Inventario.query.filter_by(ID=number).first()
    if request.form is None or res_inventario is None:
        return "False"
    if 'cantidad' in request.form.keys():
        res_inventario.cantidad = request.form['cantidad']
    #if 'id_Sucursal' in request.form.keys():
    #    res_inventario.id_Sucursal = request.form['id_Sucursal']
    #if 'id_Producto' in request.form.keys():
    #    res_inventario.id_Producto = request.form['id_Producto']
    mysql.session.commit()
    return "True"

@app.route('/request/inventario', methods=['GET'])
def req_get_invetario():
    all_invetario = Inventario.query.all()
    result = inventario_schema_multiple.dump(all_invetario)
    return jsonify(result)

@app.route('/request/inventario/<number>', methods=['GET'])
def req_get_invetario_select(number):
    res_invetario = Inventario.query.get(number)
    return inventario_schema_single.jsonify(res_invetario)

@app.route('/request/inventario', methods=['POST'])
def req_post_invetario():
    try:
        cantidad = request.form['cantidad']
        id_Sucursal = request.form['id_Sucursal']
        id_Producto = request.form['id_Producto']
        new_invetario = Inventario(cantidad, id_Sucursal, id_Producto)
        mysql.session.add(new_invetario)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#-------------------Permiso------------------
@app.route('/request/permiso/<number>', methods=['PUT'])
def req_put_permiso(number):
    res_permiso = Permiso.query.filter_by(ID=number).first()
    if request.form is None or res_permiso is None:
        return "False"
    if 'nombre' in request.form.keys():
        res_permiso.nombre = request.form['nombre']
    if 'descripcion' in request.form.keys():
        res_permiso.descripcion = request.form['descripcion']
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
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        new_permiso = Permiso(nombre, descripcion)
        mysql.session.add(new_permiso)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#-------------------------------------------------------

#-------------------permiso_Asignado--------------------
@app.route('/request/permiso_Asignado/<idpermiso>/<idcuenta>', methods=['PUT'])
def req_put_permiso_Asignado(idpermiso, idcuenta):
    res_permiso_Asignado = Permiso_Asignado.query.filter_by(id_Permiso=idpermiso, id_Cuenta=idcuenta).first()
    if request.form is None or res_permiso_Asignado is None:
        return "False"
    if 'estado' in request.form.keys():
        res_permiso_Asignado.estado = request.form['estado']
    #if 'id_Permiso' in request.form.keys():
    #    res_permiso_Asignado.id_Permiso = request.form['id_Permiso']
    #if 'id_Cuenta' in request.form.keys():
    #    res_permiso_Asignado.id_Cuenta = request.form['id_Cuenta']
    mysql.session.commit()
    return "True"

@app.route('/request/permiso_Asignado', methods=['GET'])
def req_get_permiso_Asignado():
    all_permiso_Asignado = Permiso_Asignado.query.all()
    result = permiso_asignado_schema_multiple.dump(all_permiso_Asignado)
    return jsonify(result)

@app.route('/request/permiso_Asignado/<idpermiso>/<idcuenta>', methods=['GET'])
def req_get_permiso_Asignado_select(idpermiso, idcuenta):
    res_permiso_Asignado = Permiso_Asignado.query.get((idpermiso, idcuenta))
    return permiso_asignado_schema_single.jsonify(res_permiso_Asignado)

@app.route('/request/permiso_Asignado', methods=['POST'])
def req_post_permiso_Asignado():
    try:
        estado = request.form['estado']
        id_P = request.form['id_Permiso']
        id_C = request.form['id_Cuenta']
        new_permiso_Asignado = Permiso_Asignado(estado, id_P, id_C)
        mysql.session.add(new_permiso_Asignado)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#----------------------------------------------