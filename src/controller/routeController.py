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

@app.route('/restricted/client', methods=['GET'])
def ro_client():
    return client()
    
@app.route('/restricted/sales', methods=['GET'])
def ro_sales():
    return sales()

@app.route('/restricted/inventory', methods=['GET'])
def ro_inventory():
    return inventory()

@app.route('/restricted/product', methods=['GET'])
def ro_product():
    return product()

@app.route('/variable/data', methods=['POST'])
def var_data():
    if isLogging():
        req_data = request.form.get('req_data');
        if req_data is None:
            return "False"
        saveData('req_data', req_data);
        return 'True'
    else:
        return redirect("/login", code=302)


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

@app.route('/request/persona_var', methods=['GET'])
def req_get_persona_var():
    if isLogging():
        req_nomComp = request.args.get('fName')
        if req_nomComp is None:
            req_nomComp = ''
        else:
            req_nomComp = "%{}%".format(req_nomComp)
        req_ci = request.args.get('CI')
        if req_ci is None:
            req_ci = ''
        else:
            req_ci = "%{}%".format(req_ci)
        req_dep = str(request.args.get('dep')).upper()
        if req_dep is None:
            req_dep = ''
        else:
            req_dep = "%{}%".format(req_dep)
        req_data = mysql.session.query(Persona.ID, Persona.nombre, Persona.apellido_Paterno, Persona.apellido_Materno, Persona.CI).filter(((Persona.nombre.like(req_nomComp)) | (Persona.apellido_Paterno.like(req_nomComp)) | (Persona.apellido_Materno.like(req_nomComp))), Persona.CI.like(req_dep), Persona.CI.like(req_ci)).limit(10).all()
        result = []
        for persona in req_data:
            content = {'ID': persona.ID, 'CI': persona.CI, 'nombre': persona.nombre, 'apellido_Paterno': persona.apellido_Paterno, 'apellido_Materno': persona.apellido_Materno}
            result.append(content)
        return jsonify(result)
    else:
        return redirect("/login", code=302)

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
@app.route('/request/tipo_empleado/<number>', methods=['PUT'])
def req_put_tipo_empleado(number):
    res_tipo_empleado = Tipo_Empleado.query.filter_by(ID=number).first()
    if request.form is None or res_tipo_empleado is None:
        return "False"
    if 'nombre' in request.form.keys():
        res_tipo_empleado.nombre = request.form['nombre']
    if 'descripcion' in request.form.keys():
        res_tipo_empleado.descripcion = request.form['descripcion']
    
    mysql.session.commit()
    return "True"

@app.route('/request/tipo_empleado')
def req_get_tipo_empleado():
    all_empleado = Empleado.query.all()
    result = tipo_empleado_schema_multiple.dump(all_empleado)
    return jsonify(result)

@app.route('/request/tipo_empleado/<number>', methods=['GET'])
def req_get_tipo_empleado_select(number):
    res_tipo_empleado = Tipo_Empleado.query.get(number)
    return tipo_empleado_schema_single.jsonify(res_tipo_empleado)

@app.route('/request/tipo_empleado', methods=['POST'])
def req_post_tipo_empleado():
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
    if isLogging():
        res_cliente = Cliente.query.filter_by(ID=number).first()
        if request.form is None or res_cliente is None:
            return "False"
        if 'NIT' in request.form.keys():
            res_cliente.NIT = json.loads(request.form.get('NIT'))
        if 'razon_Social' in request.form.keys():
            res_cliente.razon_Social = json.loads(request.form.get('razon_Social'))
        #if 'id_Persona' in request.form.keys():
        #    res_cliente.id_Persona = request.form['id_Persona']
        mysql.session.commit()
        return "True"
    else:
        return "False"

@app.route('/request/cliente', methods=['GET'])
def req_get_cliente():
    all_cliente = Cliente.query.all()
    result = cliente_schema_multiple.dump(all_cliente)
    return jsonify(result)

@app.route('/request/cliente/<number>', methods=['GET'])
def req_get_cliente_select(number):
    res_cliente = Cliente.query.get(number)
    return cliente_schema_single.jsonify(res_cliente)

