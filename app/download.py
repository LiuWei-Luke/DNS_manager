#-*- coding:utf-8 -*-

from flask_restful import Resource
from flask import send_from_directory
import os

class Download(Resource):
    def __init__(self):
        super(Download, self).__init__()

    def get(self, filename):
        if os.path.isfile(os.path.join('/root/backups/', filename)):
            return send_from_directory('/root/backups/', filename, as_attachment=True)
        else:
            return {'message' : '没有指定文件'}, 404
