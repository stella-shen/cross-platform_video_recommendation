from BiliV.foundation import db

class Friends(db.Model):
	__tablename__ = 'friends'
	id = db.Column(db.Integer, primary_key = True)
	uid = db.Column(db.Integer, db.ForeignKey('user.id'))
	screen_name = db.Column(db.String(50))
	description = db.Column(db.String(100))
	profile_url = db.Column(db.String(100))
	gender = db.Column(db.Integer)
	follow_me = db.Column(db.Boolean)
	data_set = db.Column(db.Text)    #all weibo API data

	def __repr__(self):
		return "<Friends: %r>" % self.screen_name

	def __str__(self):
		return self.id

