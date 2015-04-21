import requests
import urllib
import json

class BiliAPI(object):
	host = 'http://www.bilibili.com'
	api_root = '/index/rank'

	def __init__(self, day = 3):
		if day == 0:
			day = 1
		elif day >= 2 and day <= 4:
			day = 3
		else:
			day = 7
		self.day = day

	def build_url(self):
		url = "%s%s/all-%d-0.json" % (self.host, self.api_root, self.day)
		return url

	def fetch(self):
		url = self.build_url()
		r = requests.get(url)
		r.raise_for_status()

		ret = r.json()
		return ret
		
