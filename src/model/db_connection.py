from model.init import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/securitypage'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql = SQLAlchemy(app)
mysql.session.autoflush = True