#-*- coding:utf-8 -*-
from flask_restful import Resource
from flask import send_from_directory
import sys,os
import subprocess

class Download(Resource):
    '''
    备份文件下载
    '''
    def __init__(self):
        super(Download, self).__init__()

    def get(self, filename):
        if os.path.isfile(os.path.join('/home/backups/', filename)):
            return send_from_directory('/home/backups/', filename, as_attachment=True)
        else:
            return {'message' : '没有指定文件'}, 404

class Backup(Resource):
    '''
    对文件进行备份
    '''
    def __init__(self):
        super(Backup, self).__init__()

    def get(self):
        path = os.path.abspath(os.path.join(sys.path[0], os.pardir))
        path = path + '/bin/backup_zone.sh'
        p = subprocess.Popen([path], stdout=subprocess.PIPE, bufsize=1)
        p.wait()
        if p.returncode == 0:
            with p.stdout:
                for line in iter(p.stdout.readline, b''):
                    print line
            return send_from_directory('/home/backups/', 'zone.tar.gz', as_attachment=True)

