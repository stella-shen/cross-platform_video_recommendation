import datetime, time

def analyze_timestr(timestr):
	time_list = timestr.split(" ")
	utc = time_list[-2]
	index = timestr.find(utc)
	timestr = timestr[ : index - 1] + timestr[index + len(utc) : ]
	date = time.strptime(timestr)
	return {'time' : date, 'utc' : utc}

