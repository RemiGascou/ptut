# -*- coding: utf-8 -*-
"""
LOF algorithm, version 2.1

"""

import time
import numpy as np
import json
import pandas as pd
from scipy.spatial.distance import pdist, squareform

# Mesure du temps d'exécution du programme
exetime = time.time()


########## DATASETS ##########
datafile = "../data/sensornormal10000.json"
f = open(datafile, "r")
data_sensor10000 = [json.loads(line) for line in f.readlines()]

datafile = "../data/sensornormal500000.json"
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

datafile = "../data/9outlier1000.json" # 1000 entrées (entre 0 et 10, 9 outliers entre 50 et 60 )
f = open(datafile, "r")
data_9outlier1000 = [json.loads(line) for line in f.readlines()]

# 6 outliers sur une population de 1000
# les indices des outliers sont (en partant de 0) : 41 , 206, 316, 455, 565, 748
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
def array_data(dataset):
    python_array = np.zeros([4])
    # creation du tableau, chaque item = une entrée [light,sound,Tobj,Tamb]
    for element in dataset:
        list_python = []
        list_python.append(element["light"])
        list_python.append(element["sound"])
        list_python.append(element["temp"]["object"])
        list_python.append(element["temp"]["ambient"])
        python_array = np.vstack((python_array, list_python))
        data = np.delete(python_array, (0), axis=0) #retire la première entrée [0,0,0,0]
    return data
    


######### Algorithme LOF ############

#récupérer la reachdistance 
def reachdist(distance_df, observation, index):
    return distance_df[observation][index]

#LOF algorithm implementation
# distance metric euclidean (par défaut)
# k la population utilisée pour calculer le LOF (k=2 par défaut)
# Renvoie un dictionnaire qui associe à chaque entrée de donnée (key) son LOF (value)


def LOF_algorithm(data_input, k=2, distance_metric = "euclidean"):
    distances = pdist(data_input, distance_metric)
    dist_matrix = squareform(distances)
    distance_df = pd.DataFrame(dist_matrix)
    
    
    observations = distance_df.columns
    lrd_dict = {}
    n_dist_index = {}
    reach_array_dict = {}
    
    for observation in observations:
        dist = distance_df[observation].nsmallest(k+1).iloc[k]
        indexes = distance_df[distance_df[observation] <= dist].drop(observation).index
        n_dist_index[observation] = indexes
    
        reach_dist_array = []
        for index in indexes:
            #fonction reachdist(observation, index)
            dist_between_observation_and_index = reachdist(distance_df, observation, index)
            dist_index =  distance_df[index].nsmallest(k+1).iloc[k]
            reach_dist = max(dist_index, dist_between_observation_and_index)
            reach_dist_array.append(reach_dist)
        lrd_observation = len(indexes)/sum(reach_dist_array) 
        reach_array_dict[observation] = reach_dist_array
        lrd_dict[observation] = lrd_observation
        
    #Calcul LOF
    LOF_dict = {}
    for observation in observations:
        lrd_array = []
        for index in n_dist_index[observation]:
            lrd_array.append(lrd_dict[index])
        LOF = sum(lrd_array)*sum(reach_array_dict[observation])/np.square(len(n_dist_index[observation]))
        LOF_dict[observation] = LOF
        
        
    return LOF_dict


########## Fonction d'entraînement ###########
#data_input le training dataset
#k la population utilisée pour calculer le LOF
#distance_metric euclidean par défaut
#Renvoie le LOF maximum calculé sur le training dataset
def LOF_train (data_input, k=2, distance_metric="euclidean"):
    threshold = 0
    data=array_data(data_input)
    lof = LOF_algorithm(data, k)
    #recherche du plus grand LOF dans le cas du dataset sain
    for k,v in lof.items():
        if v>threshold:
            threshold=v
    return threshold
########## Fonction de test #############
#data_train le training dataset (utilisé par l'appel de la fonction d'entraînement)
#data_test les données à tester
# renvoie la liste (triée par LOF décroissant ) des index des outliers détectés et leur LOF
def LOF_test(data_train, data_test, distance_metric = "euclidean", k=2):
    lof_list = {}
    train = LOF_train(data_train, k)#le LOF max calculé sur le dataset sain
    threshold=train*2 #LOF seuil = 2*LOF max cas sain
    test = array_data(data_test)
    lof = LOF_algorithm(test, k) 
    for k,v in lof.items():
        if v>threshold:
            lof_list[k]=v
    if lof_list:
        print("Outliers have been detected !")
    else: 
        print("No problem detected here !")
    return sorted(lof_list.items(), key = lambda x: x[1], reverse=True)
########## TESTS ################
lof=LOF_test(data_sensor10000, data_outlier, k=4)
print(lof)
######### Affichage du temps d'exécution ##########
print("Temps d execution : %s secondes ---" % (time.time() - exetime))