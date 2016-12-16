#-*— coding:utf-8 -*-

import subprocess
from flask_restful import Resource, reqparse


class Dns_bind(Resource):
    """
    bind接口，负责DNS服务的启动、关闭、重启、状态
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('operation', type='str', required=None,
                                   help="required operation", location='json')
        super(Dns_bind, self).__init__()

    def get(self):
        """
        直接通过get进行操作，之后要附加验证方法
        """
        try:
            oper = subprocess.check_output("service named restart", shell=True)
            print oper
            return {"message" : "operate successed", "result" : oper}, 200
        except subprocess.CalledProcessError:
            return {"error" : "operate failed"}, 500

