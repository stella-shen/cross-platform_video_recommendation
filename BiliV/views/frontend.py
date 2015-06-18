from flask import Blueprint, render_template, redirect, request, url_for, g
from BiliV.foundation import db
from BiliV.models.User import User
from BiliV.models.Video import Video
from BiliV.models.LikeRelationship import like_relationship
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
	dance_videos = video.show_video_data(9, const.DANCE)
	music_videos = video.show_video_data(9, const.MUSIC)
	movie_videos = video.show_video_data(9, const.MOVIE)
	wierd_videos = video.show_video_data(9, const.WIERD)
	science_videos = video.show_video_data(9, const.SCIENCE)
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

@frontend.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
	user = g.user
	try:
		cute = int(request.args['cute'])
		hot = int(request.args['hot'])
		liter = int(request.args['liter'])
		otaku = int(request.args['otaku'])
		wierd = int(request.args['wierd'])
		aj = int(request.args['aj'])
		fu = int(request.args['fu'])
		user.cute = cute
		user.hot = hot
		user.liter = liter
		user.otaku = otaku
		user.wierd = wierd
		user.aj = aj
		user.fu = fu
		db.session.commit()
	except:
		pass
	likes = user.like_videos
	return render_template('frontend/user.html', likes = likes, cute = user.cute, hot = user.hot, liter = user.liter, otaku = user.otaku, wierd = user.wierd, aj = user.aj, fu = user.fu)

@frontend.route('/play', methods = ['GET', 'POST'])
@login_required
def play():
	aid = request.args.get('aid')
	play_video = Video.query.filter_by(id = aid).first()
	if play_video is None:
		return render_template('frontend/error.html')
	recommend_videos = video.get_video_data(7, 6, const.ALL)
	return render_template('frontend/play.html', video = play_video, recommend_videos=recommend_videos)

@frontend.route('/collect_video', methods = ['GET', 'POST'])
@login_required
def collect_video():
	aid = request.args.get('aid')
	user = g.user
	video = Video.query.filter_by(id = aid).first()
	user.like_videos.append(video)
	#db.session.add(current_collect)
	db.session.commit()
	return redirect(url_for('.play', aid = aid))

@frontend.route('/edit_interests', methods = ['GET', 'POST'])
@login_required
def edit_interests():
	return render_template('frontend/waiting.html')

