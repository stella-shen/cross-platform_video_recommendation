from BiliV.foundation import db

class Barrage(db):
	__tablename__ = "bili_barrage"
	  
	lv = Column(Integer, primary_key = True)
	avid = Column(Integer, ForeignKey('video.id'), nullable = False)
	#fbid = Column(Integer, ForeignKey('bili_user.mid'), nullable = False)
	text = Column(String(300)) # according to wikipedia
	second = Column(Float)
	mode = Column(Integer)
	font_size = Column(Float)
	color = Column(Integer)
	timestamp = Column(Integer)
	pool = Column(Integer)
	owner = Column(String(30), nullable = False)
	rowid = Column(Integer, primary_key = True)
