from SNS import sina
from BiliV.foundation import db
from BiliV.models import Friends

def get_friends_data(access_token, uid):
	friends_api = sina.privateAPI(access_token, uid)
	friends_json = json.loads(friends_api.get_friends_list())
	friends_set = friends_json['users']
	for friend in friends_set:
		f_id = friend['id']
		current_friend = Friends.query.filter_by(id = f_id).first()
		if current_friend is None:
			current_friend = Friends(id = f_id)
			db.session.add(current_friend)
		current_friend.uid = uid
		current_friend.screen_name = friend['screen_name']
		current_friend.description = friend['description']
		current_friend.profile_url = friend['profile_url']
		current_friend.gender = friend['gender']
		current_friend.follow_me = friend['follow_me']
		current_friend.data_set = friend
		db.session.commit()


