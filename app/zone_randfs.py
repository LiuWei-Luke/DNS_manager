#-*- coding:utf-8 -*-

import subprocess
from flask_restful import Resource, reqparse

class Zone_status(Resource):
    '''
    查看服务状态
    '''
    def __init__(self):
        super(Zone_status, self).__init__()

    def get(self):
        msg = ''
        cmd = 'status'
        p_s = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, bufsize=1)
        p_s.wait()
        if p_s.returncode == 0:
            with p_s.stdout:
                for line in iter(p_s.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 200
        else:
            with p_s.stderr:
                for line in iter(p_s.stderr.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500

class Zone_reload(Resource):
    '''
    重新加载配置
    '''
    def __init__(self):
        super(Zone_reload, self).__init__()

    def get(self, zone):
        msg = ''
        cmd = 'freeze ' + zone
        #开始执行freeze进程
        p_f = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, bufsize=1)
        p_f.wait()
        if p_f.returncode == 0:
            with p_f.stdout:
                for line in iter(p_f.stdout.readline, b''):
                    print line
                    msg += line
        else:
            with p_f.stderr:
                for line in iter(p_f.stderr.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500
        #开始执行reload进程
        cmd = 'reload ' + zone
        p_r = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, bufsize=1)
        p_r.wait()
        if p_r.returncode == 0:
            with p_r.stdout:
                for line in iter(p_r.stdout.readline, b''):
                    print line
                    msg += line
        else:
            with p_r.stderr:
                for line in iter(p_r.stderr.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500
        #开始执行thaw进程
        cmd = 'thaw ' + zone
        p_t = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, bufsize=1)
        p_t.wait()
        if p_t.returncode == 0:
            with p_t.stdout:
                for line in iter(p_t.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 200
        else:
            with p_t.stderr:
                for line in iter(p_t.stderr.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500

class Zone_flush(Resource):
    '''
    刷新域名缓存
    '''
    def __init__(self):
        super(Zone_flush, self).__init__()

    def get(self, zone):
        msg = ''
        if zone == 'all':
            cmd = 'flush'
            p_f = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, bufsize=1)
            p_f.wait()
            if p_f.returncode == 0:
                with p_f.stdout:
                    for line in iter(p_f.stdout.readline, b''):
                        print line
                        msg += line
                return {'message' : 'flush server\'s caches completed'}, 200
            else:
                with p_f.stderr:
                    for line in iter(p_f.stderr.readline, b''):
                        print line
                        msg += line
                return {'message' : 'flush failed'}, 500
        else:
            cmd = 'flushname ' + zone
            p_f = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, bufsize=1)
            p_f.wait()
            if p_f.returncode == 0:
                with p_f.stdout:
                    for line in iter(p_f.stdout.readline, b''):
                        print line
                        msg += line
                return {'message' : 'flush zone\'s caches completed'}, 200
            else:
                with p_f.stderr:
                    for line in iter(p_f.stderr.readline, b''):
                        print line
                        msg += line
                return {'message' : 'flush failed'}, 500

class Zone_add(Resource):
    '''
    添加域名
    '''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('zone', type=str, location='json',
                                   help='required zone name')
        super(Zone_add, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        zone = args["zone"]
        zone_file = zone + '.zone'
        msg = ''
        cmd = 'addzone ' + zone + ' {type master; file "/var/named/' + zone_file + '";};'
        p_a = subprocess.Popen(['rndc', cmd], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, bufsize=1)
        p_a.wait()
        if p_a.returncode is 0:
            with p_a.stdout:
                for line in iter(p_a.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : 'addzone complete:' + msg}, 200
        else:
            with p_a.stderr:
                for line in iter(p_a.stderr.readline, b''):
                    print line
                    msg += line
            return {'message' : 'addzone failed:' + msg}, 500

class Zone_delete(Resource):
    '''
    删除域名
    '''
    def __init__(self):
        super(Zone_delete, self).__init__(self)

    def get(self, zone):
        msg = ''
        cmd = 'freeze ' + zone
        p_f = subprocess.Popen(['rndc', cmd], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, bufsize=1)
        p_f.wait()
        if p_f.returncode == 0:
            with p_f.stdout:
                for line in iter(p_f.stdout.readline, b''):
                    print line
                    msg += line
        else:
            with p_f.stderr:
                for line in iter(p_f.stderr.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500

        cmd = 'thaw ' + zone
        p_t = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, bufsize=1)
        p_t.wait()
        if p_t.returncode == 0:
            with p_t.stdout:
                for line in iter(p_t.stdout.readline, b''):
                    print line
                    msg += line
        else:
            with p_t.stderr:
                for line in iter(p_t.stderr.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500

        cmd = 'delzone ' + zone
        p_d = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, bufsize=1)
        p_d.wait()
        if p_d.returncode == 0:
            with p_d.stdout:
                for line in iter(p_d.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : 'you have deleted ' + zone}, 200
        else:
            with p_d.stderr:
                for line in iter(p_d.stderr.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500

class Zone_notify(Resource):
    '''
    发送通知
    '''
    def __init__(self):
        super(Zone_notify, self).__init__()

    def get(self, zone):
        msg = ''
        cmd = 'notify ' + zone
        p_n = subprocess.Popen(['rndc', cmd], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, bufsize=1)
        p_n.wait()
        if p_n.returncode is 0:
            with p_n.stdout:
                for line in iter(p_n.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 200
        else:
            with p_n.stderr:
                for line in iter(p_n.stderr.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500
