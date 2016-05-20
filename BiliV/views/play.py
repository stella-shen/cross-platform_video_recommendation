#! encoding=utf-8
from flask import Blueprint, render_template, redirect, request, url_for, g
from BiliV.foundation import Base, db_session
from flask.ext.login import login_required
from BiliV.controller import video
from BiliV.models import Video, WeiboUser, LikeRelation
from BiliV import const

play = Blueprint('play', __name__, template_folder = 'template')

@play.route('/', methods = ['GET', 'POST'])
def index():
	aid = request.args.get('aid')
	play_video = Video.query.filter_by(id = aid).first()
	if play_video is None:
		return render_template('frontend/error.html')
	cur_play = LikeRelation.query.filter_by(weibo_user_id = g.user.id).filter_by(video_id = aid).first()
	if cur_play is None:
		cur_play = LikeRelation(weibo_user_id = g.user.id, video_id = aid)
		db_session.add(cur_play)
	if cur_play.score is None:
		cur_play.score = const.PLAY
	db_session.commit()
	recommend_videos = video.show_video_data(6, u'')
	return render_template('play/play.html', video = play_video, recommend_videos=recommend_videos)

@play.route('/like_video', methods = ['GET', 'POST'])
@login_required  
def like_video():
	aid = request.args.get('aid')
	user = g.user
	video = Video.query.filter_by(id = aid).first()
	cur_play = LikeRelation.query.filter_by(weibo_user_id = g.user.id).filter_by(video_id = aid).first()
	if cur_play is None:
		cur_play = LikeRelation(weibo_user_id = g.user.id, video_id = aid)
		db_session.add(cur_play)
	cur_play.score = const.LIKE
	db_session.commit()
	return redirect(url_for('.index', aid = aid))

@play.route('/dislike_video', methods = ['GET', 'POST'])
@login_required  
def dislike_video():
	aid = request.args.get('aid')
	user = g.user
	video = Video.query.filter_by(id = aid).first()
	cur_play = LikeRelation.query.filter_by(weibo_user_id = g.user.id).filter_by(video_id = aid).first()
	if cur_play is None:
		cur_play = LikeRelation(weibo_user_id = g.user.id, video_id = aid)
		db_session.add(cur_play)
	cur_play.score = const.DISLIKE
	db_session.commit()
	return redirect(url_for('.index', aid = aid))

