CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

MYSQL_USER = 'medialab'
MYSQL_PASS = 'medialab'
MYSQL_HOST = 'cluster14'
MYSQL_PORT = '3306'
MYSQL_DB = 'stream'

DB_STRING = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8mb4' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

