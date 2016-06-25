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

from db import MongoDBPipeline

from test import DB

reload(sys)
sys.setdefaultencoding('utf8')


UA = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"

class spider(object):
    def pa(self,url):
        s = requests.session()
        headers = {"User-Agent": UA}
        s.headers.update(headers)

        r = s.get(url,timeout=(2, 4))

        html = r.text
        #soup = BeautifulSoup(html, 'lxml')
        #p = re.compile(r'\?wx_fmt.+?\"')
        #content = str(soup)
        d = pq(html)
        #item =
        aArray = d.find('.olt').find('tr')

        items = []
        for i in aArray:
            it = pq(i)


            clazz = it.attr('class')

            if None == clazz:## class 为 None的tr标签

                print it

            elif "" == clazz:# class 为 "" 的标签
                trItems = it.children()
                item = {}

                for j in range(0,4):
                    jItem = pq(trItems[j])
                    if j == 0:
                        item['title'] = jItem.find('a').attr('title')
                        item['href'] =  jItem.find('a').attr('href')
                    elif j == 1:
                        item['author'] = jItem.text()
                        item['author_link'] = jItem.find('a').attr('href')
                    elif j == 2:
                        item['reply_count'] = jItem.text()
                    else:
                        item['last_reply'] = jItem.text()

                    item['md5'] = hashlib.new("md5", item['href']).hexdigest()

                items.append(item)

        md = MongoDBPipeline(DB['db'], DB['col'], DB['address'])

        for i in items:
            md.save(i)

        print('saved '+ str(items.__len__()) +' records')






if __name__ == '__main__':
    spider = spider()
    spider.pa('https://www.douban.com/group/fangzi/')
