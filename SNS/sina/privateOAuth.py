import requests
import urllib
import error

class WeiboAPI(object):
	"Do not support saving access_token, because we don't need at this level"

	host = 'https://api.weibo.com'
	auth_root = '/oauth2'
	api_root = '/2'

	def __init__(self, app_key, app_secret):
		self.app_key = app_key
		self.app_secret = app_secret

	def build_auth_url(self, interface, get_params = None):
		"get_params: dict contain key value pair"
		url = "%s%s/%s" % (self.host, self.auth_root, interface)
		if get_params:
			# ignore when no paramas or params is empty dictionary
			suffix = urllib.urlencode(get_params)
			url = ''.join([url, '?', suffix])
		return url

	def get_auth_url(self, callback_url):
		data = {
			"response_type": "code",
			"redirect_uri": callback_url,
			"client_id": self.app_key,
		}
		auth_url = self.build_auth_url('authorize', data)
		return auth_url

	def exchange_access_token(self, callback_url, code):
		postdata = {
			'client_secret' : self.app_secret,
			'client_id' : self.app_key,
			'grant_type' : 'authorization_code',
			'code' : code,
			'redirect_uri' : self.call_back_url,
		}
		return self._get_token(postdata)

	def refresh_access_token(self, refresh_token):
		postdata = {
			'client_secret' : self.app_secret,
			'client_id' : self.app_key,
			'grant_type' : 'refresh_token',
			'refresh_token' : refresh_token,
		}
		return self._get_token(postdata)

	def _get_token(self, data):
		url = self.build_auth_url('access_token')

		# check for validation
		r = requests.post(url, data=data)
		r.raise_for_status()

		ret = r.json()
		if 'code' in ret:
			# exchange fail!
			raise error.WeiboAuthError(ret['msg'])
		flags = map(lambda key: key in ret, ['access_token', 'expires_in', 'refresh_token'])
		if not all(flags):
			raise error.WeiboAuthError('Got unexpect result')

		return ret
