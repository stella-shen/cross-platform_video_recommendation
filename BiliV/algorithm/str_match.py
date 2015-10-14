#!/usr/bin/python
# -*- coding: utf-8 -*-
import jieba
jieba.load_userdict("/home/sz11/biliv/dict.txt")
import jieba.posseg as pseg
import jieba.analyse
from basic import *

def get_keyword(content):
	tmp_res = get_tweet(content)
	return jieba.analyse.extract_tags(tmp_res, 20)

