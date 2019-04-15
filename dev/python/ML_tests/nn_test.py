import numpy as np
import tensorflow as tf
from tensorflow import keras
import json

########## Récupération des valeurs dans les fichiers ##########
datafile = "normal1000.json"
f = open(datafile, "r")
data_train = [json.loads(line) for line in f.readlines()]

datafile = "abnormal100.json"
f = open(datafile, "r")
data_test = [json.loads(line) for line in f.readlines()]

f.close()

########## Formalisation des données  ##########

# Lecture des données pour l'apprentissage et création d'une liste pour chaque capteur
list_light, list_sound, list_temp_object, list_temp_ambient = [], [], [], []
for d in data_train:
    list_light.append(d["light"])
    list_sound.append(d["sound"])
    list_temp_object.append(d["temp"]["object"])
    list_temp_ambient.append(d["temp"]["ambient"])
# Conversion des listes en tableaux numpy
light_train = np.array(list_light)
sound_train = np.array(list_sound)
temp_object_train = np.array(list_temp_object)
temp_ambient_train = np.array(list_temp_ambient)
# Récupération du maximum de chaque liste pour normaliser les valeurs entre 0 et 1
ml = light_train.max()
ms = sound_train.max()
mo = temp_object_train.max()
ma = temp_ambient_train.max()
# Normalisation des valeurs entre 0 et 1 pour chaque capteur
light_train = light_train / ml
sound_train = sound_train / ms
temp_object_train = temp_object_train / mo
temp_ambient_train = temp_ambient_train / ma
# Création d'un seul tableau (1000 listes de 4 valeurs) avec les valeurs des capteurs
train_values = np.dstack((light_train,sound_train,temp_object_train,temp_ambient_train))
train_values = train_values[0]
# Création du vecteur de label avec que des 1
train_labels = np.ones((1000,1))


# Lecture des données pour le test et création d'une liste pour chaque capteur
list_l, list_s, list_to, list_ta = [], [], [], []
for d in data_test:
    list_l.append(d["light"])
    list_s.append(d["sound"])
    list_to.append(d["temp"]["object"])
    list_ta.append(d["temp"]["ambient"])
# Conversion des listes en tableaux numpy
light_test = np.array(list_l)
sound_test = np.array(list_s)
temp_object_test = np.array(list_to)
temp_ambient_test = np.array(list_ta)
# Récupération du maximum de chaque liste pour normaliser les valeurs entre 0 et 1
ml = light_test.max()
ms = sound_test.max()
mo= temp_object_test.max()
ma = temp_ambient_test.max()
# Normalisation des valeurs entre 0 et 1 pour chaque capteur
light_test = light_test / ml
sound_test = sound_test / ms
temp_object_test = temp_object_test / mo
temp_ambient_test = temp_ambient_test / ma
# Création d'un seul tableau (1000 listes de 4 valeurs) avec les valeurs des capteurs
test_values = np.dstack((light_test,sound_test,temp_object_test,temp_ambient_test))
test_values = test_values[0]
# Création des tableaux labels pour chaque capteur avec 1 si les valeurs sont dans les bornes normales
test_labels_light = np.array([0 if (x<10 or x>250) else 1 for x in light_test])
test_labels_sound = np.array([0 if (x<0 or x>85) else 1 for x in sound_test])
test_labels_to = np.array([0 if (x<15 or x>35) else 1 for x in temp_object_test])
test_labels_ta = np.array([0 if (x<15 or x>35) else 1 for x in temp_ambient_test])
# Création du tableau de labels pour le test avec des seulement 1 si les 4 labels sont à 1 (potentiellement à modifier pour mettre des 1 si 3 des 4 labels sont à 1)
test_labels = np.array([a*b*c*d for (a,b,c,d) in zip(test_labels_light,test_labels_sound,test_labels_to,test_labels_ta)])

########## Création du réseau de neurones ##########
#1 input layer de 4 neurones
#1 hidden layer de 2 neurones avec ReL activation function
#1 output layer de 1 neurone avec sigmoid function
model = keras.Sequential([
    keras.layers.Dense(4, activation=tf.nn.relu, input_shape=(4,)),
    keras.layers.Dense(1, activation=tf.nn.sigmoid)
])
#Paramètres pour classification binaire
model.compile(optimizer='adagrad',
              loss='binary_crossentropy',
              metrics=['accuracy'])
#Apprentissage sur 10 epochs (=on passe 10 fois par toutes les données)
#et des batch de taille 32 (=on met à jour w et b tous les 32 samples)
model.fit(train_values, train_labels, epochs=10, batch_size=32)
# Evaluation du modèle et test de la prédiction sur le tableau test
test_loss, test_acc = model.evaluate(test_values, test_labels)
predictions = model.predict(test_values)
print('Test accuracy:', test_acc)
print('Test loss:', test_loss)
print(predictions)
