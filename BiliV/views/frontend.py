from flask import Blueprint, render_template, redirect, url_for, flash, request, g, session
from BiliV.foundation import db
from BiliV.models import User, Weibo, Friends
from BiliV.controller import user, weibo
from flask.ext.login import login_user, logout_user, login_required
from sqlalchemy.sql import func
from BiliV.const import APP_KEY, APP_SECRET, CALLBACK_URL
import json

frontend = Blueprint('frontend', __name__, template_folder = 'templates')

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

