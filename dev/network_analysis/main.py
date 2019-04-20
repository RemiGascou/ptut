#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : main.py
# Author             : Remi GASCOU
# Date created       : 20 april 2019
# Date last modified : 20 april 2019
# Python Version     : 3.*

import os, sys

def welcome(interface):
    print("".center(80,"="))
    print(" | ")
    print(" | Using interface : ",interface)
    print("".center(80,"="))
    print()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage : sudo python3 "+sys.argv[0]+" interface")
    else :
        if os.getuid() != 0:
            print("[warn] Could not run script. Try to run this script with sudo.")
        else:
            interface = sys.argv[1]
            welcome(interface)

            from lib import *
            Sniffer().sniff(iface=interface)
