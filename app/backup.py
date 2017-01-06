#-*- coding:utf-8 -*-
from flask_restful import Resource
from flask import send_from_directory
import os
import subprocess

class Download(Resource):
    '''
    备份文件下载
    '''
    def __init__(self):
        super(Download, self).__init__()

    def get(self, filename):
        if os.path.isfile(os.path.join('/root/backups/', filename)):
            return send_from_directory('/root/backups/', filename, as_attachment=True)
        else:
            return {'message' : '没有指定文件'}, 404

class Backup(Resource):
    '''
    对文件进行备份
    '''
    def __init__(self):
        super(Backup, self).__init__()

    def get(self):
        msg = ''
        p = subprocess.Popen(['/root/hone/DNS_manager/bin/backup_zone.sh'],
                             stdout=subprocess.PIPE, bufsize=1)
        p.wait()
        if p.returncode == 0:
            with p.stdout:
                for line in iter(p.stdout.readline, b''):
                    print line
                    msg += line
            return {'message' : msg}, 200

