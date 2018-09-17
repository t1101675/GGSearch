#-*- coding: utf-8 -*-
import json
dict = {}
with open('data.json', 'r') as f:
    dict = json.load(f)

for key in dict:
    print key
