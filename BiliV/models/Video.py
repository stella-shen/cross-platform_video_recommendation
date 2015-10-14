#! encoding=utf-8

from BiliV.foundation import db_session, Base
from sqlalchemy import Column, Integer, ForeignKey, String, Text, Float, LargeBinary, DateTime
from sqlalchemy.dialects.mysql import TINYINT

class Video(Base):
	__tablename__ = "bilibili_video_info"

	id = Column(Integer, primary_key = True)
	url = Column(String(100))
	play = Column(Integer)
	date = Column(DateTime)
	title = Column(String(100))
	author = Column(String(100))
	description = Column(Text)
	pic = Column(String(100))
	pts = Column(String(10))
	videotype = Column(String(10))
	detail = Column(Text)
	isempty = Column(String(24))
	hasempty = Column(String(1))
	isnew = Column(String(1))
	flushtime = Column(DateTime)

