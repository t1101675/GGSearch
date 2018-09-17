# -*- coding: utf-8 -*-
from urllib2 import Request, urlopen, URLError, HTTPError
from HTMLParser import HTMLParser
import chardet
import re
import Queue
import json
import time

reg = re.compile(r'([12]\d{3})[-]([0]?[1-9]|1[0-2])[-](0[1-9]|[1-2][0-9]|3[01])')

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inTitle = False
        self.beginNews = False
        self.inURL = False
        self.inPassage = False
        self.inTime = False
        self.inScript = False
        self.inURL = False
        self.passage = ''
        self.title = ''
        self.time = ''
        self.reg = re.compile('https?://www.xinhuanet.com/(?!(jblc|jbzx|video|photo))[^\s]*')
        self.news = {}
        self.urlList = []
        self.wrongURL = ['page-Article', 'nextpage']

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.inTitle = True
            self.beginNews = True
        if tag == 'p':
            self.inPassage = True
            # print 'True: ', tag
        if tag == 'a':
            self.inURL = True
            self.getURL(attrs)
        if tag == 'script':
            self.inScript = True

        self.getTime(attrs)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.inTitle = False
        if tag == 'p':
            self.inPassage = False
            # print 'False', tag
        if tag == 'span':
            self.inTime = False
        if tag == 'script':
            self.inScript = False
        if tag == 'a':
            self.inURL = False

    def handle_data(self, data):
        if self.inTitle:
            self.title = data.replace("\r\n", '')
        if self.beginNews and self.inPassage and not self.inScript and not self.inURL:
            if len(data.replace("\r\n", '')) > 5:
                self.passage = self.passage + data.replace("\r\n", '') + '\n'
            # print data.replace("\r\n", '')
        if self.inTime:
            self.time = data.replace("\r\n", '')

    def getAttr(self, attrs, name):
        for m in attrs:
            if m[0] == name:
                return m[1]
        return None

    def getURL(self, attrs):
        url = self.getAttr(attrs, 'href')
        type = self.getAttr(attrs, 'class')
        if (url and self.reg.match(url) and type not in self.wrongURL ):
            self.urlList.append(url)
            # pass#print url

    def getTime(self, attrs):
        type = self.getAttr(attrs, 'class')
        if (type and (type == 'h-time' or type == 'time')):
            self.inTime = True
        type = self.getAttr(attrs, 'id')
        if (type and type == 'pubtime'):
            self.inTime = True

    def getResult(self):
        return {'title':self.title, 'passage':self.passage, 'time':self.time}

    def printResult(self):
        print "Title: ", self.title
        print "Passage: ", self.passage
        print "Time: ", self.time

newsList = []

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

def runSpider(root, num):
    filename = 'news.json'
    f = open(filename, 'w')
    visitSet = set()
    Q = Queue.Queue()
    Q.put(root)
    n = 0
    while n < num and not Q.empty():
        url = Q.get()
        if url not in visitSet:
            print url
            visitSet.add(url)
            req = Request(url = url, headers = headers)
            response = urlopen(req)
            html = response.read()
            parser = Parser()
            parser.feed(html)
            global newsList
            newsDict = parser.getResult()
            if (len(newsDict['passage']) > 200 and reg.search(newsDict['time'])):
                newsDict['id'] = n
                newsList.append(newsDict)
                parser.printResult()
                print "length: ", len(newsDict['passage'])
                print "number: ", n
                print "\n\n"
                n += 1
            urlList = parser.urlList
            for url in urlList:
                Q.put(url)
            time.sleep(0.5)
    f.close()
