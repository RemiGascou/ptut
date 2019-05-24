# -*- coding: utf-8 -*-
"""
Plotting data sets
"""

import json
import matplotlib.pyplot as plt
import sys

########## Fonction pour afficher pour chaque capteurs un graphique avec les données normales et anormales ##########
def plot_compare(normal_datafile,anomaly_datafile):
    # Récupération des valeurs dans les fichiers
    f = open(normal_datafile, "r")
    normal_data = [json.loads(line) for line in f.readlines()]
    f = open(anomaly_datafile, "r")
    anomaly_data = [json.loads(line) for line in f.readlines()]
    f.close()

    # Lecture des données normales
    normal_light, normal_sound, normal_temp_object, normal_temp_ambient = [], [], [], []
    for d in normal_data:
        normal_light.append(d["light"])
        normal_sound.append(d["sound"])
        normal_temp_object.append(d["temp"]["object"])
        normal_temp_ambient.append(d["temp"]["ambient"])

    # Lecture des données anormales
    abnormal_light, abnormal_sound, abnormal_temp_object, abnormal_temp_ambient = [], [], [], []
    for d in anomaly_data:
        abnormal_light.append(d["light"])
        abnormal_sound.append(d["sound"])
        abnormal_temp_object.append(d["temp"]["object"])
        abnormal_temp_ambient.append(d["temp"]["ambient"])

    # Affichage des données
    plt.figure(1,figsize=(10, 8))

    plt.subplot(221)
    plt.plot(normal_light,label="normal")
    plt.plot(abnormal_light,label="abnormal")
    plt.title("light")
    plt.legend()

    plt.subplot(222)
    plt.plot(normal_sound,label="normal")
    plt.plot(abnormal_sound,label="abnormal")
    plt.title("sound")
    plt.legend()

    plt.subplot(223)
    plt.plot(normal_temp_object,label="normal")
    plt.plot(abnormal_temp_object,label="abnormal")
    plt.title("temp object")
    plt.legend()

    plt.subplot(224)
    plt.plot(normal_temp_ambient,label="normal")
    plt.plot(abnormal_temp_ambient,label="abnormal")
    plt.title("temp ambient")
    plt.legend()

    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.5, wspace=0.5)
    plt.show()


if __name__ == '__main__':
########## Affichage sur un même graphique des données de tous les capteurs ##########
    if len(sys.argv) == 2:
        datafile = sys.argv[1]
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

    ########## Affichage de 2 data sets avec un graphique par capteur ##########
    elif len(sys.argv) == 3:
        plot_compare(sys.argv[1],sys.argv[2])
    else:
        print("Usage: python3",sys.argv[0],"datafile.json")
        print("OR")
        print("Usage: python3",sys.argv[0],"normaldatafile.json","abnormaldatafile.json")
