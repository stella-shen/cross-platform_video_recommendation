from BiliV import const
from BiliV.foundation import db_session, Base
from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger, ForeignKey, UnicodeText, Unicode
from sqlalchemy.orm import relationship
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

class WeiboUser(Base, UserMixin):
	__tablename__ = 'biliv_weibo_user'
	__table_args__ = {
		"mysql_engine": "InnoDB",
		"mysql_charset": "utf8mb4"
	}
	id = Column(BigInteger, primary_key = True)

	access_token = Column(String(100))
	expire_date = Column(ArrowType)

	last_update = Column(ArrowType)

	screen_name = Column(Unicode(50))
	description = Column(Unicode(100))
	gender = Column(Integer)
	image_url = Column(String(100))
	followers_cnt = Column(Integer)
	friends_cnt = Column(Integer)
	statuses_cnt = Column(Integer)
	bi_followers_cnt = Column(Integer)
	cute = Column(Integer)
	hot = Column(Integer)
	liter = Column(Integer)
	wierd = Column(Integer)
	aj = Column(Integer)
	otaku = Column(Integer)
	fu = Column(Integer)
	flag = Column(Integer, default = 0)
	state = Column(Integer, default = 0)
	detail = Column(JSONType)    #all weibo json data
	#like_videos = relationship('Video', secondary=like_relationship, backref=db.backref('users', lazy='dynamic'))

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
		self.bi_followers_cnt = data['bi_followers_count']

		self.detail = data
		self.last_update = arrow.utcnow()

class WeiboRelation(Base):
	__tablename__ = 'biliv_weibo_relation'
	__table_args__ = {
	  "mysql_engine": 'InnoDB',
	  "mysql_charset": 'utf8mb4'
	}
	id = Column(Integer, primary_key = True)
	source = Column(BigInteger, ForeignKey('biliv_weibo_user.id'))
	dest = Column(BigInteger, ForeignKey('biliv_weibo_user.id'))

	source_user = relationship(WeiboUser, primaryjoin = source == WeiboUser.id)
	dest_user = relationship(WeiboUser, primaryjoin = dest == WeiboUser.id)
