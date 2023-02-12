import argparse

from tkinter import filedialog
from tkinter import Tk

from api_server import Component
from env import Environment
from web_init import init_web
from web_server import ApiServer


def main(args):
    read_path = args.dest
    if read_path is None:
        root = Tk()
        root.withdraw()
        read_path = filedialog.askdirectory()
        root.destroy()
        if read_path == "":
            print("No directory selected")
            return
    env = Environment({}, read_path=read_path)
    inited = init_web(env, args.quasarbuild)
    api_server: ApiServer = inited[0]
    instantiated_components: list[Component] = inited[1]
    api_server.run(host=args.host, port=args.port)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--dest", type=str, default=None)
    parser.add_argument("--quasarbuild", type=str, default="public/dist/spa")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
