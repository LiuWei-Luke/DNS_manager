#-*- coding:utf-8 -*-
from flask import Flask
from flask_restful import Api
import dns_bind

app = Flask(__name__)
api = Api(app)
MAIN_URL = '/apis/v1.0/'

api.add_resource(dns_bind.Dns_bind, MAIN_URL + 'dns_bind')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    