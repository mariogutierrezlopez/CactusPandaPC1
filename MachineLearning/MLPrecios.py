import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def knn(ruta_fichero):
    df = pd.read_csv(ruta_fichero)

    # Eliminar la columna 'Name'
    df = df.drop(columns=['Name'])

    # Selecciona las columnas que necesitas
    X = df[['AveragePoints', 'Goals',  'Matches', 'AveragePtsLastThreeMatches', 'AverageCardsLastThreeMatches']]
    y = df['Price']

    # Divide los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crea el modelo KNN
    model = KNeighborsRegressor(n_neighbors=2)

    # Entrena el modelo
    model.fit(X_train, y_train)

    return model

def arbol_decision(ruta_fichero):
        
    # Leer el archivo CSV
    df = pd.read_csv(ruta_fichero)

    # Eliminar la columna 'Name'
    df = df.drop(columns=['Name'])

    # Selecciona las columnas que necesitas
    X = df[['AveragePoints', 'Goals', 'Matches', 'AveragePtsLastThreeMatches', 'AverageCardsLastThreeMatches']]
    y = df['Price']

    # Divide los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crea el modelo de árbol de decisión
    model = DecisionTreeRegressor(random_state=16)

    # Entrena el modelo
    model.fit(X_train, y_train)

    # Realiza las predicciones
    y_pred = model.predict(X_test)

    # Evalúa el modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'Mean Squared Error: {mse}')
    print(f'R2 Score: {r2}')

    return model

def random_forest(ruta_fichero):   
    # Leer el archivo CSV
    df = pd.read_csv(ruta_fichero)

    # Eliminar la columna 'Name'
    df = df.drop(columns=['Name'])

    # Selecciona las columnas que necesitas
    X = df[['AveragePoints', 'Goals', 'Matches', 'AveragePtsLastThreeMatches', 'AverageCardsLastThreeMatches']]
    y = df['Price']

    # Divide los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crea el modelo de árbol de decisión
    model = RandomForestRegressor(random_state=7)

    # Entrena el modelo
    model.fit(X_train, y_train)

    # Realiza las predicciones
    y_pred = model.predict(X_test)

    # Evalúa el modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'Mean Squared Error: {mse}')
    print(f'R2 Score: {r2}')

    return model

def grafica_prediccion(modelo, datos):
    # Realizar predicciones usando el modelo entrenado
    predicciones = modelo.predict(datos)

    # Generar el gráfico de dispersión con puntos de predicción
    plt.scatter(datos['SOFASCORE'], predicciones, color='red', label='Predicción', marker='x', alpha=0.5)
    plt.xlabel('SOFASCORE')
    plt.ylabel('Puntos Predichos')
    plt.title('Gráfico de Dispersión con Predicciones del Modelo')
    plt.legend()
    plt.show()

def predecir(modelo, ejemplares):
    resultado = modelo.predict(ejemplares)
    resultado_int = [int(x) for x in resultado]
    return resultado_int

def importar_modelo(ruta_fichero):
    loaded_model = joblib.load(ruta_fichero)
    return loaded_model

def exportar_modelo(ruta_fichero, modelo):
    joblib.dump(modelo, ruta_fichero)