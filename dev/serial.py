# File name: serial.py
# Author: Remi GASCOU
# Date created: 04/05/2019
# Date last modified: 04/07/2019
# Python Version: 3.*

import matplotlib.pyplot as plt
import serial
import json


# def dyn_update(fig, p, y, ly, size=100):
#     lx = list(range(size))
#     ly = ly[1:] + [y]
#     while len(ly) != len(lx): ly = [0] + ly
#     p.set_xdata(lx)
#     p.set_ydata(ly)
#     plt.ylim(0, max(ly)+2)
#     plt.xlim(0, max(lx)+1)
#     fig.canvas.draw()
#     fig.canvas.flush_events()
#     return lx, ly

def dyn_update(fig, ax, y, ly, size=100, marker='', color="blue"):
    lx = list(range(size))
    ly = ly[1:] + [y]
    while len(ly) != len(lx): ly = [0] + ly
    ax.clear()
    ax.plot(lx, ly, marker=marker, color=color)
    ax.set_ylim(0, max(ly)+2)
    ax.set_xlim(0, max(lx)+1)
    return lx, ly


list_time = [0]
list_sound, list_light = [0], [0]


# Creates the objects for plot
plt.ion()
fig       = plt.figure()
ax_sound  = fig.add_subplot(2, 1, 1)
ax_light  = fig.add_subplot(2, 1, 2)

# Infinite loop to read and plot
xk = 0
ser = serial.Serial('COM4', 9600, timeout=1)
while True:
    ser.write(b"?\n")       # Asks the arduino for data
    line = ser.readline()   # Reads data
    try :
        d = json.loads(line)
        print(d)
        xk += 1
        # Updates the plot for sound sensor
        list_time, list_light = dyn_update(fig, ax_light, d["light"], list_light, color="red")
        # Updates the plot for light sensor
        list_time, list_sound = dyn_update(fig, ax_sound, d["sound"], list_sound, color="blue")
        # Refreshs the screen
        fig.canvas.draw()
        fig.canvas.flush_events()
    except Exception:
        pass
