from model.init import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://silva:silva123@zapateriazan.ga/diego'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql = SQLAlchemy(app)
mysql.session.autoflush = True