from BiliV.models import Weibo, Video, Barrage
from BiliV.algorithm import recommend
import random

def get_weibo_content(uid):
	res = []
	weibo = Weibo.query.filter_by(uid = uid).all()
	for w in weibo:
		res.append(w.text)
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

