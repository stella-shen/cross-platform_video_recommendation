from BiliV.foundation import db_session, Base
from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger, UnicodeText, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy_utils import JSONType

class WeiboVideo(Base):
	__tablename__ = 'weibo_video'
	__table_args__ = {
	  "mysql_engine": 'InnoDB',
	  "mysql_charset": 'utf8mb4'
	}

	id = Column(Integer, primary_key = True)
	platform = Column(String(10))

	title = Column(UnicodeText)
	brief = Column(UnicodeText)

	url = Column(Text)
	other = Column(JSONType)

	seg_info = Column(JSONType)
	state = Column(Integer, default = 0)

