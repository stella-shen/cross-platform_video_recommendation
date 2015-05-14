from BiliV.foundation import db
from sqlalchemy_utils import JSONType

class Video(db.Model):
	__tablename__ = 'video'
	id = db.Column(db.Integer, primary_key = True)
	url = db.Column(db.String(100))
	play = db.Column(db.String(10))
	title = db.Column(db.String(100))
	author = db.Column(db.String(100))
	description = db.Column(db.String(100))
	pic = db.Column(db.String(200))
	pts = db.Column(db.String(10))
	type = db.Column(db.String(10))
	detail = db.Column(JSONType)    #all video json data

	def __init__(self, id):
		self.id = id
		self.url = 'http://www.bilibili.com/video/av%d/' % (self.id)

