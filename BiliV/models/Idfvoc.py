#! encoding=utf-8

from BiliV.foundation import db_session, Base
from sqlalchemy import Column, Integer, Float, String

class Idfvoc(Base):
	__tablename__ = 'idfvoc'
	__table_args__ = {
			'mysql_engine': 'InnoDB',
			'mysql_charset': 'utf8mb4'
	}
	word = Column(String(20), primary_key = True)
	idf = Column(Float)

