#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import logging.config
import time
import hashlib
import re
import json
import urllib
import urllib2
import random
import sys
import base64

from flask import Flask, request
from flask_restful import Resource, Api
from bs4 import BeautifulSoup
import requests
from pyquery import PyQuery as pq

app = Flask(__name__)
api = Api(app)

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("spider")
reload(sys)
sys.setdefaultencoding('utf8')


class Spider(Resource):
    def get(self):
         return 'hello world'


api.add_resource(Spider, '/')

try:
    logger.info('succeed init env')
except Exception, ex:
    logger.error('config file error,prepare to user test.py')
    app.config.from_pyfile('test.py')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
