#-*— coding:utf-8 -*-

import subprocess
from flask_restful import Resource, reqparse

#配置文件的绝对路径
CHECK_CONF = '/etc/named.conf'

class Check_conf(Resource):
    """
    检查配置文件
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Check_conf, self).__init__()

    def get(self):
        """
        直接通过get进行操作，之后要附加验证方法
        """
        cmd = 'named-checkconf'

        try:
            #执行一个shell命令子进程，
            oper = subprocess.check_output(cmd, shell=True)
            print oper
            return {"message" : "operate successed"}, 200
        except subprocess.CalledProcessError, e:
            print "Error Output:" + e.output[:-1]
            return {"message" : e.output}, 500

        