import logging

from flask import Flask
from flask_cors import CORS, cross_origin


class ApiServer:
    def __init__(self, static_url_path='', static_folder="public/dist/spa"):
        self.app = Flask(__name__,
                         static_url_path='',
                         static_folder=static_folder)
        self.app.config['JSON_AS_ASCII'] = False
        cors = CORS(self.app)
        self.app.config['CORS_HEADERS'] = 'Content-Type'
        log = logging.getLogger('werkzeug')
        log.disabled = True

    def run(self):
        self.app.run(threaded=True)

    def register(self, path, func, methods=['GET']):
        func.__func__.__name__ += path
        self.app.add_url_rule(path, view_func=func, methods=methods)
