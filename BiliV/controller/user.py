from SNS import sina
from BiliV.models import User

def get_user_data(access_token, uid):
	user_api = sina.privateAPI(access_token, uid)
	data_json = json.loads(user_api.get_user_data())
	current_user = User.query.filter_by(id == uid).first()
	if current_user is None:
		current_user = User(id = uid)
		db.session.add(user)
		screen_name = data_json['screen_name']
	current_user.screen_name = data_json['screen_name']
	current_user.access_token = access_token
	current_user.description = data_json['description']
	current_user.gender = data_json['gender']
	current_user.image_url = data_json['profile_image_url']
	current_user.url = data_json['url']
	current_user.followers_cnt = data_json['followers_count']
	current_user.friends_cnt = data_json['friends_count']
	current_user.statuses_cnt = data_json['statuses_count']
	current_user.bi_followers_count = data_json['bi_followers_count']
	current_user.data_set = str(data_json)
	db.session.commit()

