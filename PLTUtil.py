import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib  # Importar la biblioteca joblib
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
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score

def grafica_vacia(ax):
    # Crea un gráfico vacío con el eje especificado
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_title('Gráfico Vacío')
    ax.grid(True)

    return ax
def knn_precios(ax):  # Acepta un eje como argumento
    df = pd.read_csv('./data/exactPricesPlayer_23-24.csv')

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

    # Realiza las predicciones
    y_pred = model.predict(X_test)

    # Guardar el modelo en un archivo
    model_filename = 'modelo_Precio_KNN.joblib'
    joblib.dump(model, model_filename)
    print(f'Modelo guardado como {model_filename}')

    # Evalúa el modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Imprimir el error cuadrático medio medio y el R2 del modelo
    print('Error Cuadrático Medio Medio del modelo es:', mse)
    print('Coeficiente de Determinación (R2) del modelo es:', r2)

    # Generar el gráfico de dispersión con puntos de predicción
    ax.scatter(X_test['AveragePoints'], y_test, color='black', label='Real', alpha=0.3)
    ax.scatter(X_test['AveragePoints'], y_pred, color='blue', label='Predicción', marker='x', alpha=0.5)
    #ax.plot(X_test['AveragePoints'], y_pred, color='red', linewidth=2, label='Red Neuronal')
    ax.set_xlabel('AveragePoints')
    ax.set_ylabel('Price')
    ax.set_title('Gráfico de Dispersión con KNN de Predicción de price')
    ax.legend()

    return ax

def decision_tree_precios(ax):  # Acepta un eje como argumento
    # Leer el archivo CSV
    df = pd.read_csv('./data/exactPricesPlayer_23-24.csv')

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

    # Imprimir el error cuadrático medio medio y el R2 del modelo
    print('Error Cuadrático Medio Medio del modelo es:', mse)
    print('Coeficiente de Determinación (R2) del modelo es:', r2)

    # Generar el gráfico de dispersión con puntos de predicción
    ax.scatter(X_test['AveragePoints'], y_test, color='black', label='Real', alpha=0.3)
    ax.scatter(X_test['AveragePoints'], y_pred, color='blue', label='Predicción', marker='x', alpha=0.5)
    #ax.plot(X_test['AveragePoints'], y_pred, color='red', linewidth=2, label='Red Neuronal')
    ax.set_xlabel('AveragePoints')
    ax.set_ylabel('Price')
    ax.set_title('Gráfico de Dispersión con Árbol de Decisión de Predicción de Price')
    ax.legend()

    # Guardar el modelo en un archivo
    model_filename = 'modelo_Precio_ArbolDecision.joblib'
    joblib.dump(model, model_filename)
    print(f'Modelo guardado como {model_filename}')

    return ax

def random_forest_precios(ax):  # Acepta un eje como argumento
    # Leer el archivo CSV
    df = pd.read_csv('./data/exactPricesPlayer_23-24.csv')

    # Eliminar la columna 'Name'
    df = df.drop(columns=['Name'])

    # Selecciona las columnas que necesitas
    X = df[['AveragePoints', 'Goals', 'Matches', 'AveragePtsLastThreeMatches', 'AverageCardsLastThreeMatches']]
    y = df['Price']

    # Divide los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crea el modelo de Random Forest
    model = RandomForestRegressor(random_state=7)

    # Entrena el modelo
    model.fit(X_train, y_train)

    # Realiza las predicciones
    y_pred = model.predict(X_test)

    # Evalúa el modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Imprimir el error cuadrático medio medio y el R2 del modelo
    print('Error Cuadrático Medio Medio del modelo es:', mse)
    print('Coeficiente de Determinación (R2) del modelo es:', r2)

    # Generar el gráfico de dispersión con puntos de predicción
    ax.scatter(X_test['AveragePoints'], y_test, color='black', label='Real', alpha=0.3)
    ax.scatter(X_test['AveragePoints'], y_pred, color='blue', label='Predicción', marker='x', alpha=0.5)
    #ax.plot(X_test['AveragePoints'], y_pred, color='red', linewidth=2, label='Red Neuronal')
    ax.set_xlabel('AveragePoints')
    ax.set_ylabel('Price')
    ax.set_title('Gráfico de Dispersión con Random Forest de Predicción de Price')
    ax.legend()

    # Guardar el modelo en un archivo
    model_filename = 'modelo_Precio_RandomForest.joblib'
    joblib.dump(model, model_filename)
    print(f'Modelo guardado como {model_filename}')

    return ax

