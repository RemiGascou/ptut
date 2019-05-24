# -*- coding: utf-8 -*-
"""
Anomaly detection with LSTM
"""

from matplotlib import pyplot
from sklearn.preprocessing import MinMaxScaler
from pandas import DataFrame
from pandas import concat
from sklearn.metrics import mean_squared_error
from math import sqrt
import json
import tensorflow as tf
import numpy as np

########## Fonction pour formatter les données en inputs et outputs pour le RNN ##########
########## Implémentée par Jason Brownlee (https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/ ##########
# Convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg

def detection_lstm(datafile_train,datafile_test,datafile_anomalous):

    ########## Récupération des data sets dans les fichiers ##########
    f = open(datafile_train, "r")
    data_train = [json.loads(line) for line in f.readlines()]

    f = open(datafile_test, "r")
    data_traintest = [json.loads(line) for line in f.readlines()]

    f = open(datafile_anomalous, "r")
    data_test = [json.loads(line) for line in f.readlines()]

    f.close()

    ########## Préprocessing des données normales ##########

    # Lecture des données pour l'apprentissage et création d'une liste pour chaque capteur
    list_light, list_sound, list_temp_object, list_temp_ambient = [], [], [], []
    for d in data_train:
        list_light.append(d["light"])
        list_sound.append(d["sound"])
        list_temp_object.append(d["temp"]["object"])
        list_temp_ambient.append(d["temp"]["ambient"])

    nb_time_stamps = len(data_train)

    # Conversion des listes en tableaux numpy
    light_train = np.array(list_light)
    sound_train = np.array(list_sound)
    temp_object_train = np.array(list_temp_object)
    temp_ambient_train = np.array(list_temp_ambient)

    # Création d'un tableau avec toutes les valeurs
    train_values = np.stack((light_train,sound_train,temp_object_train,temp_ambient_train), axis=-1)
    #print(train_values)

    #  POUR LE TEST AVEC 2 DATA SETS DIFFERENTS POUR LE TRAINING ET LE TEST
    # Lecture des données pour le test et création d'une liste pour chaque capteur
    list_light, list_sound, list_temp_object, list_temp_ambient = [], [], [], []
    for d in data_traintest:
        list_light.append(d["light"])
        list_sound.append(d["sound"])
        list_temp_object.append(d["temp"]["object"])
        list_temp_ambient.append(d["temp"]["ambient"])

    # Conversion des listes en tableaux numpy
    lt = np.array(list_light)
    st = np.array(list_sound)
    tot = np.array(list_temp_object)
    tat = np.array(list_temp_ambient)

    # Création d'un tableau avec toutes les valeurs
    traintest_values = np.stack((lt,st,tot,tat), axis=-1)
    #print(traintest_values)

    ########## Préprocessing des données anormales  ##########

    # Lecture des données et création d'une liste pour chaque capteur
    list_light, list_sound, list_temp_object, list_temp_ambient = [], [], [], []
    for d in data_test:
        list_light.append(d["light"])
        list_sound.append(d["sound"])
        list_temp_object.append(d["temp"]["object"])
        list_temp_ambient.append(d["temp"]["ambient"])

    # Conversion des listes en tableaux numpy
    light_test = np.array(list_light)
    sound_test = np.array(list_sound)
    temp_object_test = np.array(list_temp_object)
    temp_ambient_test = np.array(list_temp_ambient)

    # Création d'un tableau avec toutes les valeurs
    abno_values = np.stack((light_test,sound_test,temp_object_test,temp_ambient_test), axis=-1)
    #print(test_values)


    ########## Affichage des données ##########
    pyplot.figure(1,figsize=(10, 8))

    pyplot.subplot(221)
    pyplot.plot(light_train, label="training")
    pyplot.plot(lt, label="testing")
    pyplot.plot(light_test, label="abnormal")
    pyplot.legend()
    pyplot.title("light")

    pyplot.subplot(222)
    pyplot.plot(sound_train, label="training")
    pyplot.plot(st, label="testing")
    pyplot.plot(sound_test, label="abnormal")
    pyplot.legend()
    pyplot.title("sound")

    pyplot.subplot(223)
    pyplot.plot(temp_object_train, label="training")
    pyplot.plot(tot, label="testing")
    pyplot.plot(temp_object_test, label="abnormal")
    pyplot.legend()
    pyplot.title("temp obj")

    pyplot.subplot(224)
    pyplot.plot(temp_ambient_train, label="training")
    pyplot.plot(tat, label="testing")
    pyplot.plot(temp_object_test, label="abnormal")
    pyplot.legend()
    pyplot.title("temp amb")

    pyplot.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.5, wspace=0.5)
    pyplot.show()

    ########## Normalisation des données ##########
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_train = scaler.fit_transform(train_values)
    scaled_test = scaler.fit_transform(traintest_values)
    # print(scaled_train.shape)

    ########## Création des données inputs et outputs pour le RNN ##########
    reframed_train = series_to_supervised(scaled_train, 1, 1)
    reframed_test = series_to_supervised(scaled_test, 1, 1)
    # print(reframed_train.head())
    # print(reframed_train.shape)
    # print(reframed_train.values)

    ########## Formalisation des données pour le RNN ##########

    #  POUR LE TEST AVEC 1 SEUL DATA SET POUR LE TRAINING ET LE TEST
    # séparation des données pour l'apprentissage et le test
    #values = reframed.values
    #n_train_values = 800
    #train = values[:n_train_values, :]
    #test = values[n_train_values:, :]
    train = reframed_train.values
    test = reframed_test.values
    # print(train.shape)
    # print(test.shape)

    # séparation en input and output
    train_X, train_y = train[:, :-4], train[:, 4:]
    test_X, test_y = test[:, :-4], test[:, 4:]
    # print(test_X.shape)
    # print(test_y.shape)

    # ajout d'une dimension pour avoir la forme [nombre_de_points, nombre_de_timesteps, nombre_de_features]
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
    # print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

    ########## Création du RNN ##########
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.LSTM(20, input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(tf.keras.layers.Dense(4))
    model.compile(loss='mae', optimizer='adam')

    ########## Phase d'apprentissage ##########
    history = model.fit(train_X, train_y, epochs=50, batch_size=30, validation_data=(test_X, test_y), verbose=2, shuffle=False)

    # Affichage de l'évolution de la fonction d'évaluation
    pyplot.plot(history.history['loss'], label='train')
    pyplot.plot(history.history['val_loss'], label='test')
    pyplot.legend()
    pyplot.show()

    ########## Prédiction sur le data set de test ##########
    yhat = model.predict(test_X)
    test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
    # print(yhat.shape)

    # Récupération des données non normalisées
    inv_yhat = scaler.inverse_transform(yhat)
    inv_yhat_light = inv_yhat[:,0]
    inv_yhat_sound = inv_yhat[:,1]
    inv_yhat_to = inv_yhat[:,2]
    inv_yhat_ta = inv_yhat[:,3]

    test_y = test_y.reshape((len(test_y), 4))
    inv_y = scaler.inverse_transform(test_y)
    inv_y_light = inv_y[:,0]
    inv_y_sound = inv_y[:,1]
    inv_y_to = inv_y[:,2]
    inv_y_ta = inv_y[:,3]

    ########## Affichage de la prédiction et de l'erreur avec le réel pour le data set de test ##########
    print("Evaluation for test data set")
    rmse = sqrt(mean_squared_error(inv_y_light, inv_yhat_light))
    print('Test RMSE light: %.3f' % rmse)
    rmse = sqrt(mean_squared_error(inv_y_sound, inv_yhat_sound))
    print('Test RMSE sound: %.3f' % rmse)
    rmse = sqrt(mean_squared_error(inv_y_to, inv_yhat_to))
    print('Test RMSE temp obj: %.3f' % rmse)
    rmse = sqrt(mean_squared_error(inv_y_ta, inv_yhat_ta))
    print('Test RMSE temp amb: %.3f' % rmse)

    pyplot.figure(1,figsize=(10, 8))

    pyplot.subplot(221)
    pyplot.plot(inv_yhat_light, label='prediction')
    pyplot.plot(inv_y_light, label='test')
    pyplot.legend()
    pyplot.title("light")

    pyplot.subplot(222)
    pyplot.plot(inv_yhat_sound, label='prediction')
    pyplot.plot(inv_y_sound, label='test')
    pyplot.legend()
    pyplot.title("sound")

    pyplot.subplot(223)
    pyplot.plot(inv_yhat_to, label='prediction')
    pyplot.plot(inv_y_to, label='test')
    pyplot.legend()
    pyplot.title("temp obj")

    pyplot.subplot(224)
    pyplot.plot(inv_yhat_ta, label='prediction')
    pyplot.plot(inv_y_ta, label='test')
    pyplot.legend()
    pyplot.title("temp amb")

    pyplot.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.5, wspace=0.5)
    pyplot.show()

    ########## Phase d'évaluation sur les données anormales ##########

    # Normalisation
    scaler = MinMaxScaler(feature_range=(0, 1))
    test_scaled = scaler.fit_transform(abno_values)
    # print(test_scaled.shape)

    # création des inputs et outputs
    test_reframed = series_to_supervised(test_scaled, 1, 1)
    # print(test_reframed.head())
    # print(test_reframed.shape)
    # print(test_reframed.values)

    real_values = test_reframed.values
    # séparation en input and output
    X, y = real_values[:, :-4], real_values[:, 4:]

    # ajout d'une dimension pour avoir la forme [nombre_de_points, nombre_de_timesteps, nombre_de_features]
    X = X.reshape((X.shape[0], 1, X.shape[1]))

    # Prédiction avec le data set contenant des anomalies
    ypred = model.predict(X)
    # print(ypred.shape)

    # Récupération des données non normalisées
    inv_ypred = scaler.inverse_transform(ypred)
    inv_ypred_light = inv_ypred[:,0]
    inv_ypred_sound = inv_ypred[:,1]
    inv_ypred_to = inv_ypred[:,2]
    inv_ypred_ta = inv_ypred[:,3]

    abno_pred = scaler.inverse_transform(y)
    y_light = abno_pred[:,0]
    y_sound = abno_pred[:,1]
    y_to = abno_pred[:,2]
    y_ta = abno_pred[:,3]

    # Calcul de l'erreur entre la prédiction et les valeurs réelles pour le data set avec anomalies
    print("Evaluation for abnormal data set")
    rmse = sqrt(mean_squared_error(inv_ypred_light, y_light))
    print('Test RMSE light: %.3f' % rmse)
    rmse = sqrt(mean_squared_error(inv_ypred_sound, y_sound))
    print('Test RMSE sound: %.3f' % rmse)
    rmse = sqrt(mean_squared_error(inv_ypred_to, y_to))
    print('Test RMSE temp obj: %.3f' % rmse)
    rmse = sqrt(mean_squared_error(inv_ypred_ta, y_ta))
    print('Test RMSE temp amb: %.3f' % rmse)

    pyplot.figure(1,figsize=(10, 8))

    pyplot.subplot(221)
    pyplot.plot(inv_ypred_light, label='prediction')
    pyplot.plot(y_light, label='abnormal')
    pyplot.legend()
    pyplot.title("light")

    pyplot.subplot(222)
    pyplot.plot(inv_ypred_sound, label='prediction')
    pyplot.plot(y_sound, label='abnormal')
    pyplot.legend()
    pyplot.title("sound")

    pyplot.subplot(223)
    pyplot.plot(inv_ypred_to, label='prediction')
    pyplot.plot(y_to, label='abnormal')
    pyplot.legend()
    pyplot.title("temp obj")

    pyplot.subplot(224)
    pyplot.plot(inv_ypred_ta, label='prediction')
    pyplot.plot(y_ta, label='abnormal')
    pyplot.legend()
    pyplot.title("temp amb")

    pyplot.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.5, wspace=0.5)
    pyplot.show()

if __name__ == '__main__':
    datafile_train = "../data/normal1000.json"
    datafile_test = "../data/train_normal800.json"
    datafile_anomalous = "../data/2abnormal1000.json"
    detection_lstm(datafile_train,datafile_test,datafile_anomalous)
