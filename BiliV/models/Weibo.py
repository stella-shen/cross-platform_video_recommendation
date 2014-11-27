from datetime import datetime

from flask import current_app

from BiliV.foundation import db
from BiliV.models import User

class Weibo(db.Model):
	__tablename__ = 'Weibo'
	id = db.Column(db.Integer, primary_key = True)
	uid = db.Column(db.Integer, db.ForeignKey('User.id'))
	access_token = db.Column(db.Text)
	count = db.Column(db.Integer)
	#created_at = db.Column(db.DateTime)
	text = db.Column(db.Text)
	source = db.Column(db.Text)
	reposts_cnt = db.Column(db.Integer)
	comments_cnt = db.Column(db.Integer)

	def __str__(self):
		return self.id

	def __repr__(self):
		return "<Weibo %r>" % self.text
