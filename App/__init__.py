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

#initializing CORS
cors = CORS(app)

#initializing mail service
mail = Mail(app)

#importing views
from App import DailyReport, Email, Factory, Field, Upload, TestField

def get_app():
	return app
