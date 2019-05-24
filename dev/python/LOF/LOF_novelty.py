# -*- coding: utf-8 -*-
"""
NOVELTY DETECTION WITH LOF
version 1.3
"""
import time
import json
import numpy as np
from sklearn.neighbors import LocalOutlierFactor

# Mesure du temps d'exécution du programme
exetime = time.time()

########## Récupération des valeurs dans les fichiers ##########
datafile = "../data/sensornormal10000.json" #10000 entrées dans la range des capteurs au repos
f = open(datafile, "r")
data_sensor10000 = [json.loads(line) for line in f.readlines()]

datafile = "../data/sensornormal500000.json" #500000 entrées dans la range des capteurs au repos
f = open(datafile, "r")
data_sensor500000 = [json.loads(line) for line in f.readlines()]

datafile = "../data/9outlier.json" # 100 entrées (entre 0 et 10, 9 outliers entre 50 et 60 )
f = open(datafile, "r")
data_9outlier = [json.loads(line) for line in f.readlines()]

datafile = "../data/20outlier.json" # 100 entrées (entre 0 et 10, 20 outliers entre 50 et 60 )
f = open(datafile, "r")
data_20outlier = [json.loads(line) for line in f.readlines()]

datafile = "../data/40outlier.json" # 100 entrées (entre 0 et 10, 40 outliers entre 50 et 60 )
f = open(datafile, "r")
data_40outlier = [json.loads(line) for line in f.readlines()]

# 6 outliers sur une population de 1000
#les indices des outliers sont (en partant de 0) : 41 , 206, 316, 455, 565, 748
datafile = "../data/outlier.json" 
f = open(datafile, "r")
data_outlier = [json.loads(line) for line in f.readlines()]

datafile = "../data/normalsimple100A.json" #100 entrée (entre 0 et 10)
f = open(datafile, "r")
data_normal100A = [json.loads(line) for line in f.readlines()]

datafile = "../data/normalsimple100B.json" #100 entrées (entre 0 et 10)
f = open(datafile, "r")
data_normal100B = [json.loads(line) for line in f.readlines()]

datafile = "../data/normalsimple1000.json" #1000 entrées (entre 0 et 10)
f = open(datafile, "r")
data_normal1000 = [json.loads(line) for line in f.readlines()]

datafile = "../data/normalsimple10000.json" #10 000 entrées (entre 0 et 10)
f = open(datafile, "r")
data_normal10000 = [json.loads(line) for line in f.readlines()]

datafile = "../data/normalsimple100000.json" #100 000 entrée (entre 0 et 10)
f = open(datafile, "r")
data_normal100000 = [json.loads(line) for line in f.readlines()]

datafile = "../data/normalsimple500000.json" #500 000 entrée (entre 0 et 10)
f = open(datafile, "r")
data_normal500000 = [json.loads(line) for line in f.readlines()]


f.close()

########## Formalisation des données ###########
# Lecture des données pour l'apprentissage et création d'une liste pour chaque capteur
def array_data(data_input):
    list_light, list_sound, list_temp_object, list_temp_ambient = [], [], [], []
    for d in data_input:
        list_light.append(d["light"])
        list_sound.append(d["sound"])
        list_temp_object.append(d["temp"]["object"])
        list_temp_ambient.append(d["temp"]["ambient"])
    # Conversion des listes en tableaux numpy
    light = np.array(list_light)
    sound = np.array(list_sound)
    temp_object = np.array(list_temp_object)
    temp_ambient = np.array(list_temp_ambient)

    # Création d'un seul tableau (1000 listes de 4 valeurs) avec les valeurs des capteurs
    python_array = np.zeros([4])

    for index in range (0, len(light)):
        python_list = []
        python_list.append(light[index])
        python_list.append(sound[index])
        python_list.append(temp_object[index])
        python_list.append(temp_ambient[index])
        python_array = np.vstack((python_array, python_list)) 
    data = np.delete(python_array, (0), axis=0)
    return data

  
######### LOF novelty detection ##########
    # fit the model
def LOF_novelty(data_train, data_test, n_neighbors=2): 
    train = array_data(data_train)
    test = array_data(data_test)
    lof = LocalOutlierFactor(n_neighbors, metric = "cityblock", novelty=True)
    lof.fit(train)
    result = lof.predict(test)
    return (result)

######## Tests #########
lof1=LOF_novelty(data_normal500000, data_40outlier, n_neighbors = 6)
nb_outliers1 = (lof1==-1).sum()
print("nombre d'outliers trouvés=",nb_outliers1) #affiche le nombre d'outliers détectés

for index, value in enumerate(lof1):
    if value == -1:
        print ("Outlier index :", index, "\n") #affiche l'index des points identifiés comme outliers

######### Affichage du temps d'exécution ##########
print("Temps d execution : %s secondes ---" % (time.time() - exetime))