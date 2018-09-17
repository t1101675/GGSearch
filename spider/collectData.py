#-*- coding: utf-8 -*-
import spider
import handleNews
import json

root = 'http://www.xinhuanet.com/politics/'

spider.runSpider(root, 5000)
handleNews.buildIndex(spider.newsList)

filename = 'data/index.json'
filename2 = 'data/data.json'
filename3 = 'data/TFIDF.json'

with open(filename, 'w') as f:
    json.dump(handleNews.indexDict, f)
print 'data dump'

with open(filename2, 'w') as f2:
    json.dump(spider.newsList, f2)
print 'index dump'

with open(filename3, 'w') as f3:
    json.dump(handleNews.TFIDFTags, f3)
print 'TFIDFdump'
# for key, value in handleNews.indexDict.items():
    # print 'key:', key, 'value: ', value
