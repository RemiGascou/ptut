#!/usr/bin/env python3
from scapy.layers.inet import TCP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sniff
import os
import sys

nbPackets=0

WordsInteresting=["user","username","login","password","pass","mdp","access","authorization","token"]

class HttpPacket:
    def __init__(self, macdest, macori, header):
        self.ori = macori
        self.dst = macdest
        tab = filter(None, header.split("\\r\\n"))
        body = False
        self.headers = []
        self.body = []
        for h in tab:
            if body:
                self.body.append(h)
            else:
                self.headers.append(h)
                if str(h).startswith('Content-Length'):
                    body = True

    def __repr__(self):
        return "Http " + self.ori + " => " + self.dst + " { " + self.headers.__str__() + " }, {" + self.body.__str__() + "}"

    def __str__(self):
        return "Http " + self.ori + " => " + self.dst + " { " + self.headers.__str__() + " }, {" + self.body.__str__() + "}"

def isCredentials(text):
    global WordsInteresting
    for word in WordsInteresting:
        if word.lower() in text.lower():
            return True
    return False

def pkt_count(pkt):
  global nbPackets
  print("\rNombre de paquets Http : "+str(nbPackets),end="")
  nbPackets+=1

def show(interesting):
  elmt="".join(interesting)
  if (type(elmt) != bytes):
    print("\x1b[92m\nDATA : \x1b[90m : \x1b[91m"+elmt+"\x1b[90m\n")
  

def packet_callbak(pkt):
  pkt_count(pkt)
  if TCP in pkt:
    http = HttpPacket(pkt[0][Ether].dst, pkt[0][Ether].src, str(pkt[0][TCP].payload))
    data = None
    for header in http.headers:
      if (isCredentials(header)):
        data=header
        show(header)
    for body in http.body:
      if (isCredentials(body)):
        data=header
        show(body)
    if data is not None:
      print("".join(http.headers[0]))


def main():
  global WordsInteresting
  if os.getuid()==0:
    if (len(sys.argv)==1):
      sniff(iface="wlo1", filter='tcp',  prn=packet_callbak)
    else:
      WordsInteresting=sys.argv
      WordsInteresting.pop(0)     
      sniff(iface="wlo1", filter='tcp',  prn=packet_callbak)
  else:
    print("Please use it as root or use sudo")

if __name__ == '__main__':
    main()
