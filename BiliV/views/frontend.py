from flask import Blueprint, render_template, redirect, request, url_for, g
from BiliV.foundation import db
from BiliV.models.User import User
from BiliV.models.Video import Video
from BiliV.controller import video, get_weibo, get_recommend_video
from flask.ext.login import login_user, logout_user, login_required
from BiliV import const
from SNS import sina
import arrow

frontend = Blueprint('frontend', __name__, template_folder = 'templates')

@frontend.route('/')
@login_required
def index():
	all_videos = get_recommend_video.get_recommend_video_by_tfidf(g.user.id)
	comic_videos = video.show_video_data(9, const.COMIC)
	series_videos = video.show_video_data(9, const.SERIES)
	return render_template('frontend/index.html', all_videos = all_videos, comic_videos = comic_videos, series_videos = series_videos)

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
		user = User.query.get(uid)
		need_fetch = True
		if user is None:
			user = User(id=uid)
			db.session.add(user)
		else:
			limit = arrow.utcnow().replace(hours=-1)
			if user.last_update and user.last_update > limit:
				need_fetch = False
		user.update_token(tokens)

		if need_fetch:
			user.update()
			get_weibo.get_weibo_data(user.access_token, user.id)	
		db.session.commit()
		login_user(user)
		return redirect(url_for('.index'))
	except:
		raise
		db.session.rollback()
		return render_template('frontend/error.html')

@frontend.route('/account')
@login_required
def account():
	likes = video.get_video_data(1, 9, const.ALL)
	return render_template('frontend/user.html', likes = likes)

@frontend.route('/play', methods = ['GET', 'POST'])
@login_required
def play():
	aid = request.args.get('aid')
	play_video = Video.query.filter_by(id = aid).first()
	if play_video is None:
		return render_template('frontend/error.html')
	recommend_videos = video.get_video_data(7, 5, const.ALL)
	return render_template('frontend/play.html', video = play_video, recommend_videos=recommend_videos)
