import keras
import pandas as pd
import random
from sklearn import metrics
import numpy as np
from keras.utils import np_utils
from keras.models import Sequential, Model
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import LSTM
from sklearn.model_selection import train_test_split

df = pd.read_csv("../../r2_service_d_all.csv")
dataset = df.to_numpy()
X = dataset[:, 0:17]
X1 = dataset[:,18].reshape(-1, 1)
X = np.concatenate((X, X1), axis=1)
Y = dataset[:, 17]

# X = dataset[:, 1:18]
# X1 = dataset[:,19].reshape(-1, 1)
# X = np.concatenate((X, X1), axis=1)
# Y = dataset[:, 18]

for i in range(len(Y)):
    Y[i] = Y[i] // 10
NUM_OF_TYPE = int(max(Y)) + 1

Y_one_hot = np_utils.to_categorical(Y, NUM_OF_TYPE) #  float32
X_train, X_test, Y_train, Y_test = train_test_split(X, Y_one_hot, test_size=0.3, random_state=0)

model = Sequential()
model.add(Dense(512, activation='relu', input_dim=18))
model.add(Dropout(0.2))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(NUM_OF_TYPE, activation='softmax'))

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])

batch_size=32
nb_class=NUM_OF_TYPE
nb_epochs = 50
Training = model.fit(X_train, Y_train,
                    epochs=nb_epochs, batch_size=batch_size,
                    validation_data=(X_test, Y_test))

model.save('r2_service_d_fc')
