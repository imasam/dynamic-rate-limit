import pandas as pd
import numpy as np
import random
import os
import matplotlib.pyplot as plt
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from keras.models import Sequential, Model
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import LSTM

def read_from_csv_and_get_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8', header=0)
    dataset = df.to_numpy()
    
    X = dataset[:, 0:17]
    X1 = dataset[:,18].reshape(-1, 1)
    X = np.concatenate((X, X1), axis=1)
    
    Y = dataset[:, 17]
    return X, Y

df = pd.read_csv('../../r1_service_c/r1_service_c_10.csv',encoding='utf-8',header=0)
dataset = df.to_numpy()

X = dataset[:, 0:17]
X1 = dataset[:,18].reshape(-1, 1)
X = np.concatenate((X, X1), axis=1)
X.shape

Y = dataset[:, 17]

new_X_dataset = np.ones(shape=(1,5,18))
new_Y_dataset = np.ones(shape=(1,1))

dir_path = '../../r1_service_c'
for file in os.listdir(dir_path):
    if file[0] != '.':
        X, Y = read_from_csv_and_get_data(dir_path + '/' + file)
        for i in range(5, 51):
            reshape_X = X[i-5:i,:].reshape(1, 5, -1)
            new_X_dataset = np.concatenate((new_X_dataset, reshape_X), axis=0)

            reshape_Y = Y[i-1].reshape(1,1)
            new_Y_dataset = np.concatenate((new_Y_dataset, reshape_Y), axis=0)
    
new_Y_dataset = new_Y_dataset.reshape(-1,)

for i in range(len(new_Y_dataset)):
    new_Y_dataset[i] = new_Y_dataset[i] // 10
NUM_OF_TYPE = int(max(new_Y_dataset)) + 1

new_Y_dataset_one_hot = np_utils.to_categorical(new_Y_dataset, NUM_OF_TYPE) #  float32

X_train, X_test, Y_train, Y_test = train_test_split(new_X_dataset, new_Y_dataset_one_hot, test_size=0.3, random_state=0)

model = Sequential()
model.add(LSTM(64,input_shape=(5,18)))
model.add(Dense(32))
model.add(Dropout(0.2))
model.add(Dense(24))
model.add(Dropout(0.2))
model.add(Dense(NUM_OF_TYPE, activation='softmax'))

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])

batch_size=16
nb_class=NUM_OF_TYPE
nb_epochs = 50
Training = model.fit(X_train, Y_train,
                    epochs=nb_epochs, batch_size=batch_size,
                    validation_data=(X_test, Y_test))

model.save('r1_service_c_lstm')