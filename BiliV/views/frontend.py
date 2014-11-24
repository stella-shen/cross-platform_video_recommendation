from flask import Blueprint, render_template, redirect, url_for, flash, request, g, session
from BiliV.models import User, Weibo
from flask.ext.login import login_user, logout_user, login_required
from SNS import sina

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
	access_token = accessOauth.get_access_token()
	return access_token

@frontend.route('/access_token', methods = ['POST'])
def access_token():

	return request.data 

@frontend.route('/show')
def show():
	return 
