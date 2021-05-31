from controller.session import *

def page_404():
    return render_template("404.html"), 404

def login(message):
    return render_template("login.html", err_message = message)

def home():
    global sess_global
    nomInfo = sess_global['nombre'].capitalize() + ' ' + sess_global['ap_Paterno'].capitalize() + ' ' + sess_global['ap_Materno'].capitalize()
    url_Photo = sess_global['url_Photo']
    return render_template('home.html', sess_nomInfo = nomInfo, url_picture = url_Photo)

def profile(ret_message):
    global sess_global
    inf_name = str(sess_global['nombre'].capitalize())
    inf_fLast = str(sess_global['ap_Paterno'].capitalize())
    inf_mLast = str(sess_global['ap_Materno'].capitalize())
    info_data = sess_global['ac_infoPer']
    inf_pNumber = str(info_data[1])
    inf_email = str(info_data[2])
    inf_sex = str(info_data[0])
    if inf_sex == 'H':
        inf_sex = 'Hombre'
    elif inf_sex == 'M':
        inf_sex = 'Mujer'
    info_bDate = str(info_data[3])
    
    return render_template('profile.html', name = inf_name, fLast = inf_fLast, mLast = inf_mLast, pNumber = inf_pNumber, email = inf_email, sex = inf_sex, bDate = info_bDate, errMessage = ret_message)

def new_Client():
    return render_template('restricted/new_Client.html')

def register_Sales():
    return render_template('restricted/register_Sales.html')

def show_Sales():
    return render_template('restricted/show_Sales.html')

def register_Inventory():
    global sess_global
    idSucursal = sess_global('sucursal_id')
    return render_template('restricted/register_Inventory.html', sucursal_code = idSucursal)

def register_Product():
    get_Brand = getData('data_Brand')
    get_Technician = getData('data_Technician')
    if get_Brand is None:
        data_Brands = Marca.query.distinct().all()
        saveData('data_Brand', data_Brands)
        get_Brand = getData('data_Brand')
    if get_Technician is None:
        data_Technicians = mysql.session.query(Persona.ID, Persona.nombre, Persona.apellido_Paterno, Persona.apellido_Materno, Persona.telefono, Tecnico).filter(Persona.ID == Tecnico.id_Persona, Tecnico.estado == 0).all()
        saveData('data_Technician', data_Technicians)
        get_Technician = getData('data_Technician')
    
    return render_template('restricted/register_Product.html', dataBrand = get_Brand, dataTechnician = get_Technician)