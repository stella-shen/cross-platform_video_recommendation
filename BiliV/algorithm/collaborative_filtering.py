from math import sqrt

class UserBasedCF:
	def __init__(self):
		W = dict()

	def user_similarity(user1, user2):
		like_video1 = user1.like_videos
		like_video2 = user2.like_videos
		video_list1 = []
		video_list2 = []
		for v in like_video1:
			video_list1.append(v.id)
		common = 0
		for v in like_video2:
			video_list2.append(v.id)
			if v.id in video_list1:
				common = common + 1
		
		similarity = common / (sqrt(len(video_list1) * len(video_list2)))
		return similarity

	def calculate_all(self, users):
		l = len(users)
		for i in range(0, l):
			for j in range(i + 1, l):
				user1 = users[i]
				user2 = users[j]
				user_sim = user_similarity(user1, user2)
				self.W[user1][j] = user_sim
				self.W[user2][i] = user_sim
	
	def recommend(self, user, K = 10, N = 9):
		for v in sorted(self.W[user.items(), key=lambda x:x[1], reverse=True])[0 : K]:
			

