from flask import Flask

app = Flask(__name__, static_folder='model/static', template_folder='view')