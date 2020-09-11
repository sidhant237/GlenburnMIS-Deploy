from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_mail import Mail

#initializing app
app = Flask(__name__)

#importing configurations
app.config.from_pyfile('config.py')

#initializing db
mysql = MySQL(app)
#app.config['MYSQL_HOST'] = "localhost"
#app.config['MYSQL_USER'] = "root"
#app.config['MYSQL_PASSWORD'] = 'Supernova723!'
#app.config['MYSQL_DB'] = "newschema"

#initializing CORS
cors = CORS(app)

#initializing mail service
mail = Mail(app)

#importing views
from App import DailyReport, Email, Factory, Field, Upload, TestField

def get_app():
	return app
