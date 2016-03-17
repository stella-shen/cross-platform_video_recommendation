from SNS import bili
from BiliV.foundation import db_session, Base
from BiliV.models import Video
import json
import random

def get_video_data(day, num, type, all_site = True):
	bili_api = bili.BiliAPI(day, type, all_site)
	video_set = bili_api.fetch()
	#video_set = video_json['list']
	video_list = []
	cnt = 0
	for video in video_set:
		#print video
		aid = int(video['aid'])
		#print aid
		current_video = Video.query.filter_by(id = aid).first()
		if current_video is None:
			current_video = Video(id = aid)
			db_session.add(current_video)
		current_video.play = video['play']
		current_video.title = video['title']
		current_video.author = video['author']
		current_video.description = video['description']
		current_video.pic = video['pic']
		current_video.pts = video['pts']
		current_video.type = type
		current_video.detail = video
		db_session.commit()
		#print current_video.id
		if cnt < num:
			video_list.append(current_video)
			cnt = cnt + 1
		else:
			break
	return video_list

def show_video_data(num, type):
	res = []
	videos = Video.query.all()
	cnt = 0
	for video in videos:
		if video.videotype is None:
			continue
		if type in video.videotype:
			res.append(video)
			cnt = cnt + 1
			if cnt == num:
				break;
	return res

