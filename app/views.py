#-*- coding:utf-8 -*-
from flask import Flask
from flask_restful import Api
import dns_named
import check_conf
import check_zone
import zone_randfs
import backup

app = Flask(__name__)
api = Api(app)
MAIN_URL = '/apis/v1.0/'

#检查named配置
api.add_resource(check_conf.Check_conf, MAIN_URL + 'named_conf')
#检查域名及其配置文件
api.add_resource(check_zone.Check_zone, MAIN_URL + 'zones/check/<zone>')
#直接进行named操作
api.add_resource(dns_named.Dns_named, MAIN_URL + 'named/')
#查看域名解析服务状态
api.add_resource(zone_randfs.Zone_status, MAIN_URL + 'server_status')
#重新加载一个域名
api.add_resource(zone_randfs.Zone_reload, MAIN_URL + 'zones/reload/<zone>')
#刷新域名缓存或整个缓存
api.add_resource(zone_randfs.Zone_flush, MAIN_URL + 'zones/flush/<zone>')
#查看当前解析域名列表
api.add_resource(zone_randfs.Zone_list, MAIN_URL + 'zones')
#添加域名，需要指定域名文件
api.add_resource(zone_randfs.Zone_add, MAIN_URL + 'zones')
#删除zone功能,进行freeze,thaw,delzone操作，这里删除只是删除server中的zone，保留了zone文件
api.add_resource(zone_randfs.Zone, MAIN_URL + 'zones/<zone>')
#发送notify
api.add_resource(zone_randfs.Zone_notify, MAIN_URL + 'zones/notify/<zone>')
#下载备份文件
api.add_resource(backup.Download, MAIN_URL + 'download/<filename>')
#对文件进行备份
api.add_resource(backup.Backup, MAIN_URL + 'backup')

    