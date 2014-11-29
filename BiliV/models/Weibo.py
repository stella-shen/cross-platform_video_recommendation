from datetime import datetime

from flask import current_app

from BiliV.foundation import db
from BiliV.models import User

class Weibo(db.Model):
	__tablename__ = 'Weibo'
	id = db.Column(db.Integer, primary_key = True)
	uid = db.Column(db.Integer, db.ForeignKey('User.id'))
	created_at = db.Column(db.Text)
	text = db.Column(db.Text)
	source = db.Column(db.Text)
	reposts_cnt = db.Column(db.Integer)
	comments_cnt = db.Column(db.Integer)
	data_set = db.Column(db.Text)

	def __str__(self):
		return self.id

	def __repr__(self):
		return "<Weibo %r>" % self.text
