#!/usr/bin/python
# -*- coding: utf-8 -*-
from str_match import *

def recommend_by_str_match(video, weibo):
	res = []
	weibo_keyword = get_keyword(weibo)
	for v in video:
		video_info = v.title + ' ' + v.description
		for wk in weibo_keyword:
			if wk in video_info:
				res.append(v)
				break
	return res

