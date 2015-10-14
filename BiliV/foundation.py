from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.login import LoginManager
from pkgutil import iter_modules
from importlib import import_module
import os, config

engine = create_engine(config.DB_STRING, convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,\
		autoflush=False,\
		bind=engine)\
		)

Base = declarative_base()
Base.query = db_session.query_property()

login_manager = LoginManager()

sina_api = {'BiliV':('2090411654',
					 '64e9b96552114537fc51de682d479d95',
					 'http://bili.thumedia.org/callback'),
			}

def load_all_task():
	for loader, module_name, is_pkg in iter_modules([os.path.dirname(__file__)], __name__ + '.'):
		import_module(module_name)
	global load_all_task
	load_all_task = lambda: None
	return

