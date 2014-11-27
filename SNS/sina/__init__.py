#coding=utf-8
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

"""
weibo API library
"""
__version__ = '1.5'
__author__ = 'Joshua Roesslein'
__license__ = 'MIT'

from .error import WeibopError
from .privateOAuth import privateOAuth
from .privateAPI import privateAPI

