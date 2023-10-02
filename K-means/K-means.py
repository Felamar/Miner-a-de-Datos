# %%
import pandas as pd
import numpy as np

# %%
def read_data(file_name: str) -> pd.DataFrame:
    df = pd.read_csv(file_name, header=None, sep=',')
    df = df.replace('?', np.nan)
    return df.astype(np.float32)

# %%
def a_distance(centroid_a, object_a, range_a) -> float:
    if np.isnan(centroid_a) or np.isnan(object_a): return 1
    if centroid_a == object_a                    : return 0
    if range_a == 1                              : return 1
    return abs(centroid_a - object_a) / range_a

# %%
def HEOM(centroid, object, ranges) -> float:
    distances = np.array([a_distance(centroid[a], object[a], ranges[a]) for a in range(len(centroid))])
    return np.sqrt(np.sum(np.square(distances)))

# %%
def get_extremes(df : pd.DataFrame) -> list:
    return [(df[column].dropna().max(), df[column].dropna().min()) for column in df.columns]

# %%
def get_ranges(extremes : list) -> np.array:
    return np.array([ex_tup[0] - ex_tup[1] for ex_tup in extremes])

# %%
def get_centroids(extremes: list, k: int, ranges: np.array) -> np.array:
    centroids = []

    for _ in range(k):
        centroid = []

        for i, (max, min) in enumerate(extremes):
            if   ranges[i] == 1            : a = np.random.choice([max, min])
            elif max % 1 > 0 or min % 1 > 0: a = round(np.random.uniform(min, max), 2)
            else                           : a = np.random.randint(min, max)
            centroid.append(a)

        centroids.append(centroid)
        
    return np.array(centroids)

# %%
def clustering(centroids: np.array, df: pd.DataFrame, ranges: np.array) -> np.array:
    clusters = np.zeros(len(df))

    for i, row in df.iterrows():
        distances   = np.array([HEOM(centroid, row, ranges) for centroid in centroids])
        clusters[i] = np.argmin(distances)
        
    return clusters

# %%
def k_means(df: pd.DataFrame, k: int) -> pd.DataFrame:
    extremes     = get_extremes (df)
    ranges       = get_ranges   (extremes)
    centroids    = get_centroids(extremes, k, ranges)
    clusters     = clustering   (centroids, df, ranges)
    df_clustered = df.copy().assign(cluster=clusters)

    cluster_array = []
    cluster_array.append(clusters)
    while True:
        
        new_centroids = np.array  ([round(df_clustered[df_clustered['cluster'] == i].mean(), 2)[:-1] for i in range(k)])
        new_clusters  = clustering(new_centroids, df, ranges)

        cluster_array.append(new_clusters)

        if len(cluster_array) > 3: cluster_array.pop(0)
        if len(cluster_array) > 2 and np.array_equal(cluster_array[0], cluster_array[2]): break
        if np.array_equal(clusters, new_clusters): break

        clusters = new_clusters
        df_clustered['cluster'] = clusters

        print(f'cemtroids: \n{new_centroids}')
        print(f'clusters: \n{clusters}')
        
    return df.assign(cluster=clusters)

# %%
df = read_data('K-means\hepatitis\hepatitis.data')
df_clustered = k_means(df, 3)
df_clustered.to_csv('hepatitis_clustered.csv', index=False)


