#!/usr/bin/python
# -*- coding: utf-8 -*-
from BiliV.algorithm import basic
from BiliV.models import Video, Barrage

def fetch_barrage_for_video():
	videos = Video.query.all()
	for video in videos:
		current_id = video.id
		current_barrage = Barrage.query.filter_by(avid = current_id).all()
		content = []
		for cb in current_barrage:
			content.append(cb.text)
		key_words = basic.count(content)


