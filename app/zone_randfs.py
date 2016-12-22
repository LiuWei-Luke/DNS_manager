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
        msg = ''
        cmd = 'freeze ' + zone
        #开始执行freeze进程
        p_f = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        p_f.wait()
        if p_f.returncode == 0:
            with p_f.stdout:
                for line in iter(p_f.stdout.readline, b''):
                    print line
                    msg += line
        else:
            with p_f.stdout:
                for line in iter(p_f.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500
        #开始执行reload进程
        cmd = 'reload ' + zone
        p_r = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE, bufsize=1)
        p_r.wait()
        if p_r.returncode == 0:
            with p_r.stdout:
                for line in iter(p_r.stdout.readline, b''):
                    print line
                    msg += line
        else:
            with p_r.stdout:
                for line in iter(p_r.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500
        #开始执行thaw进程
        cmd = 'thaw' + zone
        p_t = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE, bufsize=1)
        p_t.wait()
        if p_t.returncode == 0:
            with p_t.stdout:
                for line in iter(p_t.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 200
        else:
            with p_t.stdout:
                for line in iter(p_t.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500
    #执行addzone命令, rndc addzone zone '{type master; file "/var/named/zone_file";};'
    elif o_type == 'a':
        msg = ''
        cmd = 'addzone ' + zone + ' {type master; file "/var/named/' + zone_file + '";};'
        p = subprocess.Popen(['rndc', cmd], stdout=subprocess.PIPE, bufsize=1)
        p.wait()
        if p.returncode is 0:
            with p.stdout:
                for line in iter(p.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : 'addzone complete:' + msg}, 200
        else:
            with p.stdout:
                for line in iter(p.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : 'addzone failed:' + msg}, 500
    #执行notify命令，rndc notify zone IN view
    elif o_type == 'n':
        msg = ''
        cmd = 'notify ' + zone
        p = subprocess.Popen(['rndc', cmd], stdout=subprocess.PIPE, bufsize=1)
        p.wait()
        if p.returncode is 0:
            with p.stdout:
                for line in iter(p.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 200
        else:
            with p.stdout:
                for line in iter(p.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500
    #删除zone功能,进行freeze,thaw,delzone操作
    elif o_type == 'd':
        msg = ''
        cmd = 'freeze ' + zone
        p_f = subprocess.Popen(['rndc', cmd], stdout=subprocess.PIPE, bufsize=1)
        p_f.wait()
        if p_f.returncode == 0:
            with p_f.stdout:
                for line in iter(p_f.stdout.readline, b''):
                    print line
                    msg += line
        else:
            with p_f.stdout:
                for line in iter(p_f.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500

        cmd = 'thaw ' + zone
        p_t = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE, bufsize=1)
        p_t.wait()
        if p_t.returncode == 0:
            with p_t.stdout:
                for line in iter(p_t.stdout.readline, b''):
                    print line
                    msg += line
        else:
            with p_t.stdout:
                for line in iter(p_t.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500

        cmd = 'delzone ' + zone
        p_d = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE, bufsize=1)
        p_d.wait()
        if p_d.returncode == 0:
            with p_d.stdout:
                for line in iter(p_d.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : 'you have deleted ' + zone}, 200
        else:
            with p_d.stdout:
                for line in iter(p_d.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500
    #进行flush操作，没有包含指定view底下的刷新，只进行指定域名的刷新
    elif o_type == 'f':
        msg = ''
        cmd = 'flush'
        p_f = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE, bufsize=1)
        p_f.wait()
        if p_f.returncode == 0:
            with p_f.stdout:
                for line in iter(p_f.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : 'flush server\'s caches completed'}, 200
        else:
            with p_f.stdout:
                for line in iter(p_f.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : 'flush failed'}, 500
    #进行status操作，查看dns状态
    elif o_type == 's':
        msg = ''
        cmd = 'status'
        p_s = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE, bufsize=1)
        p_s.wait()
        if p_s.returncode == 0:
            with p_s.stdout:
                for line in iter(p_s.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 200
        else:
            with p_s.stdout:
                for line in iter(p_s.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500
    else:
        return {'error' : 'illegal operation', 'message' : help_msg}, 400
