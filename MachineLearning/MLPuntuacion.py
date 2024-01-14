import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn import svm
from sklearn.neighbors import KNeighborsRegressor
import joblib  # Importar la biblioteca joblib
from sklearn.neural_network import MLPRegressor



def knn(ruta_fichero):
    # Cargar el dataset desde un archivo CSV
    df = pd.read_csv(ruta_fichero)
    # Eliminar la columna 'Name'
    df = df.drop(columns=['Name', 'Team', 'Jornada'])

    # Convertir la columna 'Status' a un formato numérico
    df['posicion'] = df['posicion'].astype('category').cat.codes

    # Convertir la columna 'Status' a un formato numérico
    df['status'] = df['status'].astype('category').cat.codes

    # Eliminar filas con valores nulos
    df = df.dropna()

    # Seleccionar los atributos con mayor correlación
    selected_features = ['SOFASCORE', 'puntos_SOFASCORE', 'AS', 'puntos_AS', 'MD', 'puntos_MD', 'MARCA', 'puntos_MARCA', 'puntos_Goles']
    X = df[selected_features]
    y = df['puntos_Jornada']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Crear el modelo KNN para regresión
    knn_model = KNeighborsRegressor(n_neighbors=4)  # Puedes ajustar el número de vecinos según sea necesario

    # Realizar Cross-Validation para evaluar el rendimiento del modelo
    scores = cross_val_score(knn_model, X_train, y_train, cv=10, scoring='neg_mean_squared_error')

    # Calcular el error cuadrático medio medio del modelo
    mse = -np.mean(scores)

    # Entrenar el modelo con los datos de entrenamiento
    knn_model.fit(X_train, y_train)

    # Realizar predicciones con los datos de prueba
    y_pred = knn_model.predict(X_test)

    # Calcular el error cuadrático medio del modelo con los datos de prueba
    mse_test = mean_squared_error(y_test, y_pred)

    # Calcular el coeficiente de determinación (R2)
    r2 = r2_score(y_test, y_pred)

    return knn_model


def redes_neuronales(ruta_fichero):
    # Cargar el dataset desde un archivo CSV
    df = pd.read_csv(ruta_fichero)
    # Eliminar la columna 'Name'
    df = df.drop(columns=['Name', 'Team', 'Jornada'])

    # Convertir la columna 'Status' a un formato numérico
    df['posicion'] = df['posicion'].astype('category').cat.codes

    # Convertir la columna 'Status' a un formato numérico
    df['status'] = df['status'].astype('category').cat.codes

    # Eliminar filas con valores nulos
    df = df.dropna()

    # Seleccionar los atributos con mayor correlación
    selected_features = ['SOFASCORE', 'puntos_SOFASCORE', 'AS', 'puntos_AS', 'MD', 'puntos_MD', 'MARCA', 'puntos_MARCA', 'puntos_Goles']
    X = df[selected_features]
    y = df['puntos_Jornada']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Crear el modelo de Red Neuronal
    # Puedes ajustar los parámetros según sea necesario
    model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=0)

    # Realizar Cross-Validation para evaluar el rendimiento del modelo
    scores = cross_val_score(model, X_train, y_train, cv=10, scoring='neg_mean_squared_error')

    # Calcular el error cuadrático medio medio del modelo
    mse = -np.mean(scores)

    # Entrenar el modelo con los datos de entrenamiento
    model.fit(X_train, y_train)

    # Realizar predicciones con los datos de prueba
    y_pred = model.predict(X_test)

    # Calcular el error cuadrático medio del modelo con los datos de prueba
    mse_test = mean_squared_error(y_test, y_pred)

    # Calcular el coeficiente de determinación (R2)
    r2 = r2_score(y_test, y_pred)

    return model

