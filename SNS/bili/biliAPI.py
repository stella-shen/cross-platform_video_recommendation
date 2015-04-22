import requests
import urllib
import json

class BiliAPI(object):
	host = 'http://www.bilibili.com'
	api_root = '/index/rank'

	def __init__(self, day = 3, type = 0):
		if day == 0:
			day = 1
		elif day >= 2 and day <= 4:
			day = 3
		else:
			day = 7
		self.day = day
		self.type = type

	def build_url(self, type):
		url = "%s%s/all-%d-%d.json" % (self.host, self.api_root, self.day, self.type)
		return url

	def fetch(self):
		url = self.build_url(self.type)
		r = requests.get(url)
		r.raise_for_status()
		data = r.json()
		rank = data['rank']
		ret = rank['list']
		return ret
		
