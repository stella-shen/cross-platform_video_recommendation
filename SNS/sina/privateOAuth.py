
class privateOAuth(object):

	auth_host = 'https://api.weibo.com'
	auth_root = '/oauth2/authorize?'

	def __init__(self, app_key, app_secret, call_back_url):
		self.app_key = app_key
		self.app_secret = app_secret
		self.call_back_url = call_back_url

	def get_auth_url(self):
		auth_url = self.auth_host + self.auth_root + 'client_id=' + self.app_key + '&response_type=code&redirect_uri=' + str(self.call_back_url)
		return auth_url
