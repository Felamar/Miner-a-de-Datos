# %%
import pandas as pd
import numpy as np

# %%
def read_data(file_name: str) -> pd.DataFrame:
    # Read data from file
    df = pd.read_csv(file_name, header=None, sep=',')
    # Replace '?' with NaN
    df = df.replace('?', np.nan)
    # Convert to float32
    return df.astype(np.float32)

# %%
def a_distance(centroid_a, object_a, range_a) -> float:
    # Calculate distance between centroid and object

    # If centroid or object is NaN, return 1
    if np.isnan(centroid_a) or np.isnan(object_a): return 1
    # If centroid and object are the same, return 0
    if centroid_a == object_a                    : return 0
    # If range is 1, return 1
    if range_a == 1                              : return 1
    # Else, return distance
    return abs(centroid_a - object_a) / range_a

# %%
def HEOM(centroid, object, ranges) -> float:
    # Calculate HEOM distance between centroid and object

    # Calculate distance for each attribute and store it in an array
    distances = np.array([a_distance(centroid[a], object[a], ranges[a]) for a in range(len(centroid))])
    # Return square root of sum of squares of distances
    return np.sqrt(np.sum(np.square(distances)))

# %%
def get_extremes(df : pd.DataFrame) -> list:
    # Get maximum and minimum values for each column

    # Return list of tuples containing maximum and minimum values for each column
    return [(df[column].dropna().max(), df[column].dropna().min()) for column in df.columns]

# %%
def get_ranges(extremes : list) -> np.array:
    # Get range for each column

    # Return array of ranges for each column
    return np.array([ex_tup[0] - ex_tup[1] for ex_tup in extremes])

# %%
def get_centroids(extremes: list, k: int, ranges: np.array) -> np.array:
    # Get k random centroids

    # Create empty list to store centroids
    centroids = []

    # For each centroid
    for _ in range(k):
        # Create empty list to store centroid values
        centroid = []

        # For each column
        for i, (max, min) in enumerate(extremes):
            # If range is 1, choose either maximum or minimum
            if   ranges[i] == 1            : a = np.random.choice([max, min])
            # If range is float, choose a random float between maximum and minimum
            elif max % 1 > 0 or min % 1 > 0: a = round(np.random.uniform(min, max), 2)
            # If range is integer, choose a random integer between maximum and minimum
            else                           : a = np.random.randint(min, max)
            # Append value to centroid list
            centroid.append(a)

        # Append centroid to centroids list
        centroids.append(centroid)
        
    # Return array of centroids
    return np.array(centroids)

# %%
def clustering(centroids: np.array, df: pd.DataFrame, ranges: np.array) -> np.array:
    # Cluster objects to centroids

    # Create empty array to store clusters
    clusters = np.zeros(len(df))

    # For each object
    for i, row in df.iterrows():
        # Calculate HEOM distance between object and each centroid
        distances   = np.array([HEOM(centroid, row, ranges) for centroid in centroids])
        # Assign object to cluster with minimum distance
        clusters[i] = np.argmin(distances)

    # Return array of clusters
    return clusters

# %%
def k_means(df: pd.DataFrame, k: int) -> pd.DataFrame:
    # K-means clustering algorithm

    # Get maximum and minimum values for each column
    extremes     = get_extremes (df)
    # Get range for each column
    ranges       = get_ranges   (extremes)
    # Get k random centroids
    centroids    = get_centroids(extremes, k, ranges)
    # Cluster objects to centroids
    clusters     = clustering   (centroids, df, ranges)
    # Create new dataframe with clusters
    df_clustered = df.copy().assign(cluster=clusters)

    # Create empty list to store clusters
    cluster_array = []
    # Append clusters to cluster array
    cluster_array.append(clusters)

    # While clusters are changing
    while True:
        # Calculate new centroids
        new_centroids = np.array  ([round(df_clustered[df_clustered['cluster'] == i].mean(), 2)[:-1] for i in range(k)])
        # Cluster objects to new centroids
        new_clusters  = clustering(new_centroids, df, ranges)
        # Append clusters to cluster array
        cluster_array.append(new_clusters)

        # If cluster array has more than 3 elements pop the first element
        if len(cluster_array) > 3: cluster_array.pop(0)
        # If first and third cluster are the same, break
        if len(cluster_array) > 2 and np.array_equal(cluster_array[0], cluster_array[2]): break
        # If second and third cluster are the same, break
        if np.array_equal(clusters, new_clusters): break

        # Set clusters to new clusters
        clusters = new_clusters
        # Set cluster column to new clusters
        df_clustered['cluster'] = clusters

        print(f'cemtroids: \n{new_centroids}')
        print(f'clusters: \n{clusters}')

    # Return dataframe with clusters        
    return pd.DataFrame(clusters)

# %%
df = read_data('hepatitis\\hepatitis.data')
df_clustered = k_means(df, 3)
df_clustered.to_csv('hepatitis_clustered.csv', index=False)