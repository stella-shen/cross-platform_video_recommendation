import datetime, time
from BiliV import const

def analyze_timestr(timestr):
	time_list = timestr.split(" ")
	utc = time_list[-2]
	index = timestr.find(utc)
	timestr = timestr[ : index - 1] + timestr[index + len(utc) : ]
	time_tuple = time.strptime(timestr)
	date = datetime.datetime(*time_tuple[0:6])
	return {'time' : date, 'utc' : utc}

def analyze_gender(gender):
	if gender == 'm':
		return const.GENDER_MALE
	elif gender == 'f':
		return const.GENDER_FEMALE
	else:
		return const.GENDER_NONE

