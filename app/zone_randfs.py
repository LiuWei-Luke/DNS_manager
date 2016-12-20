#-*- coding:utf-8 -*-

import subprocess
from flask_restful import Resource, reqparse

help_msg = """
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

#操作指令集，r:重新载入 a:添加一个zone n:发送notify d:移除zone f:刷新 s:显示状态
OPERATIONS = ['r', 'a', 'n', 'd', 'f', 's']

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
        self.reqparse.add_argument('zone', type=str, location='json', required=True,
                                   help='required zone name')
        self.reqparse.add_argument('file', type=str, location='json', required=True,
                                   help='required zone file name')
        super(Zone_randfs, self).__init__()

    def post(self):
        """
        post方法
        """
        args = self.reqparse.parse_args()
        oper = args['oper']
        zone = args['zone']
        zone_file = args['file']

        return execute_operation(oper, zone, zone_file)


def execute_operation(o_type, zone, zone_file):
    """
    根据操作类型进行操作
    """
    # 重新读取配置文件以及zone
    # 分别执行rndc的freeze, reload, thaw命令
    if o_type == 'r':
        print 'r'
        try:
            p = subprocess.Popen(["rndc", "freeze", "test.com"], stdout=subprocess.PIPE, bufsize=1)
            with p.stdout:
                for line in iter(p.stdout.readline, b''):
                    print line
            p.wait()
            try:
                re = subprocess.check_output('rndc reload ' + zone, shell=True)
                print re
                try:
                    th = subprocess.check_output('rndc thaw ' + zone, shell=True)
                    print th
                    return {'message' : "operation successed:" + th}, 200
                except subprocess.CalledProcessError, e:
                    print "Error Print:" + e.output
                    return {'message' : e.output}, 500
            except subprocess.CalledProcessError, e:
                print "Error Print:" + e.output
                return {'message' : e.output}, 500
        except subprocess.CalledProcessError, e:
            print "Error Print:" + e.output
            return {'message' : e.output}, 500
    elif o_type == 'a':
        print 'a'
    elif o_type == 'n':
        print 'n'
    elif o_type == 'd':
        print 'd'
    elif o_type == 'f':
        print 'f'
    elif o_type == 's':
        print 's'
    else:
        return {'error' : 'illegal operation', 'message' : help_msg}, 400
