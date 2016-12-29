#-*— coding:utf-8 -*-

import subprocess
from flask_restful import Resource, reqparse


class Dns_bind(Resource):
    """
    bind接口，负责DNS服务的启动、关闭、重启、状态
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('operation', type=str,
                                   help="required operation", location='json')
        super(Dns_bind, self).__init__()

    def post(self):
        """
        直接通过get进行操作，之后要附加验证方法
        """
        args = self.reqparse.parse_args()
        cmd = "service named " + args['operation']
        try:
            #执行一个shell命令子进程，
            oper = subprocess.check_output(cmd, shell=True)
            print oper
            return {"message" : "operate successed: " + oper}, 200
        except subprocess.CalledProcessError, e:
            return {"message" : "operate failed:" + e.output}, 500

        