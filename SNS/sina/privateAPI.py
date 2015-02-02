import requests
import json

class privateAPI(object):
	api_host = 'https://api.weibo.com'
	api_root = '/2/'

	def __init__(self, access_token, uid = None):
		self.access_token = access_token
		self.uid = uid

	def get_user_data(self):
		data_url = self.api_host + self.api_root + 'users/show.json?access_token=' + self.access_token + '&uid=' + str(self.uid)
		r = requests.get(data_url)
		return r.text

	def get_weibo_data(self, id):
		data_url = self.api_host + self.api_root + 'statuses/user_timeline.json?access_token=' + self.access_token + '&uid=' + str(id)
		r = requests.get(data_url)
		return r.text

	def get_friends_list(self):
		data_url = self.api_host + self.api_root + 'friendships/friends.json?access_token=' + self.access_token + '&uid=' + str(self.uid)
		r = requests.get(data_url)
		return r.text
