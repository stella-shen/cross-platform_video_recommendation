#!/usr/bin/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XML
from network import HLSession
from BiliV.models import Barrage, Video
from BiliV.foundation import db
import re, sys
from sqlalchemy import and_

default_encoding = 'utf-8'
cnt = 0
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)

def get_xml_url(avid):
	webs = HLSession()
	video_url = "http://www.bilibili.com/video/av%s/" % (avid)
	resp = webs.get(video_url)
	resp.encoding='utf-8'
	origin_text = resp.text
	text = re.findall(ur'cid=(\d+)', origin_text)
	if(text):
		cid = re.findall(ur'cid=(\d+)', origin_text)[0]
		xml_url = 'http://comment.bilibili.com/%s.xml' % (cid)
	else:
		xml_url = ''
	return xml_url

def read_xml(url):
	webs = HLSession()
	r = webs.get(url)
	r.encoding = 'utf-8'
	text = r.text
	if text is not None and text[-1] != '>':
		text += '>'
	text = re.sub(u'[\x00-\x08\x0b-\x0c\x0e-\x1f]+', u'', text)
	return text

def extract_xml(avid):
	xml_url = get_xml_url(avid)
	if len(xml_url) == 0:
		return ''
	xml = read_xml(xml_url)
	#parser = ET.XMLParser(encoding="utf-8")
	#xml_file = open("./BiliV/controller/xml/%s.xml" % (avid), "w+")
	#xml_file.write(xml)
	root = ET.fromstring(xml)
	#root = ET.parse(xml).getroot()
	#xml_file.close()
	all_barrage = root.findall('d')
	global cnt
	for b in all_barrage:
		cnt = cnt + 1
		if cnt <= 314932:
			print cnt
			continue
		attr = b.attrib.get('p').split(',')
		second = float(attr[0])
		mode = int(attr[1])
		font_size = float(attr[2])
		color = int(attr[3], 10)
		timestamp = int(attr[4])
		pool = int(attr[5])
		owner = attr[6]
		rowid = int(attr[7])
		barrage = b.text
		current_barrage = Barrage.query.filter(and_(Barrage.avid==avid, Barrage.rowid==rowid)).first()
		if current_barrage is None:
			fresh = Barrage.query.filter_by(text = barrage).first()
			if fresh is None:
				current_barrage = Barrage()
				current_barrage.avid = avid
				current_barrage.text = barrage
				current_barrage.second = second
				current_barrage.mode = mode
				current_barrage.font_size = font_size
				current_barrage.color = color
				current_barrage.timestamp = timestamp
				current_barrage.pool = pool
				current_barrage.owner = owner
			else:
				continue
		else:
			continue
		db.session.add(current_barrage)
		db.session.commit()
	#xml_file.close()

def get_barrage():
	videos = Video.query.all()
	for video in videos:
		avid = video.id
		extract_xml(avid)

#extract_xml(1913475)

