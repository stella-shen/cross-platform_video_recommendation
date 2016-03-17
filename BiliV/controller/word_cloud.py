#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from os import path
from wordcloud import WordCloud, STOPWORDS
from BiliV.foundation import db_session
from BiliV.models import WeiboTweet
import matplotlib.pyplot as plt

stopwords = {}

def stopword(filename = ''):
	global stopwords
	f = open(filename, 'r')
	line = f.readline().rstrip()
	while line:
		stopwords.setdefault(line, 0)
		stopwords[line.decode('utf-8')] = 1
		line = f.readline().rstrip()
	f.close()
	stopword(filename = './stopwords.txt')

def word_cloud_img(uid)
	#read weibo tweet from database
	weibo_tweets = WeiboTweet.query.filter_by(uid = uid).all()

	#The words for wordcloud
	text = ""
	for tweet in weibo_tweets:
		text.append(tweet.text)
	#generate wordcloud image
	wordcloud = WordCloud().generate(text)

	#display the generated image
	plt.imshow(wordcloud)
	plt.axis("off")

	wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
	plt.figure()
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()

