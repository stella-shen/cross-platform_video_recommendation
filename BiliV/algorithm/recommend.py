#!/usr/bin/python
# -*- coding: utf-8 -*-
from str_match import *
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

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

def calculate_tfidf(tweet_list):
	word_list = []
	for tweet in tweet_list:
		words = get_tweet(tweet)
		word_list.append(words)
	vectorizer = CountVectorizer()
	transformer = TfidfTransformer()
	tfidf = transformer.fit_transform(vectorizer.fit_transform(word_list))
	words = vectorizer.get_feature_names()
	weight = tfidf.toarray()
	return (words, weight)

def calculate_score(tweet_list):
	res = {}
	(words, weight) = calculate_tfidf(tweet_list)
	for word_num in range(len(words)):
		cnt = 0.0
		for doc_num in range(len(weight)):
			cnt = cnt + weight[doc_num][word_num]
		res[words[word_num]] = cnt
	res = sorted(res.items(), key = lambda x:x[1], reverse = True)
	return dict(res)

def recommend_by_tfidf(video, weibo):
	recmd = [] 
	res = calculate_score(weibo)
	words = res.keys()
	print words
	#words = words[5 : -5]
	for v in video:
		video_info = v.title + ' ' + v.description
		for w in words:
			if w in video_info:
				recmd.append(v)
				break
	return recmd


