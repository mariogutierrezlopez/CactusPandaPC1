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


# Cargar el dataset desde un archivo CSV

class MLPrecios:
    @staticmethod
    def knn(ruta_fichero):
        # Cargar el dataset desde un archivo CSV
        df = pd.read_csv(ruta_fichero)
        # Eliminar la columna 'Name'
        df = df.drop(columns=['Name', 'Team', 'Jornada'])

        # Convertir la columna 'Posicion' a un formato numérico
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

        # Generar el gráfico de dispersión con puntos de predicción
        plt.scatter(X_test['SOFASCORE'], y_test, color='black', label='Real', alpha=0.3)
        plt.scatter(X_test['SOFASCORE'], y_pred, color='blue', label='Predicción', marker='x', alpha=0.5)
        plt.xlabel('SOFASCORE')
        plt.ylabel('puntos_Jornada')
        plt.title('Gráfico de Dispersión con KNN de Predicción de Puntos Jornada')
        plt.legend()
        plt.show()

        return knn_model, X_test, y_test
    
    @staticmethod
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

        # Generar el gráfico de dispersión con puntos de predicción
        plt.scatter(X_test['SOFASCORE'], y_test, color='black', label='Real', alpha=0.3)
        plt.scatter(X_test['SOFASCORE'], y_pred, color='blue', label='Predicción', marker='x', alpha=0.5)
        plt.xlabel('SOFASCORE')
        plt.ylabel('puntos_Jornada')
        plt.title('Gráfico de Dispersión con Red Neuronal de Predicción de Puntos Jornada')
        plt.legend()
        plt.show()

        return model

    @staticmethod
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

        # Generar el gráfico de dispersión con puntos de predicción
        plt.scatter(X_test['SOFASCORE'], y_test, color='black', label='Real', alpha=0.3)
        plt.scatter(X_test['SOFASCORE'], y_pred, color='blue', label='Predicción', marker='x', alpha=0.5)
        plt.xlabel('SOFASCORE')
        plt.ylabel('puntos_Jornada')
        plt.title('Gráfico de Dispersión con Árbol de Decisión de Predicción de Puntos Jornada')
        plt.legend()
        plt.show()

        return tree_model
    
    @staticmethod
    def exportar(ruta_fichero, modelo):
        model_filename = 'modelo_ArbolDeDecisiones.joblib'
        joblib.dump(modelo, ruta_fichero)
        print(f'Modelo guardado como {model_filename}')