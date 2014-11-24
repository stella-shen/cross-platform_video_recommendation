import requests

class privateOAuth(object):

	auth_host = 'https://api.weibo.com'
	auth_root = '/oauth2/'

	def __init__(self, app_key, app_secret, call_back_url, code = None):
		self.app_key = app_key
		self.app_secret = app_secret
		self.call_back_url = call_back_url
		self.code = code

	def get_auth_url(self):
		auth_url = self.auth_host + self.auth_root + 'authorize?client_id=' + self.app_key + '&response_type=code&redirect_uri=' + str(self.call_back_url)
		return auth_url

	def get_access_token_url(self):
		access_url = self.auth_host + self.auth_root + 'access_token?client_id=' + self.app_key + '&client_secret=' + self.app_secret + '&grant_type=authorization_code&redirect_uri=' + self.call_back_url + '&code=' + self.code
		return access_url

	def get_access_token(self):
		postdata = {
				'redirect_url' : self.call_back_url,
				'client_id' : seld.app_key,
				'grant_type' : 'authorization_code',
				'code' : self.code,
				'client_secret' : self.app_secret
				}
		request_url = 'https://api.weibo.com/oauth2/access_token'
		r = requests.post(request_url, data=postdata)
		return r.text

