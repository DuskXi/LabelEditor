from . import *


class Image(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/image', 'image', ['GET'])
        self.env = env

    @staticmethod
    def status_404():
        resp = make_response("image not found", 400)
        resp.headers['X-Something'] = 'A value'
        return resp

    def view(self):
        image_name = request.args.get('image', '')
        if not image_name.endswith('.png') and not image_name.endswith('.jpg'):
            return self.status_404()
        path = self.env.read_path
        image_path = os.path.join(path, image_name)
        if not os.path.exists(image_path):
            return self.status_404()
        return send_file(image_path)
