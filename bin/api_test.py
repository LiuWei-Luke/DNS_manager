#-*- coding:utf-8 -*-
import requests
import json

# a = {'oper' : 'y', 'zone' : 'test4.com', 'file' : 'test4.com.zone'}
a = {'zone' : 'test3.com'}
# r = requests.post(url="http://172.16.10.254:5001/apis/v1.0/zone_randfs", json=a)
r = requests.get(url="http://172.16.2.239:5001/apis/v1.0/backup")
c = r.json()
print c['message']
