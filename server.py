from RevShell import Server
from argparse import ArgumentParser

if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('--port', '-p', type=int, default=58777)
    args = p.parse_args()
    server = Server(port=args.port)
    server.listen()
    server.accept()
    exit(0)