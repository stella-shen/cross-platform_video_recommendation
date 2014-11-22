from flask import Blueprint, render_template, redirect, url_for, flash, request, g, session
from BiliV.models import User, Weibo
from flask.ext.login import login_user, logout_user, login_required
from SNS import sina

frontend = Blueprint('frontend', __name__, template_folder = 'templates')

APP_KEY = '2090411654'
APP_SECRET = '64e9b96552114537fc51de682d479d95'
CALLBACK_URL = 'http://bili.thumedia.org/callback'

@frontend.route('/')
def index():
	return render_template('frontend/index.html')

@frontend.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated is True:
		return redirect(url_for('.show'))
	
	pOAuth = sina.privateOAuth(APP_KEY, APP_SECRET, CALLBACK_URL)
	print "test"
	authorize_url = pOAuth.get_auth_url()
	path = redirect(authorize_url)
	code = request.args.get('code', 0)
	session['code'] = code
	return path
	
@frontend.route('/callback', methods = ['GET', 'POST'])
def callback():
	code = session['code']
	accessOauth = sina.privateOAuth(APP_KEY, APP_SECRET, CALLBACK_URL, code)
	access_token_url = accessOauth.get_access_token_url()
	redirect(access_token_url)
	access_token = request.args.get('access_token', 0)
	session['access_token'] = access_token
	return render_template('fronted/show.html')

@frontend.route('/show')
def show():
	return 