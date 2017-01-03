#-*- coding:utf-8 -*-
from flask import Flask
from flask_restful import Api
import dns_named
import check_conf
import check_zone
import zone_randfs

app = Flask(__name__)
api = Api(app)
MAIN_URL = '/apis/v1.0/'

#检查named配置
api.add_resource(check_conf.Check_conf, MAIN_URL + 'named_conf')
#检查域名及其配置文件
api.add_resource(check_zone.Check_zone, MAIN_URL + 'zones/check/<zone>')
#直接进行named操作
api.add_resource(dns_named.Dns_named, MAIN_URL + 'named/')
#查看named状态
api.add_resource(zone_randfs.Zone_status, MAIN_URL + 'server_status')
#重新加载一个域名
api.add_resource(zone_randfs.Zone_reload, MAIN_URL + 'zones/reload/<zone>')
#刷新域名缓存或整个缓存
api.add_resource(zone_randfs.Zone_flush, MAIN_URL + 'zones/flush/<zone>')




    