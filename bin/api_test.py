import requests
import json

r = requests.get(url="http://172.16.2.239:5001/apis/v1.0/dns_bind")

print r.text