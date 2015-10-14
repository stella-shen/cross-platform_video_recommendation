from datetime import datetime
from BiliV.foundation import db_session, Base
from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger, UnicodeText, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy_utils import JSONType
from WeiboVideo import WeiboVideo
from WeiboUser import WeiboUser

class WeiboTweet(Base):
	__tablename__ = 'biliv_weibo_tweet'
	__table_args__ = {
	  "mysql_engine": 'InnoDB',
	  "mysql_charset": 'utf8mb4'
	}
	id = Column(BigInteger, primary_key = True)
	uid = Column(BigInteger, ForeignKey('biliv_weibo_user.id'))
	created_at = Column(DateTime)
	utc = Column(String(10))
	text = Column(UnicodeText)
	source = Column(String(50))
	reposts_cnt = Column(Integer)
	comments_cnt = Column(Integer)
	data_set = Column(JSONType)    #all weibo API data

	flag = Column(Integer, default = 0)
	state = Column(Integer, default = 0)

	root_id = Column(BigInteger, default = 0)
	images = Column(Text, default='[]')
	video_id = Column(Integer, ForeignKey('weibo_video.id'))
	video = relationship(WeiboVideo, primaryjoin = video_id == WeiboVideo.id)
	user = relationship(WeiboUser, primaryjoin = uid == WeiboUser.id)

	def __str__(self):
		return self.id

	def __repr__(self):
		return "<Weibo %r>" % self.text
