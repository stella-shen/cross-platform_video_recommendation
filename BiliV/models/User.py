from BiliV import const
from BiliV.foundation import db
from sqlalchemy_utils import ArrowType, JSONType
from SNS import sina
from flask.ext.login import UserMixin
import arrow
from LikeRelationship import *

def analyze_gender(gender):
	m = {
		"m": const.GENDER_MALE,
		"f": const.GENDER_FEMALE,
	}
	return m.get(gender, const.GENDER_NONE)

class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key = True)

	access_token = db.Column(db.String(100))
	expire_date = db.Column(ArrowType)

	last_update = db.Column(ArrowType)

	screen_name = db.Column(db.String(50))
	description = db.Column(db.String(100))
	gender = db.Column(db.Integer)
	image_url = db.Column(db.String(100))
	followers_cnt = db.Column(db.Integer)
	friends_cnt = db.Column(db.Integer)
	statuses_cnt = db.Column(db.Integer)
	bi_followers_count = db.Column(db.Integer)

	detail = db.Column(JSONType)    #all weibo json data
	weibo = db.relationship('Weibo', backref = 'user', lazy = 'dynamic')
	friends = db.relationship('Friends', backref = 'user', lazy = 'dynamic')
	like_videos = db.relationship('Video', secondary=like_relationship, backref=db.backref('users', lazy='dynamic'))

	def __repr__(self):
		return "<User %r>" % self.screen_name

	def update_token(self, data):
		"""Store access token and expire date returning by WeiboAPI"""
		self.access_token = data['access_token']
		date = arrow.Arrow.fromtimestamp(data['expires_in'])
		self.expire_date = date
		return

	def update(self):
		api = sina.WeiboAPI(self.access_token, self.id)

		data = api.get_user_data()

		self.screen_name = data['screen_name']
		self.description = data['description']
		self.gender = analyze_gender(data['gender'])
		self.image_url = data['profile_image_url']
		self.followers_cnt = data['followers_count']
		self.friends_cnt = data['friends_count']
		self.statuses_cnt = data['statuses_count']
		self.bi_followers_count = data['bi_followers_count']

		self.detail = data
		self.last_update = arrow.utcnow()
