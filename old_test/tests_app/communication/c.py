#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time
import json
from threading import *

class Client(Thread):
    def __init__(self, ip:str, port:int):
        Thread.__init__(self)
        self.ip         = ip
        self.port       = port
        self.running    = False
        self.socket     = None
        print("[LOG] running thread @ %s %s" % (self.ip, self.port))

    def run(self):
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.ip, self.port))
        except ConnectionRefusedError as e:
            print("Could not connect to", self.ip, self.port)
            self.running  = False
        else:
            print("Connected to",self.ip)
            while(self.running):
                r = self.socket.recv(2048)
                if len(r) != 0 :
                    if str(r.decode("utf-8")).split(" ")[1] == "/exit":
                        self.running = False
                    else :
                        print(str(r.decode("utf-8")), sep="")
            print("Disconnected.")

    def send_str(self, data):
        """Documentation for send_str"""
        if type(data) == str:
            self.socket.send(bytes(data, 'utf-8'))
        else:
            raise TypeError("In send_str(data), type(data) : str expected, got", type(data))

    def send_dict(self, data):
        """Documentation for send_dict"""
        if type(data) == dict:
            print(self.socket)
            self.socket.send(bytes(json.dumps(data), 'utf-8'))
        else:
            raise TypeError("In send_dict(data), type(data) : dict expected, got", type(data))

    def request_stop(self):
        self.running = False


if __name__ == """__main__""":
    print("Broadcast from server :")
    c = Client("localhost", 1111)
    c.start()
    time.sleep(1)
    d = {"command": "/exit"}
    c.send_dict(d)

    # running = True
    # while running:
    #     rin = input("[>] ")
    #     c.socket.send(bytes("[Client2] " + rin, 'utf-8'))
    #     if rin == "/exit":
    #         running = False
    #         c.socket.send(bytes("[_DisconnectRequest_]", 'utf-8'))
    # c.join()
