#!/usr/bin/env python
# encoding: utf-8

def VisitSort(userid, vlist, num):
	vlist.sort(lambda x, y: cmp(x.play, y.play), reverse = True)
	return vlist[:num]
