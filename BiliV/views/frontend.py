from flask import Blueprint, render_template, redirect, url_for, flash, request, g, session
from BiliV.foundation import db
from BiliV.models import User, Weibo
from flask.ext.login import login_user, logout_user, login_required
from sqlalchemy.sql import func
from SNS import sina
import json

frontend = Blueprint('frontend', __name__, template_folder = 'templates')

APP_KEY = '2090411654'
APP_SECRET = '64e9b96552114537fc51de682d479d95'
CALLBACK_URL = 'http://bili.thumedia.org:5000/callback'

@frontend.route('/')
def index():
	return render_template('frontend/index.html')

@frontend.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated is True:
		return redirect(url_for('.callback'))
	auth = sina.privateOAuth(APP_KEY, APP_SECRET, CALLBACK_URL)
	authorize_url = auth.get_auth_url()
	return redirect(authorize_url)
	
@frontend.route('/callback', methods = ['GET', 'POST'])
def callback():
	code = request.args.get('code', 0)
	session['code'] = code
	accessOauth = sina.privateOAuth(APP_KEY, APP_SECRET, CALLBACK_URL, code)
	text_json = accessOauth.get_access_token()
	text = json.loads(text_json)
	if text.has_key('access_token'):
		access_token = text["access_token"]
		session['access_token'] = access_token
		remind_in = text['remind_in']
		session['remind_in'] = remind_in
		expires_in = text['expires_in']
		session['expires_in'] = expires_in
		uid = text['uid']
		session['uid'] = uid
	else:
		return render_template('frontend/error.html')
	#get user data
	user_api = sina.privateAPI(access_token, uid)
	data_json = json.loads(user_api.get_user_data())
	current_user = User.query.filter(User.id == uid).first()
	screen_name = data_json['screen_name']
	description = data_json['description']
	gender = data_json['gender']
	img_url = data_json['profile_image_url']
	url = data_json['url']
	followers_cnt = data_json['followers_count']
	friends_cnt = data_json['friends_count']
	statuses_cnt = data_json['statuses_count']
	#update_time = data_json['created_at']
	bi_followers_count = data_json['bi_followers_count']
	if current_user is None:
		user = User(id = uid, screen_name = screen_name, access_token = access_token, description = description, gender = gender, image_url = img_url, url = url, followers_cnt = followers_cnt, friends_cnt = friends_cnt, statuses_cnt = statuses_cnt, bi_followers_count = bi_followers_count)
		db.session.add(user)
	else:
		current_user.screen_name = screen_name
		current_user.access_token = access_token
		current_user.description = description
		current_user.gender = gender
		current_user.image_url = img_url
		current_user.url = url
		current_user.followers_cnt = followers_cnt
		current_user.friends_cnt = friends_cnt
		current_user.statuses_cnt = statuses_cnt
		current_user.bi_followers_count = bi_followers_count
	db.session.commit()
	users = User.query.all()
	print users
	#get weibo data
	count = 200
	weibo_api = sina.privateAPI(access_token, uid, count)
	weibo_json = json.loads(weibo_api.get_weibo_data())
	weibo_set = weibo_json['statuses']
	weibo_list = []
	for weibo in weibo_set:
		w_id = weibo['id']
		text = weibo['text']
		weibo_list.append(text.encode("utf8"))
		source = weibo['source']
		reposts_cnt = weibo['reposts_count']
		comments_cnt = weibo['comments_count']
		w_user = weibo['user']
		w_uid = w_user['id']
		current_weibo = Weibo.query.filter(id == w_id).first()
		if current_weibo is None:
			weibo = Weibo(id = w_id, uid = w_uid, access_token = access_token, count = 200, text = text, source = source, reposts_cnt = reposts_cnt, comments_cnt = comments_cnt)
			db.session.add(weibo)
		else:
			current_weibo.uid = uid
			current_weibo.access_token = access_token
			current_weibo.count = count
			current_weibo.text = text
			current_weibo.source = source
			current_weibo.reposts_cnt = reposts_cnt
			current_weibo.comments_cnt = comments_cnt
		db.session.commit()
	return repr(weibo_list)
	return redirect(url_for(show))

