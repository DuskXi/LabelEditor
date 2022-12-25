import argparse

from api_server import Component
from env import Environment
from web_init import init_web
from web_server import ApiServer


def main(args):
    env = Environment({}, read_path=r"W:\work\training\dusk_v2_training_set")
    inited = init_web(env)
    api_server: ApiServer = inited[0]
    instantiated_components: list[Component] = inited[1]
    api_server.run()


def parse_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
