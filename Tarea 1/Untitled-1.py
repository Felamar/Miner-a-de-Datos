
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as stats

def transform_data(df):
    dummies = pd.get_dummies(df['outlook'])
    df      = pd.concat([df, dummies], axis=1)
    df      = df.drop(['outlook'], axis=1)
    cols    = df.columns.tolist()
    cols    = cols[-1 : -4 : -1] + cols[:-3]
    return df[cols]

def read_data(path):
    df = pd.read_csv(path)
    return transform_data(df)

def random_data(df):
    df = df.sample(frac=1)
    return df

def split_data(df, train_size):
    train = df[ : train_size]
    test  = df[train_size : ]
    return train, test

def euclidean_distance(x, y):
    return np.sqrt(np.sum((y[:-1] - x[:-1])**2))

def kNearestNeighbors(x, train_data, k):
    neighbors = []
    for i in range(len(train_data)):
        neighbors.append((euclidean_distance(x, train_data.iloc[i].values), i))
    neighbors.sort()
    return neighbors[:k+1]

df = read_data('Tarea 1\golf.csv')
train_data, test_data = split_data(df, 10)

k = 3
for i in range(len(train_data)):
    x = train_data.iloc[i].values
    y = kNearestNeighbors(x, train_data, k)
    results = df.iloc[[y[i][1] for i in range(len(y))]]['play'].tolist()[1:]
    prediction = stats.mode(results)
    print(f'Punto: {x} \nVecinos: {y[1:]} \nPredicción: {prediction}\n\n')




