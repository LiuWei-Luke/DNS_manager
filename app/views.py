#-*- coding:utf-8 -*-
from flask import Flask
from flask_restful import Api
import dns_bind
import check_conf
import check_zone
import zone_randfs

app = Flask(__name__)
api = Api(app)
MAIN_URL = '/apis/v1.0/'

api.add_resource(dns_bind.Dns_bind, MAIN_URL + 'dns_bind')
api.add_resource(check_conf.Check_conf, MAIN_URL + 'check_conf')
api.add_resource(check_zone.Check_zone, MAIN_URL + 'check_zone')
api.add_resource(zone_randfs.Zone_randfs, MAIN_URL + 'zone_randfs')

    