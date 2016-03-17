import requests
import error
import urllib

class WeiboAPI(object):
	host = 'https://api.weibo.com'
	api_root = '/2'

	def __init__(self, access_token, uid = None):
		self.access_token = access_token
		self.uid = uid

	def build_url(self, interface, get_params = {}, token=True):
		"get_params: dict contain key value pair"
		url = "%s%s/%s" % (self.host, self.api_root, interface)
		if token:
			get_params['access_token'] = self.access_token
		if get_params:
			# ignore when no paramas or params is empty dictionary
			suffix = urllib.urlencode(get_params)
			url = ''.join([url, '?', suffix])
		return url

	def fetch(self, url):
		r = requests.get(url)
		r.raise_for_status()

		ret = r.json()
		if 'error_code' in ret:
			raise error.WeiboAPIError('%s - %s' % \
					(ret['error_code'], ret.get('error', ''))\
			)
		return r.json()

	def get_user_data(self):
		url = self.build_url('users/show.json', {"uid": self.uid, "access_token": self.access_token})
		return self.fetch(url)

	def get_weibo_data(self):
		url = self.build_url('statuses/user_timeline.json', {"access_token": self.access_token, "uid": self.uid})
		return self.fetch(url)

	def get_followed_list(self):
		url = self.build_url('friendships/friends.json', {"access_token": self.access_token, "uid": self.uid, "count": str(200)})
		return self.fetch(url)

	def get_follower_list(self):
		url = self.build_url('friendships/followers.json', {"access_token": self.access_token, "uid": self.uid, "count": str(200)})
		return self.fetch(url)
