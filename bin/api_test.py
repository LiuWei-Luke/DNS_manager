#-*- coding:utf-8 -*-
import requests
import json

a = {'oper' : 'a', 'zone' : 'test3.com', 'file' : 'test3.com.zone'}
r = requests.post(url="http://172.16.2.239:5001/apis/v1.0/zone_randfs", json=a)
c = r.json()
print c['message']