def arbol_decision(ruta_fichero):
    # Cargar el dataset desde un archivo CSV
    df = pd.read_csv(ruta_fichero)
    # Eliminar la columna 'Name'
    df = df.drop(columns=['Name', 'Team', 'Jornada'])

    # Convertir la columna 'Status' a un formato numérico
    df['posicion'] = df['posicion'].astype('category').cat.codes

    # Convertir la columna 'Status' a un formato numérico
    df['status'] = df['status'].astype('category').cat.codes
    
    # Eliminar filas con valores nulos
    df = df.dropna()

    # Seleccionar los atributos con mayor correlación
    selected_features = ['SOFASCORE', 'puntos_SOFASCORE', 'AS', 'puntos_AS', 'MD', 'puntos_MD', 'MARCA', 'puntos_MARCA', 'puntos_Goles']
    X = df[selected_features]
    y = df['puntos_Jornada']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Crear el modelo de árbol de decisión para regresión
    tree_model = DecisionTreeRegressor(random_state=0)

    # Realizar Cross-Validation para evaluar el rendimiento del modelo
    scores = cross_val_score(tree_model, X_train, y_train, cv=10, scoring='neg_mean_squared_error')

    # Calcular el error cuadrático medio medio del modelo
    mse = -np.mean(scores)

    # Entrenar el modelo con los datos de entrenamiento
    tree_model.fit(X_train, y_train)

    # Realizar predicciones con los datos de prueba
    y_pred = tree_model.predict(X_test)

    # Calcular el error cuadrático medio del modelo con los datos de prueba
    mse_test = mean_squared_error(y_test, y_pred)

    # Calcular el coeficiente de determinación (R2)
    r2 = r2_score(y_test, y_pred)

    return tree_model


def exportar(ruta_fichero, modelo):
    model_filename = 'modelo_ArbolDeDecisiones.joblib'
    joblib.dump(modelo, ruta_fichero)
    print(f'Modelo guardado como {model_filename}')

def predecir_knn(ruta_modelo, datos):
    # Cargar el modelo desde el archivo
    loaded_model = joblib.load(ruta_modelo)

    nuevos_datos = pd.DataFrame({'SOFASCORE': [7.9], 'puntos_SOFASCORE': [9], 'AS': [1], 'puntos_AS': [2], 'MD': [1], 'puntos_MD': [2], 'MARCA': [1], 'puntos_MARCA': [2], 'puntos_Goles': [0]})

    # Realizar predicciones con los datos de prueba (o cualquier otro conjunto de datos)
    nuevas_predicciones = loaded_model.predict(nuevos_datos)
    
    return nuevas_predicciones

def predecir_redes_neuronales(ruta_modelo, datos):
    # Cargar el modelo desde el archivo
    loaded_model = joblib.load(ruta_modelo)

    nuevos_datos = pd.DataFrame({'SOFASCORE': [7.9], 'puntos_SOFASCORE': [9], 'AS': [1], 'puntos_AS': [2], 'MD': [1], 'puntos_MD': [2], 'MARCA': [1], 'puntos_MARCA': [2], 'puntos_Goles': [0]})

    # Realizar predicciones con los datos de prueba (o cualquier otro conjunto de datos)
    nuevas_predicciones = loaded_model.predict(nuevos_datos)
    
    return nuevas_predicciones

def predecir_arbol_decision(ruta_fichero, datos):
    # Cargar el modelo desde el archivo
    loaded_model = joblib.load('modelo_ArbolDeDecisiones.joblib')

    nuevos_datos = pd.DataFrame({'SOFASCORE': [7.9], 'puntos_SOFASCORE': [9], 'AS': [1], 'puntos_AS': [2], 'MD': [1], 'puntos_MD': [2], 'MARCA': [1], 'puntos_MARCA': [2], 'puntos_Goles': [0]})

    # Realizar predicciones con los datos de prueba (o cualquier otro conjunto de datos)
    nuevas_predicciones = loaded_model.predict(nuevos_datos)

    return nuevas_predicciones


def predecir(modelo, ejemplares):
    print(ejemplares.to_string())
    resultado = modelo.predict(ejemplares)
    resultado_int = [int(x) for x in resultado]
    return resultado_int

def importar_modelo(ruta_fichero):
    loaded_model = joblib.load(ruta_fichero)
    return loaded_model

def exportar_modelo(ruta_fichero, modelo):
    joblib.dump(modelo, ruta_fichero)