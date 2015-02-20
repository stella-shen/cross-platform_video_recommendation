#coding=utf-8
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

"""
weibo API library
"""
__version__ = '1.0'
__author__ = 'UGeeker'
__license__ = 'MIT'

from .error import WeibopError
from .privateOAuth import WeiboAPI
from .privateAPI import privateAPI

