from datetime import datetime
from BiliV.foundation import db

class Weibo(db.Model):
	__tablename__ = 'weibo'
	id = db.Column(db.Integer, primary_key = True)
	uid = db.Column(db.Integer, db.ForeignKey('user.id'))
	created_at = db.Column(db.DateTime)
	text = db.Column(db.String(300))
	source = db.Column(db.String(200))
	reposts_cnt = db.Column(db.Integer)
	comments_cnt = db.Column(db.Integer)
	data_set = db.Column(db.Text)    #all weibo API data

	def __str__(self):
		return self.id

	def __repr__(self):
		return "<Weibo %r>" % self.text
