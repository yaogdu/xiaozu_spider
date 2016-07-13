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
import jieba
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
    def pa(self, url, start, limit):

        md = MongoDBPipeline(DB['db'], DB['col'], DB['address'])

        while start <= limit:
            url = url.split('=').pop(0) + '='
            url += str(start)
            start += 25

            print url

            s = requests.session()
            headers = {"User-Agent": UA}
            s.headers.update(headers)

            r = s.get(url, timeout=(2, 4))

            html = r.text
            # print html
            # soup = BeautifulSoup(html, 'lxml')
            # p = re.compile(r'\?wx_fmt.+?\"')
            # content = str(soup)
            d = pq(html)
            # item =
            aArray = d.find('.olt').find('tr')

            items = []
            for i in aArray:
                it = pq(i)

                clazz = it.attr('class')

                if None == clazz:  ## class 为 None的tr标签

                    print it

                elif "" == clazz:  # class 为 "" 的标签
                    trItems = it.children()
                    item = {}

                    for j in range(0, 4):
                        jItem = pq(trItems[j])
                        href = item.get('href')
                        if href != None:
                            item['md5'] = hashlib.new("md5", item['href']).hexdigest()
                            tmp = md.find({'md5': item['md5']})
                            if tmp != None:
                                item['md5'] = ''

                        if j == 0:
                            item['title'] = jItem.find('a').attr('title')
                            item['href'] = jItem.find('a').attr('href')
                        elif j == 1:
                            item['author'] = jItem.text()
                            item['author_link'] = jItem.find('a').attr('href')
                        elif j == 2:
                            item['reply_count'] = jItem.text()
                        else:
                            item['last_reply'] = jItem.text()

                    if item.get('md5') != None and item.get('md5') != '':
                        items.append(item)

            print items.__len__()
            if items.__len__() > 0:
                self.loop_article(items,s,pq)

            times = 0
            for i in items:
                times += 1
                md.save(i)

            print('saved ' + str(times) + ' records')
            time.sleep(5)

    def loop_article(self, items,s,pq):
        print 'coming in to fetch_article..'
        if items != None:
            for i in items:
                href = i.get('href')
                content = self.fetch_article(href,s,pq)
                #print content
                if content != None:
                    sub_list = jieba.cut_for_search(content)
                    if sub_list !=None:
                        sub_content = []
                        for tag in sub_list:
                            sub_content.append(tag)

                        i['sub_list'] = sub_content
                else:
                    i['sub_list'] = []
                    print 'href '+href +' content is none'
        return items

    def fetch_article(self, href,s,pq):
        print href
        r = s.get(href, timeout=(4, 8))
        html = r.text
        d = pq(html)
        content = d.find('.topic-content').find('p').html()

        time.sleep(2)
        return content


if __name__ == '__main__':
    spider = spider()
    spider.pa('https://www.douban.com/group/fangzi/discussion?start=', 0,500)
