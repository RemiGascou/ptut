#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : TELNET_Infos.py
# Author             : Remi GASCOU
# Date created       : 20 april 2019
# Date last modified : 20 april 2019
# Python Version     : 3.*


# from scapy.all import Telnet

class TELNET_Infos(object):
    """docstring for TELNET_Infos."""
    def __init__(self):
        super(TELNET_Infos, self).__init__()
        self.data = {
            "total"  : 0
        }

    def update(self, pkt):
        """ Documentation for update
            Update your measures with packet pkt
        """
        self.data["total"] += 1
        # ======================================
        # ======================================
        return None

    def clear_data(self):
        self.data = {
            "total"  : 0,
        }
