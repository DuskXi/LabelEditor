import argparse

from api_server import Component
from env import Environment
from web_init import init_web
from web_server import ApiServer


def main(args):
    env = Environment({}, read_path=r"W:\work\training\skadi_v2_768_training_set")
    inited = init_web(env, args.quasarbuild)
    api_server: ApiServer = inited[0]
    instantiated_components: list[Component] = inited[1]
    api_server.run(host=args.host, port=args.port)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--quasarbuild", type=str, default="public/dist/spa")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
