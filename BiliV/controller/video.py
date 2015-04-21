from SNS import bili
from BiliV.foundation import db
from BiliV.models import Video
import json

def get_video_data(day):
	bili_api = bili.BiliAPI(day)
	video_json = bili_api.fetch()
	video_set = video_json['list']
	for video in video_set:
		aid = video['aid']
		current_video = Video.query.filter_by(aid == aid).first()
		if current_video is None:
			current_video = Video(aid = aid)
			db.session.add(current_video)
		current_video.play = video['play']
		current_video.title = video['title']
		current_video.author = video['author']
		current_video.description = video['description']
		current_video.pic = video['pic']
		current_video.pts = video['pts']
		current_video.detail = video
		db.session.commit()

