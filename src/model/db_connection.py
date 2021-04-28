from model.init import *
from datetime import datetime
import enum
import json

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/securitypage'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql = SQLAlchemy(app)