import asyncio

from . import *


class FileWords(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/filewords', 'filewords', ['GET'])
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

    async def view(self):
        file_name = request.args.get('filename', '')
        load_all = request.args.get('all', False)
        path = self.env.read_path
        if load_all:
            list_file = os.listdir(path)
            list_file = list(filter(lambda x: x.endswith('.png') or x.endswith('.jpg') or x.endswith('.txt'), list_file))
            filename_list = []
            tasks = []
            for file in list_file:
                if file.endswith('.png') or file.endswith('.jpg'):
                    filename = re.sub(r'\.[^.]*$', '', file)
                    fw_name = f"{filename}.txt"
                    if fw_name in list_file:
                        filename_list.append(filename)
                        tasks.append(self.readfile(os.path.join(path, fw_name)))
            results = await asyncio.gather(*tasks)
            return {"filewords": {filename_list[i]: results[i] for i in range(len(results))}}
        else:
            if not file_name.endswith('.txt'):
                return self.status_404()
            file_path = os.path.join(path, file_name)
            if not os.path.exists(file_path):
                return self.status_404()
            return await self.readfile(file_path)
