from RevShell import Server

def main(args):
    server = ReverseShellServer()
    server.create(args.port)
    server.bind()
    server.accept()
    print('[*] Returned from SocketAccept')
    return 0

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('--port', '-p', type=int, default=58777)
    args = p.parse_args()
    code = main(args)
    exit(code)