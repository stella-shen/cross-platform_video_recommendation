#! encoding=utf-8
from flask import Blueprint, render_template, request, redirect, url_for, g
from flask.ext.login import login_required
from BiliV.foundation import Base, db_session
from BiliV.models import Video, WeiboUser, LikeRelation, Idfvoc
import BiliV.redisconfig as rc
import redis as redis_connect
import BiliV.const

account = Blueprint('account', __name__, template_folder = 'template')

@account.route('/', methods = ['GET', 'POST'])
@login_required
def index():
	user = g.user
	like_list = LikeRelation.query.filter_by(weibo_user_id = g.user.id).filter_by(score = 3).all()
	likes = list()
	for l in like_list:
		v = Video.query.filter_by(id = l.video_id).first()
		likes.append(v)
	r = redis_connect.Redis(host = rc.DATA_REDIS_HOST, port = rc.DATA_REDIS_PORT, db = rc.DATA_USER_SPARSE_TFIDF_DB)
	key_tuples = r.lrange(g.user.id, 0, 10)
	words = Idfvoc.query.all()
	key_words = dict()
	for tp in key_tuples:
		tp = tp[1 : -1]
		tp_list = tp.split(',')
		word_num = int(tp_list[0].strip()) 
		weight = float(tp_list[1].strip())
		word = words[word_num].word
		key_words[word] = weight
		print "here"
		print key_words
	return render_template('account/account.html', key_words = key_words, likes = likes)

@account.route('/edit_interests', methods = ['GET', 'POST'])
@login_required
def edit_interests():
	return render_template('account/waiting.html')

