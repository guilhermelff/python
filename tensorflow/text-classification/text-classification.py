import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler


dfWine = pd.read_csv("wine-reviews.csv", usecols = ['country','description','points', 'price', 'variety', 'winery'])
dfDiab = pd.read_csv("diabetes.csv")

print("-----------------------------------------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------------------------------------")
print("\n ")

print(dfWine.head())

print("\n ")
print("-----------------------------------------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------------------------------------")
print("\n ")

print(dfDiab.head())

print("\n ")
print("-----------------------------------------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------------------------------------")

x = dfDiab[dfDiab.columns[:-1]].values
y = dfDiab[dfDiab.columns[-1]].values

scaler = StandardScaler()
x = scaler.fit_transform(x)

x_train, x_temp, y_train, y_temp = train_test_split(x, y, test_size=0.4, random_state=0)
x_valid, x_test, y_valid, y_test = train_test_split(x_temp, y_temp, test_size=0.5, random_state=0)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid'),
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics=['accuracy']
              )

#model.fit(x_train, y_train, batch_size=16, epochs=2000, validation_data=(x_valid, y_valid))