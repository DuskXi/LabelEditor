import asyncio
import json

from . import *


class Save(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/save', 'save', ['POST'])
        self.env = env

    @staticmethod
    def status_404():
        resp = make_response("file not found", 400)
        resp.headers['X-Something'] = 'A value'
        return resp

    @staticmethod
    async def readfile(path):
        with open(path, 'r') as f:
            return f.read()

    @staticmethod
    def writefile(path, content):
        with open(path, 'w') as f:
            f.write(content)

    async def view(self):
        json_data = request.get_json()
        print(json_data)
        changes = json_data['data']
        for change in changes:
            filewords_filename = change[1]['filewordsName']
            filewords_filepath = os.path.join(self.env.read_path, filewords_filename)
            filewords = change[1]['filewords']
            self.writefile(filewords_filepath, filewords)
        print(f"Saved {len(changes)} files")
        return {"status": "ok"}
