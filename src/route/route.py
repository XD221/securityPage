from controller.dbController import *

def login():
    return render_template("login.html")

def home():
    return render_template('home.html')

def register_Sales():
    return render_template('restricted/register_Sales.html')

def show_Sales():
    return render_template('restricted/show_Sales.html')