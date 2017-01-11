#-*- coding:utf-8 -*-

import subprocess
import os
from flask_restful import Resource, reqparse
from flask import request

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
                    msg += '添加完成'
        else:
            with p_a.stderr:
                for line in iter(p_a.stderr.readline, b''):
                    print line
                    msg += line
            return {'message' : 'addzone failed:' + msg}, 500

        '''
        添加完成自动重置一次服务
        '''
        cmd = 'reload ' + zone
        p_r = subprocess.Popen(["rndc", cmd], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, bufsize=1)
        p_r.wait()
        if p_r.returncode == 0:
            with p_r.stdout:
                for line in iter(p_r.stdout.readline, b''):
                    print line
                    msg += line
                return {'message' : '服务重置成功' + msg}, 200
        else:
            with p_r.stderr:
                for line in iter(p_r.stderr.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 500

class Zone(Resource):
    '''
    指定域名的操作，包括删除，查看，修改
    '''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('conf', type=dict, location='json')
        super(Zone, self).__init__()

    def get(self, zone):
        '''
        查看给定域名的配置文件
        '''
        msg = ''
        f_path = '/var/named/' + zone + '.zone'

        try:
            with open(f_path) as f:
                for line in f.readlines():
                    msg += line
            return {'message' : msg}, 200
        except IOError as err:
            return {'message' : err}, 500

    def put(self, zone):
        '''
        更新指定域名的配置文件
        '''
        msg = ''

        args = self.reqparse.parse_args()
        conf = args['conf']
        m_ip = conf['ip']
        if not m_ip:
            return {'message' : '参数错误'}, 403

        m_domain = conf['domain']
        if not m_domain:
            return {'message' : '参数错误'}, 403

        #存储文件的每行内容
        list_content = []
        try:
            with open('/var/named/' + zone + '.zone') as f:
                for l in f.readlines():
                    list_content.append(l)
        except IOError as err:
            return {"message" : "文件读取失败," + str(err)}, 500

        #要修改的内容只从第九行开始
        list_content_after = list_content[8:]

        #有相同的域名就替换，没有就添加
        for i in range(len(list_content_after)):
            if m_domain in list_content_after[i]:
                list_content_after[i] = m_domain + "\tIN\tA\t" + m_ip + '\n'
                break
            if i+1 == len(list_content_after):
                list_content_after.append(m_domain + "\tIN\tA\t" + m_ip + '\n')
        #重新拼接文件
        list_content_complete = list_content[:8] + list_content_after

        #写入文件，此处写入是重新创建了个文件，权限并没有改变
        try:
            with open('/var/named/' + zone + '.zone', "w") as f:
                f.writelines(list_content_complete)
            msg += "修改成功"
        except IOError as err:
            return {"message" : "文件写入失败," + str(err)}, 500

        '''
        重新加载域名文件
        '''
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

    def delete(self, zone):
        '''
        从记录中删除服务的记录
        '''
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

class Zone_list(Resource):
    '''
    查看当前解析域名列表
    '''
    def __init__(self):
        super(Zone_list, self).__init__()

    def get(self):
        msg = '列表获取成功'
        domain_list = []

        for f in os.listdir("/var/named/"):
            if f.endswith(".nzf"):
                f_name = "/var/named/" + f
        try:
            with open(f_name) as text:
                for line in text.readlines():
                    print line
                    domain_list.append(line)
            return {'message' : msg, 'list' : domain_list}, 200
        except IOError as err:
            return {'message' : err}, 200
