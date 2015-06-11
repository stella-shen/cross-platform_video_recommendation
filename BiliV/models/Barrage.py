from BiliV.foundation import db

class Barrage(db.Model):
	__tablename__ = "barrage"
	  
	id = db.Column(db.Integer, primary_key=True)
	avid = db.Column(db.Integer, db.ForeignKey('video.id'), nullable = False)
	#fbid = Column(Integer, ForeignKey('bili_user.mid'), nullable = False)
	text = db.Column(db.String(300)) # according to wikipedia
	second = db.Column(db.Float)
	mode = db.Column(db.Integer)
	font_size = db.Column(db.Float)
	color = db.Column(db.Integer)
	timestamp = db.Column(db.Integer)
	pool = db.Column(db.Integer)
	owner = db.Column(db.String(30), nullable = False)
	rowid = db.Column(db.Integer)

