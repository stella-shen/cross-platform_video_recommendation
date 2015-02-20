#coding=utf-8
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

class WeibopError(Exception):
	"""Weibopy exception"""

	def __init__(self, reason):
		self.reason = str(reason).encode('utf-8')

	def __str__(self):
		return self.reason

class WeiboAuthError(Exception):
	pass
