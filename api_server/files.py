from . import *


class Files(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/files', 'files', ['GET'])
        self.env = env

    def view(self):
        path = self.env.read_path
        list_file = os.listdir(path)
        list_file = list(filter(lambda x: x.endswith('.png') or x.endswith('.jpg') or x.endswith('.txt'), list_file))
        pairs = []
        for file in list_file:
            if file.endswith('.png') or file.endswith('.jpg'):
                filename = re.sub(r'\.[^.]*$', '', file)
                fw_name = f"{filename}.txt"
                if fw_name in list_file:
                    pairs.append((file, fw_name))
        return {"files": pairs}
