from flask.ext.sqlalchemy import sqlalchemy
from flask.ext.login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

sina_api = {'BiliV':('2090411654',
					 '64e9b96552114537fc51de682d479d95',
					 'http://bili.thumedia.org/callback'),
			}
