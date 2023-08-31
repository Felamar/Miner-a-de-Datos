import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as stats


def transform_data(df):
    dummies       = pd.get_dummies(df['outlook'])
    df            = pd.concat([df, dummies], axis=1)
    df            = df.drop(['outlook'], axis=1)
    cols          = df.columns.tolist()
    cols          = cols[-1 : -4 : -1] + cols[:-3]
    df[cols[:-1]] = df[cols[:-1]].astype(np.int64)
    return df[cols]

def read_data(path):
    df = pd.read_csv(path)
    return transform_data(df)

def split_data(df, train_size):
    sample_df = df.sample(frac=1)
    train     = sample_df[ : train_size]
    test      = sample_df[train_size : ]
    return train, test

def euclidean_distance(p, q):
    x = p
    y = np.array(q.values)[:-1]
    return np.sqrt(np.sum((y - x) ** 2))

def kNearestNeighbors(p, train_data, k):
    neighbors = [(euclidean_distance(p, q), i) for i, q in train_data.iterrows()]    
    neighbors.sort()
    print(k)
    return neighbors[ :k]

def iterations(k, df):
    iterations = 20
    good_guess = 0
    for it in range(iterations):    
        train_data, test_data = split_data(df, 10)
        test_classes = test_data['play']
        test_data = test_data.drop(['play'], axis=1)
        
        for i, p in test_data.iterrows():
            y          = kNearestNeighbors(p, train_data, k)
            results    = train_data.loc[[tup[1] for tup in y]]['play'].tolist()
            prediction = stats.mode(results)

            good_guess += 1 if prediction == test_classes.loc[i] else 0

    return good_guess / (len(test_data) * iterations)

def train(path):
    df = read_data(path)
    model_results = [(iterations(k, df), k) for k in range(3, 8, 2)]
    best_k        = max(model_results)
    return best_k[1]

def predict(p, best_k, path):
    df = read_data(path)
    y          = kNearestNeighbors(p, df, best_k)
    results    = df.loc[[tup[1] for tup in y]]['play'].tolist()
    prediction = stats.mode(results)
    print(prediction)
    return prediction