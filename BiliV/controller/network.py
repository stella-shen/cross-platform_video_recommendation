import requests
import random

UA_POOL=[
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
]

LANGUAGE_POOL=[
        'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        #'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        #'en-US,en;q=0.8',
]

def _std_header():
  headers = {
    'Accept-Encoding': 'Accept-Encoding: gzip',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': random.choice(UA_POOL),
    'Accept-Language': random.choice(LANGUAGE_POOL),
  }
  return headers

# Human-Like Session
def HLSession():
  s = requests.session()
  s.headers.update(_std_header())
  return s
