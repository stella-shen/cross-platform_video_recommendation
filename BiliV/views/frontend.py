from flask import Blueprint, render_template, redirect, url_for, request, g
from BiliV.foundation import db
from BiliV.controller import user, weibo, friends
from flask.ext.login import login_user, logout_user, login_required
from BiliV.const import APP_KEY, APP_SECRET, CALLBACK_URL

frontend = Blueprint('frontend', __name__, template_folder = 'templates')

@frontend.route('/')
def index():
	return render_template('frontend/index.html')

@frontend.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('.index'))
	auth = sina.privateOAuth(APP_KEY, APP_SECRET, CALLBACK_URL)
	authorize_url = auth.get_auth_url()
	return redirect(authorize_url)
	
@frontend.route('/callback', methods = ['GET', 'POST'])
def callback():
	code = request.args.get('code', 0)
	accessOauth = sina.privateOAuth(APP_KEY, APP_SECRET, CALLBACK_URL, code)
	text_json = accessOauth.get_access_token()
	text = json.loads(text_json)
	if text.has_key('access_token'):
		access_token = text["access_token"]
		uid = text['uid']
		user.get_user_data(access_token, uid)
		friends.get_friends_data(access_token, uid)
		weibo.get_weibo_data(access_token, uid, uid)
		weibo.get_weibo_data(access_token, uid, 1690707634)
	else:
		return render_template('frontend/error.html')
	return redirect(url_for('.index'))

