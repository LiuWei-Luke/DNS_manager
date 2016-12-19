import requests
import json

a = {'domain' : 'test.com'}
r = requests.post(url="http://172.16.2.239:5001/apis/v1.0/check_zone", json=a)
print r.text