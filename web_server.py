from flask import Flask


class ApiServer:
    def __init__(self, static_url_path='', static_folder="public"):
        self.app = Flask(__name__,
                         static_url_path='',
                         static_folder=static_folder)

    def run(self):
        self.app.run()

    def register(self, path, func):
        self.app.add_url_rule(path, view_func=func)
