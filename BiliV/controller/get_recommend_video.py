#!/usr/bin/python
# -*- coding: utf-8 -*-
from BiliV.models import User, Weibo, Video, Barrage
from BiliV.algorithm import recommend
import random

def get_weibo_content(uid):
	res = []
	weibo = Weibo.query.filter_by(uid = uid).all()
	for w in weibo:
		res.append(w.text)
	user = User.query.filter_by(id = uid).first()
	res.append(user.description)
	if user.cute is not None and user.cute > 50:
		res.append(u'萌')
	if user.hot is not None and user.hot > 50:
		res.append(u'燃')
	if user.wierd is not None and user.wierd > 50:
		res.append(u'鬼畜')
	if user.otaku is not None and user.otaku > 50:
		res.append(u'宅')
	if user.liter is not None and user.liter > 50:
		res.append(u'文艺')
	if user.aj is not None and user.aj > 50:
		res.append(u'傲娇')
	if user.fu is not None and user.fu > 50:
		res.append(u'腐')
	#print res
	return res

def get_video_content():
	videos = Video.query.all()
	return videos

def get_recommend_video_by_str_match(uid):
	weibo = get_weibo_content(uid)
	#print weibo
	video = get_video_content()
	res = recommend.recommend_by_str_match(video, weibo)
	return res[ : 9]

def get_recommend_video_by_tfidf(uid):
	weibo = get_weibo_content(uid)
	video = get_video_content()
	res = recommend.recommend_by_tfidf(video, weibo)
	return random.sample(res, 9)

