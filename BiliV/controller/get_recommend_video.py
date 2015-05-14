from BiliV.models import Weibo, Video
from BiliV.algorithm import recommend

def get_weibo_content(uid):
	res = ''
	weibo = Weibo.query.filter_by(uid = uid).all()
	cnt = 0
	for w in weibo:
		res = res + ' ' + w.text
		cnt = cnt + 1
		if cnt == 2000:
			break
	return res

def get_video_content():
	videos = Video.query.all()
	return videos

def get_recommend_video(uid):
	weibo = get_weibo_content(uid)
	print weibo
	video = get_video_content()
	res = recommend.recommend_by_str_match(video, weibo)
	return res[ : 9]

