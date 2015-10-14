#!usr/bin/python
# -*- coding: utf-8 -*-
import jieba
jieba.load_userdict("/home/sz11/biliv/dict.txt")
import jieba.posseg as pseg
import jieba.analyse

def get_tweet(tweet):
	res = ' '
	words = pseg.cut(tweet)
	for w in words:
		flag = w.flag
		if flag[0] in ('n', 'a', 'z', 'v'):
			res = res + ' ' + w.word
	return res

def count(content):
	res = {}
	for tweet in content:
		words = pseg.cut(tweet)
		for w in words:
			flag = w.flag
			word = w.word
			if flag[0] in ('n', 'a', 'z', 'v'):
				if res.has_key(word):
					res[word] = res[word] + 1
				else:
					res[word] = 1
	res = sorted(res.iteritems(), key = lambda x: x[1], reverse = True)
	if len(res) > 1000:
		return res[0 : 1000]
	else:
		return res

