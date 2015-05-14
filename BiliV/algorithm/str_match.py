#!/usr/bin/python
# -*- coding: utf-8 -*-
import jieba.posseg as pseg
import jieba.analyse

def get_tweet(content):
	res = ''
	words = pseg.cut(content)
	for w in words:
		flag = w.flag
		if flag[0] in ('n', 'a', 'z', 'v') and len(w.word) >= 2:
			res = res + ' ' +w.word
	return res

def get_keyword(content):
	tmp_res = get_tweet(content)
	return jieba.analyse.extract_tags(tmp_res, 20)

