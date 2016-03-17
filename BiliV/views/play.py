#! encoding=utf-8
from flask import Blueprint, render_template, redirect, request, url_for, g
from BiliV.foundation import Base, db_session
from flask.ext.login import login_required
from BiliV.controller import video
from BiliV.models import Video, WeiboUser
from BiliV import const

play = Blueprint('play', __name__, template_folder = 'templates')

@play.route('/', methods = ['GET', 'POST'])
@login_required
def index():
	aid = request.args.get('aid')
	play_video = Video.query.filter_by(id = aid).first()
	if play_video is None:
		return render_template('frontend/error.html')
	recommend_videos = video.show_video_data(6, u'')
	return render_template('play/play.html', video = play_video, recommend_videos=recommend_videos)

@play.route('/collect_video', methods = ['GET', 'POST'])
@login_required  
def collect_video():
	#return 'collect video'
	aid = request.args.get('aid')
	user = g.user
	video = Video.query.filter_by(id = aid).first()
	user.like_videos.append(video)
	#db.session.add(current_collect)
	db_session.commit()
	return redirect(url_for('.index', aid = aid))