@app.route('/request/cliente_var', methods=['GET'])
def req_get_cliente_var():
    if isLogging():
        req_nomComp = request.args.get('fName')
        if req_nomComp is None:
            req_nomComp = ''
        else:
            req_nomComp = "%{}%".format(req_nomComp)
        req_ci = request.args.get('CI')
        if req_ci is None:
            req_ci = ''
        else:
            req_ci = "%{}%".format(req_ci)
        req_dep = str(request.args.get('dep')).upper()
        if req_dep is None:
            req_dep = ''
        else:
            req_dep = "%{}%".format(req_dep)
        req_data = mysql.session.query(Persona.ID, Persona.nombre, Persona.apellido_Paterno, Persona.apellido_Materno, Persona.CI, Cliente).filter(Persona.ID == Cliente.id_Persona, ((Persona.nombre.like(req_nomComp)) | (Persona.apellido_Paterno.like(req_nomComp)) | (Persona.apellido_Materno.like(req_nomComp))), Persona.CI.like(req_dep), Persona.CI.like(req_ci)).limit(10).all()
        result = []
        for cliente in req_data:
            content = {'ID': cliente.Cliente.ID, 'CI': cliente.CI, 'nombre': cliente.nombre, 'apellido_Paterno': cliente.apellido_Paterno, 'apellido_Materno': cliente.apellido_Materno, 'NIT': cliente.Cliente.NIT, 'razon_Social': cliente.Cliente.razon_Social}
            result.append(content)
        return jsonify(result)
    else:
        return redirect("/login", code=302)

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
def request_get_marca():
    res_marca = Marca.query.all()
    result = marca_schema_multiple.dump(res_marca)
    return jsonify(result)

@app.route('/request/marca_greater-id=<number>', methods=['GET'])
def request_get_marca_greaterId(number):
    res_marca = Marca.query.filter(Marca.ID > number).limit(10).all()
    result = marca_schema_multiple.dump(res_marca)
    return jsonify(result)

@app.route('/request/marca_less-id=<number>', methods=['GET'])
def request_get_marca_lessId(number):
    res_marca = Marca.query.filter(Marca.ID <= number).order_by(Marca.ID.asc()).limit(10).all()
    result = marca_schema_multiple.dump(res_marca)
    return jsonify(result)
    
@app.route('/request/marca/<name>', methods=['GET'])
def req_get_searchName_marca(name):
    if isLogging():
        sear_name = "{}%".format(name)
        res_marca = Marca.query.filter(Marca.nombre.like(sear_name)).limit(10).all()
        result = marca_schema_multiple.dump(res_marca)
        return jsonify(result)

    else:
        return redirect("/login", code=302)

#-----------------------------------------------

#------------------Categoria--------------------

@app.route('/request/categoria/<number>', methods=['PUT'])
def req_put_categoria(number):
    res_categoria = Categoria.query.filter_by(ID = number).first()
    if request.form is None or res_categoria is None:
        return "False"
    if 'nombre' in request.form.keys():
        res_categoria.nombre = request.form['nombre']
    mysql.session.commit()
    return "True"

@app.route('/request/categoria', methods=['GET'])
def req_get_categoria():
    all_categoria = Categoria.query.all()
    result = categoria_schema_multiple.dump(all_categoria)
    return jsonify(result)

@app.route('/request/categoria/<number>', methods=['GET'])
def req_get_categoria_select(number):
    res_categoria = Categoria.query.get(number)
    return categoria_schema_single.jsonify(res_categoria)

@app.route('/request/categoria', methods=['POS'])
def req_post_categoria():
    try:
        nombre = request.form['nombre']
        new_categoria = Categoria(nombre)
        mysql.session.add(new_categoria)
        mysql.session.commit()
        return redirect("/", code=302)
    except KeyError as error:
        return abort(400, str(error))

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

