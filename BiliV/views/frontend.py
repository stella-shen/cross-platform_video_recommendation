#! encoding=utf-8
from flask import Blueprint, render_template, redirect, request, url_for, g
from sqlalchemy import desc
from BiliV.foundation import Base, db_session
from BiliV.models import Video, WeiboUser, RecommendRelation
from BiliV.algorithm import algorithm
from BiliV.controller import video, get_recommend_video, get_weibo, friends
from flask.ext.login import login_user, logout_user, login_required
from BiliV import const
from SNS import sina
import arrow, random
import os

frontend = Blueprint('frontend', __name__, template_folder = 'templates')

@frontend.route('/', methods=['GET', 'POST'])
@login_required
def index():
	#get_weibo.get_weibo_data(g.user.access_token, g.user.id)
	#friends.get_friends_data(g.user.access_token, g.user.id)
	#user = WeiboUser.query.filter_by(id=g.user.id).first()
	video_type = request.args['type']
	common_videos = list()
	if video_type=='rand':
		all_videos = Video.query.all()
		common_videos = common_videos + random.sample(all_videos, 30)
	elif video_type=='visitsort':
		common_list = RecommendRelation.query.filter_by(weibo_user_id = g.user.id).filter_by(algorithm = 'VisitSort').all()
		for cl in common_list:
			v = Video.query.filter_by(id = cl.bili_video_id).first()
			common_videos.append(v)
	elif video_type=='tfidf':
		common_list = RecommendRelation.query.filter_by(weibo_user_id = g.user.id).filter_by(algorithm = 'docmatching').all()
		for cl in common_list:
			v = Video.query.filter_by(id = cl.bili_video_id).first()
			common_videos.append(v)
	elif video_type == 'lda':
		common_list = RecommendRelation.query.filter_by(weibo_user_id = g.user.id).filter_by(algorithm = 'ldamatching').all()
		for cl in common_list:
			v = Video.query.filter_by(id = cl.bili_video_id).first()
			common_videos.append(v)
	elif video_type=='wierd':
		common_videos = video.show_video_data(10, u'鬼畜')
	important_videos = list()
	if len(common_videos) != 0:
		important_videos = common_videos[:10]
		important_videos = random.sample(important_videos, 2)
		for v in important_videos:
			common_videos.remove(v)
	#common_videos = random.sample(common_videos, 8)
	return render_template('frontend/index.html', important_videos = important_videos, common_videos = common_videos)

@frontend.route('/login')
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('.index', type='all'))
	auth = sina.WeiboOAuth(const.APP_KEY, const.APP_SECRET)
	authorize_url = auth.get_auth_url(const.CALLBACK_URL)
	videos_list = RecommendRelation.query.filter_by(algorithm='VisitSort').all()
	videos = list()
	for v in videos_list:
		video = Video.query.filter_by(id = v.bili_video_id).first()
		if video not in videos:
			videos.append(video)
	videos = random.sample(videos, 8)
	return render_template('frontend/login.html', authorize_url = authorize_url, videos = videos)

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
		#Need to add command
		if need_fetch:
			user.update()
			get_weibo.get_weibo_data(user.access_token, user.id)
			db_session.commit()
		login_user(user)
		return redirect(url_for('.index', type='all'))
	except:
		raise
		db_session.rollback()
		return render_template('frontend/error.html')

@frontend.route('/hot')
def hot():
	auth = sina.WeiboOAuth(const.APP_KEY, const.APP_SECRET)
	authorize_url = auth.get_auth_url(const.CALLBACK_URL)
	videos_list = RecommendRelation.query.filter_by(algorithm='VisitSort').all()
	videos = list()
	for v in videos_list:
		video = Video.query.filter_by(id = v.bili_video_id).first()
		if video not in videos:
			videos.append(video)
	videos = random.sample(videos, 16)
	return render_template('frontend/hot.html', authorize_url = authorize_url, videos = videos)

@frontend.route('/like_post/<video_id>', methods = ['GET', 'POST'])
def like_post(video_id):
	print video_id
	videos = LikeRelation.query.filter_by(video_id = video_id).all()
	like_relation = videos.query.filter_by(weibo_user_id = g.user.id).first()
	if like_relation is None:
		like_relation = LikeRelation(video_id = video_id, weibo_user_id = g.user.id, score = 3)
		db.session.add(like_relation)
		db.session.commit()
	else:
		db.session.delete(like_relation)
		db.session.commit()
