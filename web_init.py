from api_server import *
from env import Environment
from web_server import ApiServer

components = [Files, Image, FileWords, ImageBase64, Save, Index]


def init_web(env: Environment) -> tuple[ApiServer, list[Component]]:
    api_server = ApiServer()
    instantiated_components = []
    for componentClass in components:
        _component = componentClass(env)
        instantiated_components.append(_component)
        api_server.register(_component.url, _component.view, _component.methods)
    return api_server, instantiated_components