@app.route('/request/producto_var', methods=['GET'])
def req_get_producto_var():
    if isLogging():
        req_nom = request.args.get('name')
        if req_nom is None:
            req_nom = '%%'
        else:
            req_nom = "%{}%".format(req_nom)
        req_mar = request.args.get('brand')
        if req_mar is None:
            req_mar = '%%'
        else:
            req_mar = "%{}%".format(req_mar)
        req_cat = request.args.get('category')
        if req_cat is None:
            req_cat = '%%'
        else:
            req_cat = "%{}%".format(req_cat)
        req_data = mysql.session.query(Producto.ID, Producto.nombre, Producto.garantia_Meses_Valido, Producto.precio_ConFactura, Producto.precio_SinFactura, Producto.precio_Tecnico, Producto.id_Marca, Producto.id_Categoria, Categoria, Marca, Sucursal, Inventario).filter(Sucursal.ID == getData('sucursal_id'), Inventario.cantidad > 0, Sucursal.ID == Inventario.id_Sucursal, Inventario.id_Producto == Producto.ID, Producto.id_Marca == Marca.ID, Producto.id_Categoria == Categoria.ID, Producto.nombre.like(req_nom), Categoria.nombre.like(req_cat), Marca.nombre.like(req_mar)).limit(10).all()
        result = []
        for data in req_data:
            content = {'ID': data.ID, 'nombre': data.nombre, 'garantia_Meses_Valido': data.garantia_Meses_Valido, 'Marca': data.Marca.nombre, 'Categoria': str(data.Categoria.nombre), 'p_conFactura': str(data.precio_ConFactura), 'p_sinFactura': str(data.precio_SinFactura), 'p_tecnico': str(data.precio_Tecnico), 'cantidad_d': str(data.Inventario.cantidad)}
            result.append(content)
        return jsonify(result)
    else:
        return redirect("/login", code=302)

@app.route('/request/producto', methods=['POST'])
def req_post_producto():
    try:
        data_Brand = getData('data_Brand')
        
        if data_Brand is None:
            return "False"
        
        data_Technician = getData('data_Technician')
        
        if data_Technician is None:
            return "False"
        
        data_Category = getData('data_Category')
        
        if data_Category is None:
            return "False"
        
        
        
        nombre = request.form['name_field']
        descripcion = request.form['description_field']
        request_marca =  request.form['brand_field']
        request_tecnico = str(request.form['technician_field']).split(sep="-", maxsplit=1)
        request_categoria = request.form['category_field']
        id_Marca = 0
        id_cater = 0
        id_tec = None
        g_m_v = 0
        
        for i in data_Brand:
            if str(i.nombre) == str(request_marca):
                id_Marca = i.ID
        
        if id_Marca == 0:
           return "False"
       
        for i in data_Category:
            if str(i.nombre) == str(request_categoria):
                id_cater = i.ID
               
        if id_cater == 0:
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
        new_producto = Producto(nombre, descripcion, precio_SF, precio_CF, precio_T, g_m_v, id_Marca, id_cater, id_tec)
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
    if 'tiene_Factura' in request.form.keys():
        res_venta.tiene_Factura = request.form['tiene_Factura']
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
        data_products = getData('req_data')
        saveData('req_data', None)
        #data_products = json.dumps(data_products)
        data_products = json.loads(data_products)
        total = request.form.get('rsl-result-totalPrice')
        if total is None:
            return 'False'
        total = float(total)
        now = datetime.now()
        fecha_V = now.strftime('%Y/%m/%d')
        tiene_Fac = request.form.getlist('rsl-bill-check')
        if tiene_Fac is None:
            return 'False'
        elif not tiene_Fac:
            tiene_Fac = False
        elif tiene_Fac[0] == 'on':
            tiene_Fac = True
        estado = 0
        data_Client = str(request.form['rsl-sClient_field'])
        req_Client = None
        if(data_Client.lower() == 'anonimo'):
            req_Client = mysql.session.query(Cliente, Persona.nombre, Persona.apellido_Paterno, Persona.apellido_Materno, Persona.CI).filter(Cliente.ID == 1).first()
            if req_Client is None:
                return "False"
        else:
            data_Client = data_Client.split(sep="--", maxsplit=1)
            data_CI = data_Client[1].strip().split(sep="/", maxsplit=1)
            if data_CI[0].lower() == 'pando':
                data_CI[0] = 'pa'
            elif data_CI[0].lower() == 'beni':
                data_CI[0] = 'be'
            elif data_CI[0].lower() == 'la paz':
                data_CI[0] = 'lp'
            elif data_CI[0].lower() == 'oruro':
                data_CI[0] = 'or'
            elif data_CI[0].lower() == 'potosí':
                data_CI[0] = 'po'
            elif data_CI[0].lower() == 'tarija':
                data_CI[0] = 'ta'
            elif data_CI[0].lower() == 'chuquisaca':
                data_CI[0] = 'ch'
            elif data_CI[0].lower() == 'cochabamba':
                data_CI[0] = 'co'
            elif data_CI[0].lower() == 'santa cruz':
                data_CI[0] = 'sa'
            elif data_CI[0].lower() == 'extranjero':
                data_CI[0] = 'ex'
            elif data_CI[0].lower() == 'ninguno':
                data_CI[0] = 'nu'
            else:
                return "False"
            data_CI[0] = data_CI[0].upper()
            data_CI = data_CI[0] + '-' + data_CI[1]
            req_Client = mysql.session.query(Cliente, Persona.nombre, Persona.apellido_Paterno, Persona.apellido_Materno, Persona.CI).filter(Cliente.id_Persona == Persona.ID, Persona.CI == data_CI).first()
            if req_Client is None:
                return "False"
        id_Cliente = req_Client.Cliente.ID
        id_Empleado = getData('em_id')
        id_Sucursal = mysql.session.query(Sucursal, Empleado.ID, Empleado.id_Sucursal).filter(Empleado.ID == id_Empleado, Empleado.id_Sucursal == Sucursal.ID).first().Sucursal.ID
        new_venta = Venta(total, fecha_V, tiene_Fac, estado, id_Cliente, id_Empleado, id_Sucursal)
        mysql.session.add(new_venta)
        mysql.session.commit()
        id_Venta = new_venta.ID
        for i in data_products[0]:
            req_Products = Producto.query.filter(Producto.nombre == i['name']).first()
            id_Product = req_Products.ID
            req_Price = float(i['price'])
            req_amount = int(i['amount'])
            req_Total = float("{:.2f}".format(req_Price * req_amount))
            new_ProductoVendido = Producto_vendido(req_Price, req_amount, req_Total, id_Product, id_Venta)
            req_maxAmount = int(i['maxAmount'])
            res_inventario = Inventario.query.filter_by(id_Sucursal = id_Sucursal, id_Producto = id_Product).first()
            res_inventario.cantidad = req_maxAmount - req_amount
            mysql.session.add(new_ProductoVendido)
            mysql.session.commit()
        for i in data_products[1]:
            req_Products = Producto.query.filter(Producto.nombre == i['name']).first()
            id_Product = req_Products.ID
            now = datetime.now()
            date_regis = now.strftime('%Y/%m/%d')
            date_V = datetime.strptime(i['date'], '%d/%m/%Y').date()
            date_V = date_V.strftime('%Y/%m/%d')
            code_F = str(i['code']).upper()
            new_Garantia = Garantia(code_F, date_regis, date_V, estado, id_Venta, id_Product)
            mysql.session.add(new_Garantia)
        if tiene_Fac:
            NIT = request.form['rsl-pr-sNIT_field']
            if NIT == '':
                NIT = 0
            raz_Soc = request.form['rsl-pr-sRSocial_field']
            new_Factura = Factura(NIT, raz_Soc, id_Venta)
            mysql.session.add(new_Factura)
        mysql.session.commit()
        return redirect("/", code=302)
    except KeyError:
        return "False"

