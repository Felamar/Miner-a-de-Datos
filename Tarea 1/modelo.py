# %% [markdown]
# ## Modelo de entrenamiento para la base de datos golf

# %% [markdown]
# #### Importación de librerías
# 
# Importamos las librerías pandas y numpy para agilizar el manejo de la base de datos.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as stats

# %% [markdown]
# #### Definición de variables

# %% [markdown]
# ##### traform_data(df)
# 
# Esta función es la encargada de transformar el `DataFrame` *`df`*. La transformación consiste en reemplazar la columna `outlook`, que contiene los valores ***sunny***, ***rainy***, y ***outcast***, por tres nuevas columnas con los mismos nombres. Los valores de estas columnas son un $1$ o un $0$, dependiendo del antiguo valor de `outlook`.  
# 
# > **NOTA:** La transformación de la base de datos ha sido programada específicamente para la base de datos `golf` y cualquier otra base de datos con la misma estructura.  
# > En caso de introducir una base de datos que no cumpla esta condición, el programa no arrojará los resultados esperados.  
# 

# %%
def transform_data(df):
    dummies       = pd.get_dummies(df['outlook'])
    df            = pd.concat([df, dummies], axis=1)
    df            = df.drop(['outlook'], axis=1)
    cols          = df.columns.tolist()
    cols          = cols[-1 : -4 : -1] + cols[:-3]
    df[cols[:-1]] = df[cols[:-1]].astype('int64')
    return df[cols]

# %% [markdown]
# ##### read_data(path)
# 
# Una simple función que lee una base de datos de un archivo csv desde el `path` a un `DataFrame`, y retorna la transformación de este.

# %%
def read_data(path):
    df = pd.read_csv(path)
    return transform_data(df)

# %% [markdown]
# ##### split_data(df, train_size)
# 
# Función encargada de separar las filas que usaremos para el entrenamiento del modelo de las filas que usaremos para probar el modelo.  
# 
# Se recibe el `DataFrame`, y el tamaño de la muestra de entrenamiento. Seguido creamos una variable `sample_df` que almacena una muestra de `df` pero organizado de forma aleatoria por el método `df.sample(frac = 1)` .  
# 
# > **NOTA:** El método `sample()` se encarga de crear y retornar un `DataFrame` muestra, donde las filas han sido organizadas aleatoriamente. El *keyarg* `frac` representa el porcentaje de `df` que servirá como muestra. En esta ocasión está igualado a $1$ ya que necesitamos todo el `DataFrame`.
# 
# Almacenamos los valores desde $0$ hasta `train_size-1` de esta muestra en la variable `train`. El resto es almacenado en la variable `test`.  
# 
# Se retorna un `tuple` con ambos `DataFrames`.

# %%
def split_data(df, train_size):
    sample_df = df.sample(frac=1)
    train     = sample_df[ : train_size]
    test      = sample_df[train_size : ]
    return train, test

# %% [markdown]
# ##### euclidean_distance(p, q)
# 
# Función encargada de calcular la distancia euclidiana entre la fila test $p$ y la fila train $q$.  
# 
# Se reciben dos `numpy arrays` y se excluye el último valor de ambos, el cual representa el valor de `play`.
# Dado que son `numpy array` los arreglos pueden ser tratados como vectores euclidianos, por lo que hacemos la sustracción, y la elevación al cuadrado de forma directa. 
# 
# Esta operación retorna un nuevo `numpy array`, el cual es pasado como parámetro a la función `np.sum()`. `np.sum()` retorna la suma de todos los valores que se encuentran dentro de el *array*. El resultado de esta suma es pasado a la función `np.sqrt()` para calcular su raíz cuadrada.  
# 
# Finalmente, el valor de la raíz cuadrada es retornado.

# %%
def euclidean_distance(p, q):
    x = np.array(p.values)[:-1]
    y = np.array(q.values)[:-1]
    return np.sqrt(np.sum((y - x) ** 2))

# %% [markdown]
# ##### kNearestNeighbors(x, train_data, k)
# 
# Función encargada de retornar los vecinos más cercanos a $p$.  
# 
# Se recibe los siguientes argumentos:
# - `p` : Un `numpy array` que contiene la información de la fila a evaluar 
# - `k` : El número de vecinos a tomar en cuenta 
# - `train_data` : Un `DataFrame` con las filas de entrenamiento.  
#   
# Se crea un arreglo `neighbors` usando un técnica llamada *list comprehension*. El tamaño del arreglo es igual al tamaño de `train_data`.   
# Esta variable almacena un arreglo de *tuples*, los cuales tienen como primer elemento la distancia entre $p$ y $q_i$. El segundo elemento de cada `tuple` es el índice de $q_i$.  
# 
# El arreglo se organiza de forma ascendente basándose en los valores de las distancias euclidianas y finalmente se retornan los primeros $k$ elementos del arreglo, los cuales representan los $k$ vecinos más cercanos.

# %%
def kNearestNeighbors(p, train_data, k):
    neighbors = [(euclidean_distance(p, q), i) for i, q in train_data.iterrows()]    
    neighbors.sort()
    return neighbors[ :k]

# %% [markdown]
# ##### train(k, train_data, test_data)
# 
# Función encargada de predecir el valor de `play` de cada una de las filas en `test_data`, y retornar el porcentaje de error del modelo.  
# 
# Recibe los siguientes parámetros:
# - `k` : Número de vecinos a tomar en cuenta
# - `train_data` : Un `DataFrame` con las filas de entrenamiento.
# - `test_data` : Un `DataFrame` con las filas de prueba.  
# 
# Se inicializa una variable `errors` con un valor de $0$ que representa el número de resultados erróneos. Se aumenta en uno cada que la predicción sea distinta al valor de `p['play']`.  
# Una vez terminadas las predicciones, se retorna el porcentaje de errores en el modelo. 

# %%
def train(k, train_data, test_data):
    errors = 0
    for i, p in test_data.iterrows():
        y          = kNearestNeighbors(p, train_data, k)
        results    = df.iloc[[tup[1] for tup in y]]['play'].tolist()
        prediction = stats.mode(results)

        # print(f'Punto: {p.values, i} \nVecinos: {y} \nPredicción: {prediction}\n\n')

        if prediction != p['play']:
            errors += 1
        
    return errors / len(test_data)

# %%
df = read_data('Tarea 1\golf.csv')
train_data, test_data = split_data(df, 10)
print(f'{train_data}\n\n')
print(test_data)

# %%
print(train(3, train_data, test_data))

# %%
print(train(5, train_data, test_data))

# %%
print(train(7, train_data, test_data))


