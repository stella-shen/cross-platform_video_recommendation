#! encoding=utf-8
from flask import Blueprint, render_template, request, redirect, url_for, g
from flask.ext.login import login_required
from BiliV.foundation import Base, db_session
from BiliV.models import Video, WeiboUser

account = Blueprint('account', __name__, template_folder = 'templates')

@account.route('/', methods = ['GET', 'POST'])
@login_required
def index():
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
		db_session.commit()
	except:
		pass
	likes = user.like_videos
	return render_template('account/account.html', likes = likes, cute = user.cute, hot = user.hot, liter = user.liter, otaku = user.otaku, wierd = user.wierd, aj = user.aj, fu = user.fu)

@account.route('/edit_interests', methods = ['GET', 'POST'])
@login_required
def edit_interests():
	return render_template('account/waiting.html')

