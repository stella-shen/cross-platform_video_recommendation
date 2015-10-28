from SNS import sina
from BiliV.foundation import db_session
from BiliV.models import WeiboUser, WeiboRelation
from BiliV.controller import basic
import json

def get_friends_data(access_token, uid):
	friends_api = sina.WeiboAPI(access_token, uid)
	followers_json = friends_api.get_follower_list()
	followers_set = followers_json['users']
	current_user = WeiboUser.query.filter_by(id = uid).first()
	for friend in followers_set:
		f_id = friend['id']
		current_friend = WeiboUser.query.filter_by(id = f_id).first()
		if current_friend is None:
			current_friend = WeiboUser(id = f_id)
			db_session.add(current_friend)
			db_session.commit()
			follower = WeiboRelation(follower_id=f_id, followed_id=uid)
			db_session.add(follower)
		current_friend.uid = uid
		current_friend.screen_name = friend['screen_name']
		current_friend.description = friend['description']
		current_friend.profile_url = friend['profile_url']
		current_friend.gender = basic.analyze_gender(friend['gender'])
		current_friend.follow_me = friend['follow_me']
		current_friend.data_set = str(friend)
		db_session.commit()
	followed_json = friends_api.get_followed_list()
	followed_set = followed_json['users']
	for friend in followed_set:
		f_id = friend['id']
		current_friend = WeiboUser.query.filter_by(id = f_id).first()
		if current_friend is None:
			current_friend = WeiboUser(id = f_id)
			db_session.add(current_friend)
			db_session.commit()
			followed = WeiboRelation(follower_id=uid, followed_id=f_id)
			db_session.add(followed)
		current_friend.uid = uid
		current_friend.screen_name = friend['screen_name']
		current_friend.description = friend['description']
		current_friend.profile_url = friend['profile_url']
		current_friend.gender = basic.analyze_gender(friend['gender'])
		current_friend.follow_me = friend['follow_me']
		current_friend.data_set = str(friend)
		current_user.followed.append(current_friend)
		db_session.commit()
	return


