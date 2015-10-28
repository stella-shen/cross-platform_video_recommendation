from SNS import sina
from BiliV.foundation import db_session, Base
from BiliV.models import WeiboTweet
from BiliV.controller import basic
import json
import urllib2

def get_weibo_data(access_token, uid):
	weibo_api = sina.WeiboAPI(access_token, uid)
	weibo_json = weibo_api.get_weibo_data()
	weibo_set = weibo_json['statuses']
	for weibo in weibo_set:
		w_id = weibo['id']
		current_weibo = WeiboTweet.query.filter_by(id = w_id).first()
		if current_weibo is None:
			current_weibo = WeiboTweet(id = w_id)
			db_session.add(current_weibo)
		current_weibo.text = weibo['text']
		timestr = weibo['created_at']
		timeinfo = basic.analyze_timestr(timestr)
		current_weibo.created_at = timeinfo['time']
		current_weibo.utc = timeinfo['utc']
		current_weibo.source = weibo['source']
		current_weibo.reposts_cnt = weibo['reposts_count']
		current_weibo.comments_cnt = weibo['comments_count']
		current_weibo.uid = uid
		current_weibo.data_set = str(weibo)
		db_session.commit()

def weibo_page(uid):
	req = urllib2.Request('http://weibo.com/u/' + str(uid))
	response = urllib2.urlopen(req)
	page = response.read()
	return page
