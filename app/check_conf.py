#-*— coding:utf-8 -*-

import subprocess
from flask_restful import Resource, reqparse

#配置文件的绝对路径
CHECK_CONF = '/etc/named.conf'

class Check_conf(Resource):
    """
    bind接口，负责DNS服务的启动、关闭、重启、状态
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Check_conf, self).__init__()

    def post(self):
        """
        直接通过get进行操作，之后要附加验证方法
        """
        cmd = 'named-checkconf'

        try:
            #执行一个shell命令子进程，
            oper = subprocess.check_output(cmd, shell=True)
            return {"message" : "operate successed", "result" : oper}, 200
        except subprocess.CalledProcessError, e:
            print "Error Output:" + e.output[:-1]
            return {"error" : "operate failed", "output" : e.output}, 500

        