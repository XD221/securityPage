from controller.dbController import *
from hashlib import md5

sess_global = {'login' : False }

def chargeGlobal():
    if 'user_id' not in session.keys():
        session['user_id'] = None
    if 'nombre' not in session.keys():
        session['nombre'] = None
    if 'ap_Paterno' not in session.keys():
        session['ap_Paterno'] = None
    if 'ap_Materno' not in session.keys():
        session['ap_Materno'] = None
    if 'permission' not in session.keys():
        session['permission'] = None
    if 'url_Photo' not in session.keys():
        session['url_Photo'] = None
    if 'sucursal_id' not in session.keys():
        session['sucursal_id'] = None
    result = {}
    for i in session.keys():
        result[i] = session[i]
    return result

def isLogging():
    global sess_global
    sess_global.update(chargeGlobal())
    if sess_global['login']:
        return True
    if session['user_id'] is not None:
        sess_global['login'] = True
        sess_global['user_id'] = session['user_id']
        sess_global['nombre'] = session['nombre']
        sess_global['ap_Paterno'] = session['ap_Paterno']
        sess_global['ap_Materno'] = session['ap_Materno']
        sess_global['url_Photo'] = session['url_Photo']
        sess_global['sucursal_id'] = session['sucursal_id']
        return True
        
    return False

def signIn(username, password):
    if isLogging():
        return 0
    password = md5(password.encode())
    account = Cuenta.query.filter_by(nombre_Cuenta=username, urs_Password=password.hexdigest()).first()
    if account is None:
        return 1
    sess_data = mysql.session.query(Persona, Empleado).filter(Persona.ID == Empleado.id_Persona, Empleado.ID == account.id_Empleado).first()
    if sess_data is None:
        return 2
    session['user_id'] = account.ID
    session['em_id'] = sess_data.Empleado.ID
    session['nombre'] = sess_data.Persona.nombre
    session['ap_Paterno'] = sess_data.Persona.apellido_Paterno
    session['ap_Materno'] = sess_data.Persona.apellido_Materno
    session['url_Photo'] = account.url_Photo
    session['sucursal_id'] = sess_data.Empleado.id_Sucursal
    session['ac_infoPer'] = [sess_data.Persona.sexo, sess_data.Persona.telefono, sess_data.Persona.email, sess_data.Persona.fecha_Nacimiento]
    return 0

def logout():
    global sess_global
    session.clear()
    for i in sess_global.keys():
        if i == 'login':
            sess_global[i] = False
        else:
            sess_global[i] = None
    return

# Get Variable 
#def getPermission():
#    global sess_global
#    if (not sess_global['login']):
#        if len(sess_global['permission']) == 0:
#            permission = Permiso_Asignado.query.filter_by(id_Cuenta = sess_global['user_id'], estado = 0).first()
#            permission = getArrayColumn('id_Permiso', permission)
#        return permission
#    return []

def getArrayColumn(column_name, data):
    result = []
    for row in data:
        m = getattr(row, column_name)
        result.append(m)
    return result
        

def saveData(key, value):
    session[key] = value
    
def getData(key):
    if session.get(key) is not None:
        return session[key]
    return None


#app.config['SESSION_TYPE'] = 'sqlalchemy'
#app.config['SESSION_SQLALCHEMY'] = mysql
#app.config['SESSION_SQLALCHEMY_TABLE'] = 'signin_session'
#app.config['SESSION_PERMANENT'] = True
#app.config['SESSION_USE_SIGNER'] = False
#app.config['SESSION_KEY_PREFIX'] = 'signIn:'

app.secret_key = '5764dfd073b08e87902d0c16e564b027'
app.config['SESSION_TYPE'] = 'filesystem'
sess = Session()
sess.init_app(app)