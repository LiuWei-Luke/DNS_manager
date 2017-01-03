#-*— coding:utf-8 -*-

import subprocess
from flask_restful import Resource, reqparse
from flask import request

#配置文件的绝对路径
CHECK_ZONE = '/var/named/'

class Check_zone(Resource):
    """
    对域名文件进行检查
    """
    def __init__(self):
        super(Check_zone, self).__init__()

    def get(self, zone):
        """
        直接通过get进行操作，之后要附加验证方法
        """
        domain = zone

        #根据要检查的域名完成命令格式为：named-checkzone domain_name file_name
        cmd = 'named-checkzone ' + domain + ' ' + CHECK_ZONE + domain + ('.zone')

        try:
            #执行一个shell命令子进程，
            oper = subprocess.check_output(cmd, shell=True)
            print oper
            return {"message" : "operate successed:" + oper}, 200
        except subprocess.CalledProcessError, e:
            print "Error Output:" + e.output
            return {"error" : "operate failed:" + e.output}, 500

        