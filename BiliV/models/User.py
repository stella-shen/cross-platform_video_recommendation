from datetime import datetime

from flask import current_app

#from flask.ext.sqlalchemy import BaseQuery
#from flask.ext.principal import RoleNeed, UserNeed, Permission

from BiliV.foundation import db
#from BiliV.permissions import admin_permission, auth_permission

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    access_token = db.Column(db.Text)
    screen_name = db.Column(db.Text)
    description = db.Column(db.Text)
    gender = db.Column(db.String(1), default = 'n')
    image_url = db.Column(db.Text)
    url = db.Column(db.Text)
    followers_cnt = db.Column(db.Integer)
    friends_cnt = db.Column(db.Integer)
    statuses_cnt = db.Column(db.Integer)
    update_time = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def __str__(self):
    	return self.id

    def __repr__(self):
    	return "<%s>" % self