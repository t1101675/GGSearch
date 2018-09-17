#-*- coding: utf-8 -*-
import jieba
import jieba.analyse
import json
from string import punctuation

add_punc = '，。、【 】 “”“”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥'
all_punc = punctuation + add_punc

indexDict = {}
TFIDFTags = []

def buildIndex(newsList):
    global indexDict
    titleTokenList = []
    passageTokenList = []
    for dict in newsList:
        print 'jieba for ', dict['id']
        passageToken = jieba.lcut_for_search(dict['passage'], HMM=True)
        passageTags = jieba.analyse.extract_tags(dict['passage'], topK=20, withWeight=True)
        titleToken = jieba.lcut_for_search(dict['title'], HMM=True)
        for c in all_punc:
            while c in titleToken:
                titleToken.remove(c)
            while c in passageToken:
                passageToken.remove(c)
        titleTokenList.append(titleToken)
        passageTokenList.append(passageToken)
        TFIDFTags.append(passageTags)


    n_title = len(titleTokenList)
    n_passage = len(passageTokenList)

    for i in range(0, n_title):
        print 'title for ', i
        for str in titleTokenList[i]:
            if str in indexDict:
                if (i not in indexDict[str][0]):
                    indexDict[str][0].append(i)
            else:
                indexDict[str] = [[i], []]

    for i in range(0, n_passage):
        print 'passage for ', i
        for str in passageTokenList[i]:
            if str in indexDict:
                if (i not in indexDict[str][1]):
                    indexDict[str][1].append(i)
            else:
                indexDict[str] = [[], [i]]
