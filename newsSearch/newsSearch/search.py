#-*- coding: utf-8 -*-
import json
import re
import datetime
from math import *
indexDict = {}
newsList = []
TFIDFTags = []

filename = '../spider/data3/index.json'
filename2 = '../spider/data3/data.json'
filename3 = '../spider/data3/TFIDF.json'

reg = re.compile(r'([12]\d{3})[-]([0]?[1-9]|1[0-2])[-](0[1-9]|[1-2][0-9]|3[01])')

def init():
    global indexDict
    global newsList
    global TFIDFTags
    with open(filename) as f:
        indexDict = json.load(f)
    with open(filename2) as f2:
        newsList = json.load(f2)
    with open(filename3) as f3:
        TFIDFTags = json.load(f3)
    print "Data loaded"

def search(textList, startTime = None, endTime = None):
    allIdList = []
    idTimesDict = {}
    for text in textList:
        if text in indexDict:
            # print 'ok'
            tempList = indexDict[text]
            idList = []
            for id in tempList[0]:
                idList.append(id)
            for id in tempList[1]:
                if (id not in idList):
                    idList.append(id)
            allIdList.append(idList)
    for idList in allIdList:
        for id in idList:
            if str(id) in idTimesDict:
                idTimesDict[str(id)] += 1
            else:
                idTimesDict[str(id)] = 1
    newsIdList = sorted(idTimesDict.items(), key=lambda e:e[1], reverse=True)

    resultList = []
    if startTime and endTime:
        d1 = datetime.datetime.strptime(startTime, '%Y-%m-%d')
        d2 = datetime.datetime.strptime(endTime, '%Y-%m-%d')
        for tuple in newsIdList:
            id = int(tuple[0])
            t = reg.search(newsList[id]['time'])
            # print newsList[id]['time']
            if (t):
                time = datetime.datetime.strptime(t.group(), '%Y-%m-%d')
                if d1 <= time and time <= d2:
                    resultList.append(newsList[id])
    else:
        for tuple in newsIdList:
            id = int(tuple[0])
            resultList.append(newsList[id])
    return resultList

def getSimilar(id):
    length = len(newsList)
    simi = [-1 for i in range(length)]
    for tag in TFIDFTags[id]:
        # print tag[0]
        for i in range(length):
            if (i is not id):
                sum = 0.0
                for otherTag in TFIDFTags[i]:
                    if otherTag[0] == tag[0]:
                        sum += otherTag[1] * tag[1]
                simi[i] = sum
                # print sum
    similarList = []
    for i in range(3):
        max = -2
        index = -1
        for i in range(length):
            if simi[i] > max:
                index = i
                max = simi[i]
        similarList.append(index)
        simi[index] = float("-inf")
    return similarList
