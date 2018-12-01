# -*- coding: utf-8 -*-

import socket
from threading import *
import json

class ClientThread(Thread):
    """docstring for ClientThread."""
    def __init__(self, parent_server:Server, ip, port, clientsocket):
        Thread.__init__(self)
        self.parent_server  = parent_server
        self.ip             = ip
        self.port           = port
        self.clientsocket   = clientsocket

    def run(self):
        print("Connection de %s %s" % (self.ip, self.port))
        r = bytes("", 'utf-8')
        self.clientsocket.send(bytes("Client to server : Connected", 'utf-8'))
        while (r != bytes("[_DisconnectRequest_]", 'utf-8')):
            r = self.clientsocket.recv(2048)
            if len(r) != 0 : self.clientsocket.send(r)
            #for c in self.parent_server.clients: #Of Server
            #    c.clientsocket.send(r)
            #self.clientsocket.send(bytes(r, 'utf-8'))
        print("Client déconnecté...")

    def orun(self):
        print("Connection de %s %s" % (self.ip, self.port))
        #r = self.clientsocket.recv(2048)
        mystring = "Hello <3"
        print("Sending welcome")
        self.clientsocket.send(bytes(mystring, 'utf-8'))
        print("Client déconnecté...")

if __name__ == '__main__':
    main()