#-------------------------------------------------------

#------------------Producto_vendido---------------------
@app.route('/request/Producto_vendido/<idproducto>/<idventa>', methods=['PUT'])
def req_put_Producto_vendido(idproducto, idventa):
    res_Producto_vendido = Producto_vendido.query.filter_by(id_Producto=idproducto, id_Venta=idventa).first()
    if request.form is None or res_Producto_vendido is None:
        return "False"
    if 'cantidad' in request.form.keys():
        res_Producto_vendido.cantidad = request.form['cantidad']
    if 'total' in request.form.keys():
        res_Producto_vendido.total = request.form['total']
    #if 'id_Producto' in request.form.keys():
    #    res_Producto_vendido.id_Producto = request.form['id_Producto']
    #if 'id_Venta' in request.form.keys():
    #    res_Producto_vendido.id_Venta = request.form['id_Venta']
    mysql.session.commit()
    return "True"

@app.route('/request/Producto_vendido', methods=['GET'])
def req_get_Producto_vendido():
    all_Producto_vendido = Producto_vendido.query.all()
    result = producto_vendido_schema_multiple.dump(all_Producto_vendido)
    return jsonify(result)

@app.route('/request/Producto_vendido/<idproducto>/<idventa>', methods=['GET'])
def req_get_Producto_vendido_select(idproducto, idventa):
    res_Producto_vendido = Producto_vendido.query.get((idproducto, idventa))
    return producto_vendido_schema_single.jsonify(res_Producto_vendido)