def knn_puntos_jornada(ax):
    # Leer el archivo CSV
    df = pd.read_csv('./data/jugadoresFantasyActualizado.csv')

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

    # Imprimir el error cuadrático medio medio y el R2 del modelo
    print('Error Cuadrático Medio Medio del modelo es:', mse)
    print('Error Cuadrático Medio del modelo con los datos de prueba es:', mse_test)
    print('Coeficiente de Determinación (R2) del modelo es:', r2)

    # Generar el gráfico de dispersión con puntos de predicción
    ax.scatter(X_test['SOFASCORE'], y_test, color='black', label='Real', alpha=0.3)
    ax.scatter(X_test['SOFASCORE'], y_pred, color='blue', label='Predicción', marker='x', alpha=0.5)
    #ax.plot(X_test['SOFASCORE'], knn_model.predict(X_test), color='red', linewidth=2, label='KNN')
    ax.set_xlabel('SOFASCORE')
    ax.set_ylabel('puntos_Jornada')
    ax.set_title('Gráfico de Dispersión con KNN de Predicción de Puntos Jornada')
    ax.legend()

    return ax

def red_neuronal_puntos_jornada(ax):
    # Leer el archivo CSV
    df = pd.read_csv('./data/jugadoresFantasyActualizado.csv')

    # Eliminar filas con valores nulos
    df = df.dropna()

    # Seleccionar los atributos con mayor correlación
    selected_features = ['SOFASCORE', 'puntos_SOFASCORE', 'AS', 'puntos_AS', 'MD', 'puntos_MD', 'MARCA', 'puntos_MARCA']
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

    # Imprimir el error cuadrático medio medio y el R2 del modelo
    print('Error Cuadrático Medio Medio del modelo es:', mse)
    print('Error Cuadrático Medio del modelo con los datos de prueba es:', mse_test)
    print('Coeficiente de Determinación (R2) del modelo es:', r2)

    # Generar el gráfico de dispersión con puntos de predicción
    ax.scatter(X_test['SOFASCORE'], y_test, color='black', label='Real', alpha=0.3)
    ax.scatter(X_test['SOFASCORE'], y_pred, color='blue', label='Predicción', marker='x', alpha=0.5)
    #ax.plot(X_test['SOFASCORE'], y_pred, color='red', linewidth=2, label='Red Neuronal')
    ax.set_xlabel('SOFASCORE')
    ax.set_ylabel('puntos_Jornada')
    ax.set_title('Gráfico de Dispersión con Red Neuronal de Predicción de Puntos Jornada')
    ax.legend()

    return ax

def arbol_decision_puntos_jornada(ax):
    # Leer el archivo CSV
    df = pd.read_csv('./data/jugadoresFantasyActualizado.csv')

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

    # Imprimir el error cuadrático medio medio y el R2 del modelo
    print('Error Cuadrático Medio Medio del modelo es:', mse)
    print('Error Cuadrático Medio del modelo con los datos de prueba es:', mse_test)
    print('Coeficiente de Determinación (R2) del modelo es:', r2)

    # Generar el gráfico de dispersión con puntos de predicción
    ax.scatter(X_test['SOFASCORE'], y_test, color='black', label='Real', alpha=0.3)
    ax.scatter(X_test['SOFASCORE'], y_pred, color='blue', label='Predicción', marker='x', alpha=0.5)
    #ax.plot(X_test['SOFASCORE'], y_pred, color='red', linewidth=2, label='Árbol de Decisión')
    ax.set_xlabel('SOFASCORE')
    ax.set_ylabel('puntos_Jornada')
    ax.set_title('Gráfico de Dispersión con Árbol de Decisión de Predicción de Puntos Jornada')
    ax.legend()

    return ax