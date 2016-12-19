#-*- coding:utf-8 -*-

import subprocess
from flask_restful import Resource, reqparse

help = """
       oper 操作:
            r 加载配置
            a 添加域名
            n 重新发送notify消息
            d 删除域名
            f 刷新缓存
            s 查看状态
        view 操作的视图
        zone zone名称
        file zone文件
       """
class Zone_randfs(Resource):
    """
    该接口动态添加、删除域名，加载配置，刷新缓存，查看bind状态
    主要使用rndc进行操作
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('oper', type=str, required=True,
                                   help='required a operation', location='json')
        self.reqparse.add_argument('view', type=str, default='default',
                                   location='json')
        self.reqparse.add_argument('zone', type=str, required=True,
                                   location='json', help='required zone name')
                                   
        super(Zone_randfs, self).__init__()
    
    def post(self):
        