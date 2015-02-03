from flask import current_app
from BiliV import const
from BiliV.foundation import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    access_token = db.Column(db.String(100))
    screen_name = db.Column(db.String(50))
    description = db.Column(db.String(100))
    gender = db.Column(db.Integer)
    image_url = db.Column(db.String(100))
    url = db.Column(db.String(100))
    followers_cnt = db.Column(db.Integer)
    friends_cnt = db.Column(db.Integer)
    statuses_cnt = db.Column(db.Integer)
    bi_followers_count = db.Column(db.Integer)
    data_set = db.Column(db.Text)    #all weibo json data
    weibo = db.relationship('Weibo', backref = 'user', lazy = 'dynamic')
    friends = db.relationship('Friends', backref = 'user', lazy = 'dynamic')

    def is_authenticated(self):
        return True
	
    def __str__(self):
        return self.id

    def __repr__(self):
        return "<User %r>" % self.screen_name
