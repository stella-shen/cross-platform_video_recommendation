
class privateOAuth(object):

	auth_host = 'https://api.weibo.com'
	auth_root = '/oauth2/authorize?'

	def __init__(self, app_key, app_secret, call_back_url, code):
		self.app_key = app_key
		self.app_secret = app_secret
		self.call_back_url = call_back_url
		self.code = code

	def get_auth_url(self):
		auth_url = self.auth_host + self.auth_root + 'client_id=' + self.app_key + '&response_type=code&redirect_uri=' + str(self.call_back_url)
		return auth_url

	def get_access_token_url(self):
		access_url = slef.auth_host + '/oauth2/access_token?client_id=' + self.app_key + '&client_secret=' + self.app_secret + '&grant_type=authorization_code&redirect_uri=' + self.call_back_url + '&code=' + self.code
