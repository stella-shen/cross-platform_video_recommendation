from flask import Blueprint, render_template, redirect, url_for, flash, request, g, session
from BiliV.foundation import db
from BiliV.models import User, Weibo, Friends
from flask.ext.login import login_user, logout_user, login_required
from sqlalchemy.sql import func
from SNS import sina
import json

frontend = Blueprint('frontend', __name__, template_folder = 'templates')

APP_KEY = '4159940778'
APP_SECRET = '8ecb3fbdd7d22c38539041e0f459890b'
CALLBACK_URL = 'http://bili.thumedia.org:8080/callback'

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
	weibo_list = get_current_user_data(access_token, uid)
	other_weibo_list = get_id_data(access_token, uid, 1690707634)
	return other_weibo_list
	return redirect(url_for(show))

def get_current_user_data(access_token, uid):
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
	user_data_set = str(data_json)
	if current_user is None:
		user = User(id = uid, screen_name = screen_name, access_token = access_token, description = description, gender = gender, image_url = img_url, url = url, followers_cnt = followers_cnt, friends_cnt = friends_cnt, statuses_cnt = statuses_cnt, bi_followers_count = bi_followers_count, data_set = user_data_set)
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
		current_user.data_set = user_data_set
	db.session.commit()
	users = User.query.all()
	print users
	#get friends list
	friends_api = sina.privateAPI(access_token, uid)
	friends_json = json.loads(friends_api.get_friends_list())
	friends_set = friends_json['users']
	for friend in friends_set:
		f_id = friend['id']
		f_uid = uid
		f_screen_name = friend['screen_name']
		f_description = friend['description']
		f_profile_url = friend['profile_url']
		f_gender = friend['gender']
		f_follow_me = friend['follow_me']
		current_friend = Friends.query.filter(Friends.id == f_id).first()
		if current_friend is None:
			friend = Friends(id = f_id, uid = f_uid, screen_name = f_screen_name, description = f_description, profile_url = f_profile_url, gender = f_gender, follow_me = f_follow_me, data_set = str(friend))
			db.session.add(friend)
		else:
			current_friend.id = f_id
			current_friend.uid = f_uid
			current_friend.screen_name = f_screen_name
			current_friend.description = f_description
			current_friend.profile_url = f_profile_url
			current_friend.gender = f_gender
			current_friend.follow_me = f_follow_me
			current_friend.data_set = str(friend)
		db.session.commit()
	#get weibo data
	weibo_api = sina.privateAPI(access_token, uid)
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
		w_uid = uid
		created_at = weibo['created_at']
		weibo = str(weibo)
		current_weibo = Weibo.query.filter(Weibo.id == w_id).first()
		if current_weibo is None:
			weibo = Weibo(id = w_id, uid = w_uid, created_at = created_at, text = text, source = source, reposts_cnt = reposts_cnt, comments_cnt = comments_cnt, data_set = weibo)
			db.session.add(weibo)
		else:
			current_weibo.uid = uid
			current_weibo.created_at = created_at
			current_weibo.text = text
			current_weibo.source = source
			current_weibo.reposts_cnt = reposts_cnt
			current_weibo.comments_cnt = comments_cnt
			current_weibo.data_set = weibo
		db.session.commit()
		return repr(weibo_list)

def get_id_data(access_token, uid, other_id):
	#get weibo data
	weibo_api = sina.privateAPI(access_token, uid)
	weibo_json = json.loads(weibo_api.get_other_weibo_data(other_id))
	return repr(weibo_json)
	weibo_set = weibo_json['statuses']
	weibo_list = []
	for weibo in weibo_set:
		w_id = weibo['id']
		text = weibo['text']
		weibo_list.append(text.encode("utf8"))
		source = weibo['source']
		reposts_cnt = weibo['reposts_count']
		comments_cnt = weibo['comments_count']
		w_uid = other_id
		created_at = weibo['created_at']
		weibo = str(weibo)
		current_weibo = Weibo.query.filter(Weibo.id == w_id).first()
		if current_weibo is None:
			weibo = Weibo(id = w_id, uid = w_uid, created_at = created_at, text = text, source = source, reposts_cnt = reposts_cnt, comments_cnt = comments_cnt, data_set = weibo)
			db.session.add(weibo)
		else:
			current_weibo.uid = uid
			current_weibo.created_at = created_at
			current_weibo.text = text
			current_weibo.source = source
			current_weibo.reposts_cnt = reposts_cnt
			current_weibo.comments_cnt = comments_cnt
			current_weibo.data_set = weibo
		db.session.commit()
		return repr(weibo_list)


