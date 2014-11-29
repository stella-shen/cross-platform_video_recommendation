from flask import current_app

from BiliV.foundation import db
from BiliV.models import User

class Friends(db.Model):
	__tablename__ = 'Friends'
	id = db.Column(db.Integer, primary_key = True)
	uid = db.Column(db.Integer, db.ForeignKey('User.id'))
	screen_name = db.Column(db.Text)
	description = db.Column(db.Text)
	profile_url = db.Column(db.Text)
	gender = db.Column(db.String(1))
	follow_me = db.Column(db.Boolean)
	data_set = db.Column(db.Text)

	def __repr__(self):
		return "<Friends: %r>" % self.screen_name

	def __str__(self):
		return self.id

