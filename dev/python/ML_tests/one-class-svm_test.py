from sklearn import svm
import numpy as np
import json

########## Récupération des valeurs dans les fichiers ##########
datafile = "normal1000.json"
f = open(datafile, "r")
data_train = [json.loads(line) for line in f.readlines()]

datafile = "abnormal100.json"
f = open(datafile, "r")
data_test = [json.loads(line) for line in f.readlines()]

datafile = "normal1000A.json"
f = open(datafile, "r")
data_traintest = [json.loads(line) for line in f.readlines()]

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
test_labels_light = np.array([-1 if (x<10 or x>250) else 1 for x in light_test])
test_labels_sound = np.array([-1 if (x<0 or x>85) else 1 for x in sound_test])
test_labels_to = np.array([-1 if (x<15 or x>35) else 1 for x in temp_object_test])
test_labels_ta = np.array([-1 if (x<15 or x>35) else 1 for x in temp_ambient_test])
# Création du tableau de labels pour le test avec des seulement 1 si les 4 labels sont à 1 (potentiellement à modifier pour mettre des 1 si 3 des 4 labels sont à 1)
test_labels = np.array([1 if (a==1 and b==1 and c==1 and d==1) else -1 for (a,b,c,d) in zip(test_labels_light,test_labels_sound,test_labels_to,test_labels_ta)])

# Lecture des données normales pour la vérification et création d'une liste pour chaque capteur
l,s,to,ta = [],[],[],[]
for d in data_traintest:
    l.append(d["light"])
    s.append(d["sound"])
    to.append(d["temp"]["object"])
    ta.append(d["temp"]["ambient"])
# Conversion des listes en tableaux numpy
lt = np.array(l)
st = np.array(s)
tot = np.array(to)
tat = np.array(ta)
# Récupération du maximum de chaque liste pour normaliser les valeurs entre 0 et 1
ml = lt.max()
ms = st.max()
mo = tot.max()
ma = tat.max()
# Normalisation des valeurs entre 0 et 1 pour chaque capteur
lt = lt / ml
st = st / ms
tot = tot / mo
tat = tat / ma
# Création d'un seul tableau (1000 listes de 4 valeurs) avec les valeurs des capteurs
traintest_values = np.dstack((lt,st,tot,tat))
traintest_values = traintest_values[0]


########## One-Class classification  ##########

# fit the model
clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)

clf.fit(train_values)
y_pred_train = clf.predict(train_values)
y_pred_test = clf.predict(traintest_values)
y_pred_outliers = clf.predict(test_values)

n_error_train = y_pred_train[y_pred_train == -1].size
n_error_test = y_pred_test[y_pred_test == -1].size
n_error_outliers = y_pred_outliers[y_pred_outliers == 1].size

print("error train: ", n_error_train, "/1000 ; error test: ", n_error_test, "/1000 ; errors novel abnormal: ", n_error_outliers, "/100")

print(y_pred_outliers)
print(test_labels)
