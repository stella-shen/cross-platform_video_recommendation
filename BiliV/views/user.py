from flask import Blueprint, render_template, url_for, g
from BiliV.foundation import db
from BiliV.models.User import User
from flask.ext.login import login_required

user = Blueprint('user', __name__)

@user.route()

