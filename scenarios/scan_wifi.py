#!/usr/bin/env python3

from scapy.all import *
import os

ActualName={}

def monitorMode(iface="wlo1",mode=True):
  toMode=""
  if mode==True:
    toMode="monitor"
  else:
    toMode="managed"
  os.system('ifconfig ' + iface + ' down')
  os.system('iwconfig ' + iface + ' mode '+toMode)
  os.system('ifconfig ' + iface + ' up')
  if (mode==False):
    os.system('service network-manager restart')


def setChannel(channel,iface="wlo1"):
  chan=channel % 12
  os.system("iwconfig "+iface+" channel "+str(chan))
  print("[+] Sniffing on channel " + str(chan))


def sendBeaconFrame(iface="wlo1"):
  dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff',addr2="ff:ff:ff:ff:ff:ff",addr3="ff:ff:ff:ff:ff:ff")
  frame = RadioTap()/dot11/Dot11Beacon()
  sendp(frame, iface=iface)

def handle_packet(pkt):
  global ActualName
  data=None
  if pkt.haslayer(Dot11ProbeResp):
    data=pkt[Dot11ProbeResp][Dot11Elt]
  if data is not None:
    if data.ID == 0:
      decodeName=data.info.decode("utf-8")
      ActualName[decodeName]=pkt.addr2
      if decodeName=="MartinRouterKing":
        print("MartinRouterKing : "+pkt.addr2)

def main():
  monitorMode(iface="wlo1",mode=True)
  sniff(iface="wlo1", prn=handle_packet)
  monitorMode(iface="wlo1",mode=False)
  print(ActualName)
  
if __name__ == '__main__':
  main()
