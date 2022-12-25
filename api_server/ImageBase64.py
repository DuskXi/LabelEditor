import base64
from io import BytesIO

from . import *
from PIL import Image as PImage


class ImageBase64(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/imageBase64', 'imageBase64', ['GET'])
        self.env = env

    @staticmethod
    def status_404():
        resp = make_response("image not found", 400)
        resp.headers['X-Something'] = 'A value'
        return resp

    @staticmethod
    async def load_png_base64(path, width=512, height=512):
        image = PImage.open(path)
        image = image.resize((width, height), PImage.ANTIALIAS)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return f"data:image/png;base64,{img_str.decode('utf-8')}"

    async def view(self):
        image_name = request.args.get('image', '')
        all_read = request.args.get('all', False)
        width = int(request.args.get('width', 512))
        height = int(request.args.get('height', 512))
        path = self.env.read_path
        if all_read:
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
                        tasks.append(self.load_png_base64(os.path.join(path, file), width, height))
            results = await asyncio.gather(*tasks)
            return {"allImageBase64": {filename_list[i]: results[i] for i in range(len(results))}}
        else:
            if not image_name.endswith('.png') and not image_name.endswith('.jpg'):
                return self.status_404()
            image_path = os.path.join(path, image_name)
            if not os.path.exists(image_path):
                return self.status_404()
            return {"imageBase64": await self.load_png_base64(image_path, width, height)}
