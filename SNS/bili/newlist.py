from BiliV import const
from BiliV.controller.network import HLSession
from bs4 import BeautifulSoup
import re, logging
from BiliV.models import Video
from BiliV.foundation import db

video_num_regex = re.compile(r'\/video\/av(\d+)/')
video_type_regex = re.compile(r'\/newlist.html\?typeid=(\d+)')
last_num_regex = re.compile(r'.*page=(\d+)\b')

def extract_video(doc):
	ret = []
	for e in doc.select('.l1'):
		tmp = {}
		tmp['pic'] = e.find('img')['src']
		title_dom = e.find(class_="title")
		tmp['title'] = title_dom.text
		tmp['aid'] = int(video_num_regex.match(title_dom['href']).group(1), 10)
		tmp['author'] = e.find(class_="up").text
		tmp['description'] = e.find(class_="info").text
		type_name = e.find(class_="typename")
		tmp['type'] = int(video_type_regex.match(type_name['href']).group(1), 10)
		ret.append(tmp)
	return ret

def extract_page_num(doc):
	last_btn = doc.find(class_="endPage")
	if not last_btn:
		return 1
	last_num = int(last_num_regex.match(last_btn['href']).group(1), 10)
	return last_num

def load():
	s = HLSession()
	arguments = {
			"timeout" : 30,
			"allow_redirects" : False,
			}
	r = s.get(const.NEW_LIST_URL, **arguments)
	logging.debug("newlist fetching...")

	doc = BeautifulSoup(r.content)
	result = extract_video(doc)
	for r in result:
		aid = int(r['aid'])
		if aid is None:
			continue
		current_video = Video.query.filter_by(id=aid).first()
		if current_video is not None:
			continue
		current_video = Video(id=aid)
		current_video.title = r['title']
		current_video.description = r['description']
		current_video.author = r['author']
		current_video.pic = r['pic']
		current_video.type = r['type']
		db.session.add(current_video)
		db.session.commit()
	logging.debug("result stored")

