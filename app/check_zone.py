#-*— coding:utf-8 -*-

import subprocess
from flask_restful import Resource, reqparse

#配置文件的绝对路径
CHECK_ZONE = '/var/named/'

class Check_zone(Resource):
    """
    bind接口，负责DNS服务的启动、关闭、重启、状态
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('domain', type=str, required=True,
                                   help='required domain name', location='json')
        super(Check_zone, self).__init__()

    def post(self):
        """
        直接通过get进行操作，之后要附加验证方法
        """
        args = self.reqparse.parse_args()
        domain = args['domain']
        #根据要检查的域名完成命令格式为：named-checkzone domain_name file_name
        cmd = 'named-checkzone ' + domain + ' ' + CHECK_ZONE + domain.append('.zone')

        try:
            #执行一个shell命令子进程，
            oper = subprocess.check_output(cmd, shell=True)
            print oper
            return {"message" : "operate successed", "result" : oper}, 200
        except subprocess.CalledProcessError, e:
            print "Error Output:" + e.output
            return {"error" : "operate failed", "output" : e.output}, 500

        