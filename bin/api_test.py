#-*- coding:utf-8 -*-
import requests
import json

# a = {'oper' : 'y', 'zone' : 'test4.com', 'file' : 'test4.com.zone'}
# a = {'oper' : 's'}
# r = requests.post(url="http://172.16.10.254:5001/apis/v1.0/zone_randfs", json=a)
r = requests.get(url="http://172.16.2.239:5001/apis/v1.0/download/test.com.zone")
#c = r.json()
#print c['message']
