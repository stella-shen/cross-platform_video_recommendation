#!/usr/bin/python
# -*- coding: utf-8 -*-
from BiliV.models import Video, RecommendRelation
from BiliV.algorithm import algorithm
from BiliV.foundation import db_session

def store_into_database(uid, vid, algorithm_name):
	recommend = RecommendRelation.query.filter_by(weibo_user_id=uid, bili_video_id=vid, algorithm = algorithm_name).first()
	if recommend is None:
		current_recommend = RecommendRelation(weibo_user_id=uid, bili_video_id = vid, algorithm = algorithm_name)
		db_session.add(current_recommend)
		#db_session.commit()

def store_recommend_video(uid, num, algorithm_name):
	vlist = Video.query.all()
	if algorithm_name == 'VisitSort':
		recommend_video_list = algorithm.VisitSort(uid, vlist, num)
		for rec_v in recommend_video_list:
			store_into_database(uid, rec_v.id, algorithm_name)
		db_session.commit()
	return

