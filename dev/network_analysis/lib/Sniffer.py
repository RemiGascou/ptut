#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Sniffer
# Author             : Remi GASCOU
# Date created       :
# Date last modified :
# Python Version     : 3.*

from scapy.all import IP, sniff
from lib import *


class Sniffer(object):
    """docstring for Sniffer."""
    def __init__(self):
        super(Sniffer, self).__init__()
        self.infos_tcp = TCP_Infos()

    def packet_handler(self, pkt):
        """ Documentation for packet_handler
            This is where you will call your classes for measurements.
        """
        if pkt.haslayer(TCP):
            self.infos_tcp.update(pkt)
        elif pkt.haslayer(TCP):
            pass
        return

    def sniff(self, iface="", filter="", store=0):
        """ Documentation for sniff
            This is an overlay for scapy
        """
        try:
            sniff(
                iface   = iface,
                filter  = filter,
                prn     = self.packet_handler,
                store   = store
            )
            print("\r", end="")
            print("[***] Exit requested... ")
            # Write logs ...
            print("\r[***] Exiting")
        except OSError as e:
            print("[OSError] No Such Device "+iface)


if __name__ == '__main__':
    pass
