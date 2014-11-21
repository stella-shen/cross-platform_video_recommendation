from flask import Flask, g, session, request, flash, redirect, json, url_for, render_template

from flask.ext.login import current_user

from BiliV import views
from BiliV.foundation import db, login_manager
from BiliV.models import User, Weibo

DEFAULT_APP_NAME = 'BiliV'

DEFAULT_MODULES = [
	views.frontend, 
	#views.auth,
]

def create_app():
	app = Flask(DEFAULT_APP_NAME)
	app.config.from_object('config')
	configure_foundations(app)
	configure_blueprint(app, DEFAULT_MODULES)
	configure_template_filter(app)
	return app

def configure_foundations(app):
	db.app = app
	db.init_app(app)
	@app.after_request
	def releaseDB(response):
		db.session.close()
		return response
	login_manager.init_app(app)
	login_manager.login_view = 'auth'
	@login_manager.user_loader
	def load_user(id):
		try:
			return User.query.get(int(id))
		except Exception:
			return None
	@app.before_request
	def before_request():
		g.user = current_user
		print g.user
		if g.user != None and g.user.is_authenticated():
			g.user.update_time = datetime.utcnow()
			db.session.add(g.user)
			db.session.commit()

def configure_blueprint(app, modules):
	for module in modules:
		app.register_blueprint(module)

def configure_template_filter(app):
	@app.template_filter('dateint')
	def _jinja2_filter_dateint(dateint):
		return date.fromordinal(dateint).strftime('%Y-%m-%d')

