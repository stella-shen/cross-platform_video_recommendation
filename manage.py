from flask.ext.script import Server, Shell, Manager, prompt_bool
from BiliV import create_app
from BiliV.foundation import db
from BiliV.models import User, Weibo, Video
from BiliV.controller import video, get_barrage
from BiliV import const 
from SNS.bili import newlist
import logging

app_ = create_app()
app_.debug = True
manager = Manager(app_)

manager.add_command("runserver", Server('0.0.0.0', port = 8081))

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

@manager.command
def fetch_rank_video():
    for i in [1, 3, 7, 30]:
        for t in [const.ALL, const.COMIC, const.SERIES, const.DANCE,\
				const.MUSIC, const.GAME, const.SCIENCE, const.FUN, \
				const.MOVIE, const.WIERD, const.NEW_COMIC]:
            video.get_video_data(i, 100, t)
            if t != const.NEW_COMIC:
                video.get_video_data(i, 100, t, False)
            logging.debug("vide day %d for type %d finished" % (i, t))
@manager.command
def fetch_new_list_video():
	newlist.load()

@manager.command
def fetch_barrage():
	get_barrage.get_barrage()

if __name__ == "__main__":
	manager.run()
