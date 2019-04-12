# -*- coding: utf-8 -*-

import json
import matplotlib.pyplot as plt
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3",sys.argv[0],"datafile.json")
    else:
        datafile    = sys.argv[1]
        # Read file
        f = open(datafile, "r")
        data = [json.loads(line) for line in f.readlines()]
        f.close()

        list_light, list_sound, list_temp_object, list_temp_ambient = [], [], [], []

        for d in data:
            list_light.append(d["light"])
            list_sound.append(d["sound"])
            list_temp_object.append(d["temp"]["object"])
            list_temp_ambient.append(d["temp"]["ambient"])

        for list_y in [list_light, list_sound, list_temp_object, list_temp_ambient]:
            plt.plot(list(range(len(list_y))), list_y)

        plt.show()
