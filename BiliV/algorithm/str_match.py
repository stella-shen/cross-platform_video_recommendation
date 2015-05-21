#!/usr/bin/python
# -*- coding: utf-8 -*-
import jieba
jieba.load_userdict("/home/sz11/biliv/dict.txt")
import jieba.posseg as pseg
import jieba.analyse

def get_tweet(content):
	res = ''
	words = pseg.cut(content)
	for w in words:
		flag = w.flag
		if flag[0] in ('n', 'a', 'z', 'v'):
			res = res + ' ' +w.word
	return res

def get_keyword(content):
	tmp_res = get_tweet(content)
	return jieba.analyse.extract_tags(tmp_res, 20)

