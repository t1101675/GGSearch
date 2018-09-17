from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
import os
import ctypes
import hashlib
import random
from ctypes import *

AllNewsResult = []
AllAnswerResult = []
so = ctypes.cdll.LoadLibrary
lib = so("C:\Guyuxian\Discrete Mathematics(2)\GZSearcher\CXXHandler\CXXHandler.so")

def init():
    print("init")
    lib.init()

def searchStart(request):
    return render_to_response("StartPage.html")

def receiveInput(request):
    textDict = {}
    textDict['input'] = request.GET.get('searchText', False)
    inputText = textDict['input']
    if 'seriousSearch' in request.GET:
        AllNewsResult.clear()
        AllAnswerResult.clear()
        input_p = c_wchar_p(textDict['input']);
        print(input_p.value)
        so = ctypes.cdll.LoadLibrary
        lib.CXXSearch(str(inputText.encode('utf-16-le')), len(inputText))
        #lib.CXXSearch(input_p, len(textDict['input']))
        lib.CreateInstance(1)
        n = lib.ResultSize()
        textDict['cxxinput'] = input_p.value
        textDict['n'] = n

        for i in range(0, n):
            c_i = c_int(i)

            #compute title
            pyGetTitle = lib.GetTitle
            pyGetTitle.argtypes = [c_int]
            pyGetTitle.restype = c_char_p
            btitle = pyGetTitle(c_i)
            title = btitle.decode()

            #compute url
            pyGetUrl = lib.GetUrl
            pyGetUrl.argtypes = [c_int]
            pyGetUrl.restype = c_char_p
            burl = pyGetUrl(c_i)
            url = burl.decode()

            #compute context
            pyGetContext = lib.GetContext
            pyGetContext.argtypes = [c_int]
            pyGetContext.restype = c_char_p
            bcontext = pyGetContext(c_i)
            context = bcontext.decode()

            #compute type
            type = lib.GetType(c_i)
            result = {'title': title, 'url': url, 'context': context}
            if type == 0:
                AllNewsResult.append(result)
            else:
                AllAnswerResult.append(result)
        return render(request, 'SeriousAnswer.html', {'answers': AllAnswerResult, 'number': len(AllAnswerResult), 'searchInput': inputText})
    else:
        ans = random.randint(1, 4)
        if ans == 1:
            return render(request, 'Aanswer.html', {'searchInput': inputText})
        elif ans == 2:
            return render(request, 'Banswer.html', {'searchInput': inputText})
        elif ans == 3:
            return render(request, 'Canswer.html', {'searchInput': inputText})
        else:
            return render(request, 'Danswer.html', {'searchInput': inputText})

def showSeriousAnswer(request):
    return render(request, 'SeriousAnswer.html', {'answers': AllAnswerResult, 'number': len(AllAnswerResult)})

def showNews(request):
    return render(request, 'News.html', {'answers':AllNewsResult, 'number': len(AllNewsResult)});
