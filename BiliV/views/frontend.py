#! encoding=utf-8
from flask import Blueprint, render_template, redirect, request, url_for, g
from BiliV.foundation import Base, db_session
from BiliV.models import Video, WeiboUser
#from BiliV.models.LikeRelationship import like_relationship
from BiliV.algorithm import algorithm
from BiliV.controller import video, get_recommend_video, get_weibo, friends
from flask.ext.login import login_user, logout_user, login_required
from BiliV import const
from SNS import sina
import arrow, random

frontend = Blueprint('frontend', __name__, template_folder = 'templates')

@frontend.route('/')
@login_required
def index():
	get_recommend_video.store_recommend_video(g.user.id, 20, 'VisitSort')
	get_weibo.get_weibo_data(g.user.access_token, g.user.id)
	friends.get_friends_data(g.user.access_token, g.user.id)
	user = WeiboUser.query.filter_by(id=g.user.id).first()
	all_recommend = user.biliv_recommend_videos
	all_videos = random.sample(all_recommend, 9)
	comic_videos = video.show_video_data(9, u'动漫')
	series_videos = video.show_video_data(9, u'电视剧')
	dance_videos = video.show_video_data(9, u'舞蹈')
	music_videos = video.show_video_data(9, u'音乐')
	movie_videos = video.show_video_data(9, u'电影')
	wierd_videos = video.show_video_data(9, u'鬼畜')
	science_videos = video.show_video_data(9, u'科普')
	print url_for('account.index')
	return render_template('frontend/index.html', all_videos = all_videos, comic_videos = comic_videos, series_videos = series_videos, dance_videos = dance_videos, music_videos = music_videos, movie_videos = movie_videos, wierd_videos = wierd_videos, science_videos = science_videos)

@frontend.route('/login',)
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('.index'))
	auth = sina.WeiboOAuth(const.APP_KEY, const.APP_SECRET)
	authorize_url = auth.get_auth_url(const.CALLBACK_URL)
	return render_template('frontend/login.html', authorize_url = authorize_url)

@frontend.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('.login'))

@frontend.route('/callback', methods = ['GET', 'POST'])
def callback():
	try:
		code = request.args['code']
		api = sina.WeiboOAuth(const.APP_KEY, const.APP_SECRET)

		tokens = api.exchange_access_token(const.CALLBACK_URL, code)

		# assumpt uid in tokens...
		uid = int(tokens['uid'])
		user = WeiboUser.query.get(uid)
		#return user.id
		need_fetch = True
		if user is None:
			user = WeiboUser(id=uid)
			db_session.add(user)
		else:
			limit = arrow.utcnow().replace(hours=-1)
			if user.last_update and user.last_update > limit:
				need_fetch = False
		user.update_token(tokens)
		get_recommend_video.store_recommend_video(user.id, 20, 'VisitSort')

		if need_fetch:
			user.update()
			get_weibo.get_weibo_data(user.access_token, user.id)
			db_session.commit()
		login_user(user)
		return redirect(url_for('.index'))
	except:
		raise
		db_session.rollback()
		return render_template('frontend/error.html')

