import pandas as pd
import numpy as np
import statistics as stats

def transform_data(df):
    default_cols  = ['overcast', 'rainy', 'sunny']
    dummies       = pd.get_dummies(df['outlook'])
    dummies       = dummies.reindex(columns=default_cols, fill_value=0)
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
    x = np.array(p.values)
    y = np.array(q.values)[:-1]
    return np.sqrt(np.sum((y - x) ** 2))

def kNearestNeighbors(p, train_data, k):
    neighbors = [(euclidean_distance(p, q), i) for i, q in train_data.iterrows()]    
    neighbors.sort()
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
    return best_k

def predict(test_path, train_path, k):
    test_df  = read_data(test_path)
    train_df = read_data(train_path)
    predictions = np.array([None] * len(test_df))

    for i, p in test_df.iterrows():
        y          = kNearestNeighbors(p, train_df, k)
        results    = train_df.loc[[tup[1] for tup in y]]['play'].tolist()
        prediction = stats.mode(results)
        predictions[i] = prediction

    test_df['play'] = predictions
    test_df.to_csv('Tarea 1\\results.csv', index=False)