class Environment:
    def __init__(self, config, **kwargs):
        self.config = config
        self.read_path = kwargs.get('read_path', "")
