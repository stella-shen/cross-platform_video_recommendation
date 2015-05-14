from SNS import bili
from BiliV.foundation import db
from BiliV.models import Video
import json

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
			db.session.add(current_video)
		current_video.play = video['play']
		current_video.title = video['title']
		current_video.author = video['author']
		current_video.description = video['description']
		current_video.pic = video['pic']
		current_video.pts = video['pts']
		current_video.type = type
		current_video.detail = video
		db.session.commit()
		#print current_video.id
		if cnt < num:
			video_list.append(current_video)
			cnt = cnt + 1
		else:
			break
	return video_list

