#-*— coding:utf-8 -*-

import subprocess
from flask_restful import Resource, reqparse
from flask import request

class Dns_named(Resource):
    """
    bind接口，负责DNS服务的启动、关闭、重启、状态
    """
    def __init__(self):
        self.oper = request.args.get('oper')
        super(Dns_named, self).__init__()

    def get(self):
        """
        直接通过get进行操作，之后要附加验证方法
        """
        cmd = "service named " + self.oper
        try:
            #执行一个shell命令子进程，
            oper = subprocess.check_output(cmd, shell=True)
            print oper
            return {"message" : "operate successed: " + oper}, 200
        except subprocess.CalledProcessError, e:
            return {"message" : "operate failed:" + e.output}, 500

        