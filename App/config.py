import os

#creating base directory
basedir = os.path.abspath(os.path.dirname(__file__))


#cross origin response certificate configuration
CORS_HEADERS = 'Content-Type'

#SQL DB configuratiosn
MYSQL_HOST = "aa3uwdk1bwspg2.cmagocj6ky2v.ap-south-1.rds.amazonaws.com"
MYSQL_USER = "root"
MYSQL_PASSWORD = 'glenburnmis'
MYSQL_DB = "ebdb"
#MYSQL_HOST = "localhost"
#MYSQL_User = "root"
#MYSQL_Password = "Supernova723!"
#MYSQL_DB = "WokDB"


#mail sending configuration
MAIL_SERVER ='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'glenburnfinetea@gmail.com'
MAIL_PASSWORD = 'glenburn1'
MAIL_USE_TLS = False
MAIL_USE_SSL = True

