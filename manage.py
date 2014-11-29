from flask.ext.script import Server, Shell, Manager, prompt_bool
from BiliV import create_app
from BiliV.foundation import db
from BiliV.models import User, Weibo

app_ = create_app()
app_.debug = True
manager = Manager(app_)

manager.add_command("runserver", Server('0.0.0.0', port = 8080))

def _make_context():
	return dict(db = db)
manager.add_command("shell", Shell(make_context = _make_context()))

def _addUser(uid, access_token):
	user = User(id = uid, access_token = access_token)
	db.session.add(user)
	db.session.commit()

@manager.command
def createall():
	db.create_all()
	#_addUser('admin', 'admin')

@manager.command
def dropall():
	if prompt_bool("Are you sure? You will lose all your data!"):
		db.drop_all()

if __name__ == "__main__":
	manager.run()
