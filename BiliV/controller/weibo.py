from SNS import sina
from BiliV.foundation import db
from BiliV.models import Weibo
from BiliV.controller import basic
import json

def get_weibo_data(access_token, uid, id):
	weibo_api = sina.privateAPI(access_token, uid)
	weibo_json = json.loads(weibo_api.get_weibo_data(id))
	weibo_set = weibo_json['statuses']
	for weibo in weibo_set:
		w_id = weibo['id']
		current_weibo = Weibo.query.filter_by(id = w_id).first()
		if current_weibo is None:
			current_weibo = Weibo(id = w_id)
			db.session.add(current_weibo)
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
		db.session.commit()

