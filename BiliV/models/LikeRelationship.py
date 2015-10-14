'''from BiliV.foundation import db

like_relationship = db.Table('like_relationship',\
		db.Column('video_id', db.Integer, db.ForeignKey('video.id')),\
		db.Column('user_id', db.Integer, db.ForeignKey('user.id'))\
		)
'''