@app.route('/request/Producto_vendido', methods=['POST'])
def req_post_Producto_vendido():
    try:
        cantidad = request.form['cantidad']
        total = request.form['total']
        id_Producto = request.form['id_Producto']
        id_Venta = request.form['id_Venta']
        new_Producto_vendido = Producto_vendido(cantidad, total, id_Producto, id_Venta)
        mysql.session.add(new_Producto_vendido)
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

#----------------Producto_devuelto-------------
@app.route('/request/producto_Devolver/<number>', methods=['PUT'])
def req_put_producto_Devolver(number):
    res_producto_Devolver = Producto_devuelto.query.filter_by(ID=number).first()
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
    all_producto_Devolver = Producto_devuelto.query.all()
    result = producto_devuelto_schema_multiple.dump(all_producto_Devolver)
    return jsonify(result)

@app.route('/request/producto_Devolver/<number>', methods=['GET'])
def req_get_producto_Devolver_select(number):
    res_producto_Devolver = Producto_devuelto.query.get(number)
    return producto_devuelto_schema_single.jsonify(res_producto_Devolver)

@app.route('/request/producto_Devolver', methods=['POST'])
def req_post_producto_Devolver():
    try:
        descripcion = request.form['descripcion']
        id_Garantia = request.form['id_Garantia']
        id_Producto = request.form['id_Producto']
        new_producto_Devolver = Producto_devuelto(descripcion, id_Garantia, id_Producto)
        mysql.session.add(new_producto_Devolver)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#-------------------------------------------------------

#-------------------Inventario------------------
@app.route('/request/inventario/<id_Sucursal>/<id_Producto>', methods=['PUT'])
def req_put_invetario(id_Sucursal, id_Producto):
    res_inventario = Inventario.query.filter_by(id_Sucursal = id_Sucursal, id_Producto = id_Producto).first()
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
    res_permiso_Asignado = Permiso_asignado.query.filter_by(id_Permiso=idpermiso, id_Cuenta=idcuenta).first()
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
    all_permiso_Asignado = Permiso_asignado.query.all()
    result = permiso_asignado_schema_multiple.dump(all_permiso_Asignado)
    return jsonify(result)

@app.route('/request/permiso_Asignado/<idpermiso>/<idcuenta>', methods=['GET'])
def req_get_permiso_Asignado_select(idpermiso, idcuenta):
    res_permiso_Asignado = Permiso_asignado.query.get((idpermiso, idcuenta))
    return permiso_asignado_schema_single.jsonify(res_permiso_Asignado)

@app.route('/request/permiso_Asignado', methods=['POST'])
def req_post_permiso_Asignado():
    try:
        estado = request.form['estado']
        id_P = request.form['id_Permiso']
        id_C = request.form['id_Cuenta']
        new_permiso_Asignado = Permiso_asignado(estado, id_P, id_C)
        mysql.session.add(new_permiso_Asignado)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#-------------------Factura--------------------

@app.route('/request/factura/<nro>', methods = ['PUT'])
def req_put_factura(nro):
    res_factura = Factura.query.filter_by(NRO=nro).first()
    if request.form is None or res_factura is None:
        return "False"
    if 'NIT' in request.form.keys():
        res_factura.NIT = request.form['NIT']
    if 'razon_Social' in request.form.keys():
        res_factura.razon_Social = request.form['razon_Social']
    #if 'id_Venta' in request.form.keys():
    #    res_factura.id_Venta = request.form['id_Venta']
    mysql.session.commit()
    return "True"

@app.route('/request/factura', methods=['GET'])
def req_get_factura():
    all_factura = Factura.query.all()
    result = factura_schema_multiple.dump(all_factura)
    return  jsonify(result)

@app.route('/request/factura/<nro>', methods=['GET'])
def req_get_factura_select(nro):
    res_factura  = Factura.query.get(nro)
    return factura_schema_single.jsonify(res_factura)

@app.route('/request/factura', methods=['POST'])
def req_post_factura():
    try:
        NIT = request.form['NIT']
        razon_S = request.form['razon_Social']
        id_V = request.form['id_Venta']
        new_factura = Factura(NIT, razon_S, id_V)
        mysql.session.add(new_factura)
        mysql.session.commit()
        return "True"
    except KeyError:
        return "False"

#----------------------------------------------

#----------------------------------------------