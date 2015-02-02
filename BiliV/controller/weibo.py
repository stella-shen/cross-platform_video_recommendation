from SNS import sina
from BiliV.models import Weibo

def get_weibo_data(access_token, uid, id):
    weibo_api = sina.privateAPI(access_token, uid)
    weibo_json = json.loads(weibo_api.get_weibo_data(id))
	weibo_set = weibo_json['statuses']
	weibo_list = []
	for weibo in weibo_set:
		w_id = weibo['id']
		current_weibo = Weibo.query.filter_by(id = w_id).first()
		if current_weibo is None:
			

def get_id_data(access_token, uid, other_id):
	#get weibo data
	weibo_api = sina.privateAPI(access_token, uid)
	weibo_json = json.loads(weibo_api.get_other_weibo_data(other_id))
	return repr(weibo_json)
	weibo_set = weibo_json['statuses']
	weibo_list = []
	for weibo in weibo_set:
		w_id = weibo['id']
		text = weibo['text']
		weibo_list.append(text.encode("utf8"))
		source = weibo['source']
		reposts_cnt = weibo['reposts_count']
		comments_cnt = weibo['comments_count']
		w_uid = other_id
		created_at = weibo['created_at']
		weibo = str(weibo)
		current_weibo = Weibo.query.filter(Weibo.id == w_id).first()
		if current_weibo is None:
			weibo = Weibo(id = w_id, uid = w_uid, created_at = created_at, text = text, source = source, reposts_cnt = reposts_cnt, comments_cnt = comments_cnt, data_set = weibo)
			db.session.add(weibo)
		else:
			current_weibo.uid = uid
			current_weibo.created_at = created_at
			current_weibo.text = text
			current_weibo.source = source
			current_weibo.reposts_cnt = reposts_cnt
			current_weibo.comments_cnt = comments_cnt
			current_weibo.data_set = weibo
		db.session.commit()
		return repr(weibo_list)


