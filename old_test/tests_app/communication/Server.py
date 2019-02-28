# -*- coding: utf-8 -*-

import socket
from threading import *
import json

class Server(Thread):
    """docstring for Server."""
    def __init__(self, port=1111):
        Thread.__init__(self)
        self.port    = max(min(port, 65535), 1111)
        self.running = True
        self.clients = []
        self.motd    = "Welcome to this server\n"

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("",1111))
        while self.running:
            sock.listen(10)
            print("En écoute...")
            (clientsocket, (ip, port)) = sock.accept()
            newthread = ClientThread(self, ip, port, clientsocket)
            print("[+] Nouveau thread pour %s %s" % (ip, port))
            newthread.start()
            self.clients.append(newthread)

    def requestStop(self):
        self.running = False


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
            if len(r) != 0 :
                print("[RECEIVED]", str(r.decode("utf-8")))
                self.clientsocket.send(r)
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
    serverthread = Server()
    serverthread.start()
