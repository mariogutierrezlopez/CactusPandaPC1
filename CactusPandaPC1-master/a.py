import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Crear un DataFrame de ejemplo
data = {'SOFASCORE': [8.5, 9.0, 7.8, 6.5, 8.2],
        'puntos_Jornada': [85, 90, 78, 65, 82]}
df = pd.DataFrame(data)

# Seleccionar los atributos con mayor correlación
selected_features = ['SOFASCORE']
X = df[selected_features]
y = df['puntos_Jornada']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Crear el modelo KNN para regresión
knn_model = KNeighborsRegressor(n_neighbors=4)

# Realizar Cross-Validation para evaluar el rendimiento del modelo
scores = cross_val_score(knn_model, X_train, y_train, cv=4, scoring='neg_mean_squared_error')

# Calcular el error cuadrático medio medio del modelo
mse = -np.mean(scores)

# Entrenar el modelo con los datos de entrenamiento
knn_model.fit(X_train, y_train)

# Realizar predicciones con los datos de prueba
y_pred = knn_model.predict(X_test)

# Calcular el coeficiente de determinación (R2)
r2 = r2_score(y_test, y_pred)

# Crear un cuadro de diálogo para mostrar el gráfico de dispersión
class ScatterPlotDialog(QDialog):
    def __init__(self, X_test, y_test, y_pred):
        super().__init__()

        self.setWindowTitle('Gráfico de Dispersión con KNN de Predicción de Puntos Jornada')

        # Crear la figura y el área de dibujo de Matplotlib
        self.fig, self.ax = plt.subplots()

        # Dibujar el gráfico de dispersión
        self.ax.scatter(X_test['SOFASCORE'], y_test, color='black', label='Real', alpha=0.3)
        self.ax.scatter(X_test['SOFASCORE'], y_pred, color='blue', label='Predicción', marker='x', alpha=0.5)
        self.ax.plot(X_test['SOFASCORE'], knn_model.predict(X_test), color='red', linewidth=2, label='KNN')

        # Configurar la leyenda y etiquetas
        self.ax.legend()
        self.ax.set_xlabel('SOFASCORE')
        self.ax.set_ylabel('puntos_Jornada')

        # Crear el lienzo para mostrar la figura de Matplotlib
        self.canvas = FigureCanvas(self.fig)

        # Botón para cerrar el cuadro de diálogo
        self.close_button = QPushButton('Cerrar', self)
        self.close_button.clicked.connect(self.accept)

        # Diseño de la interfaz
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

# Crear una instancia de ScatterPlotDialog y mostrarla
app = QApplication(sys.argv)
dialog = ScatterPlotDialog(X_test, y_test, y_pred)
dialog.exec_()

# Cerrar la aplicación al cerrar la ventana de gráfico
sys.exit(app.exec_())
