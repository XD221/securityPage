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

def client():
    return render_template('restricted/client.html')

def sales():
    return render_template('restricted/sales.html')

def inventory():
    return render_template('restricted/inventory.html')

def product():
    get_Brand = getData('data_Brand')
    get_Technician = getData('data_Technician')
    get_Category = getData('data_Category')
    get_Count_Brand = getData('data_Count_Brand')
    get_Count_Technician = getData('data_Count_Technician')
    get_Count_Category = getData('data_Count_Category')
    if get_Brand is None or get_Count_Brand is None:
        count_Brands = Marca.query.count()
        data_Brands = Marca.query.filter(Marca.ID >= 0).limit(10).all()
        saveData('data_Brand', data_Brands)
        saveData('data_Count_Brand', count_Brands)
        get_Brand = getData('data_Brand')
        get_Count_Brand = getData('data_Count_Brand')
    if get_Technician is None or get_Count_Technician is None:
        count_Technicians = Tecnico.query.count()
        data_Technicians = mysql.session.query(Persona.ID, Persona.nombre, Persona.apellido_Paterno, Persona.apellido_Materno, Persona.telefono, Tecnico).filter(Cuenta.ID >= 0, Persona.ID == Tecnico.id_Persona, Tecnico.estado == 0).limit(10).all()
        saveData('data_Technician', data_Technicians)
        saveData('data_Count_Technician', count_Technicians)
        get_Technician = getData('data_Technician')
        get_Count_Technician = getData('data_Count_Technician')
    
    if get_Category is None or get_Count_Category is None:
        count_Categories = Categoria.query.count()
        data_Categories = Categoria.query.filter(Categoria.ID >= 0).limit(10).all()
        saveData('data_Category', data_Categories)
        saveData('data_Count_Category', count_Categories)
        get_Category = getData('data_Category')
        get_Count_Category = getData('data_Count_Category')
        
    
    return render_template('restricted/product.html', dataBrand = get_Brand, dataTechnician = get_Technician, dataCategory = get_Category, count_Brand = get_Count_Brand, count_Technician = get_Count_Technician, count_Category = get_Count_Category)