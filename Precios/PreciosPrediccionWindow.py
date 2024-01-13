from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

import JSONUtil
from MachineLearning import MLPrecios

class SeccionEjemplaresPredecir(QWidget):
    def __init__(self):
        super().__init__()
        self.ruta_fichero = ""

    def init_UI(self, texto):
        label = QLabel(texto)
        label.setParent(self)

        checkbox = QCheckBox('Predecir mi equipo')
        checkbox.clicked.connect(self.handle_checkbox_clicked)
        checkbox.setChecked(True)
        checkbox.setParent(self)

        ruta_fichero_QLE = QLineEdit()
        ruta_fichero_QLE.setParent(self)
        ruta_fichero_QLE.setReadOnly(True)
        ruta_fichero_QLE.setEnabled(False)

        boton_explorar = QPushButton('Explorar', self)
        boton_explorar.setParent(self)
        boton_explorar.clicked.connect(self.abrir_explorador)
        boton_explorar.setEnabled(False)

        layout = QHBoxLayout()
        layout.addWidget(checkbox)
        layout.addWidget(label)
        layout.addWidget(ruta_fichero_QLE)
        layout.addWidget(boton_explorar)

        self.setLayout(layout)

    def handle_checkbox_clicked(self, state):
        ruta_fichero_QLE = self.findChild(QLineEdit)
        boton_explorar = self.findChild(QPushButton)
        if state:
            ruta_fichero_QLE.setEnabled(False)
            boton_explorar.setEnabled(False)
        else:
            ruta_fichero_QLE.setEnabled(True)
            boton_explorar.setEnabled(True)
    
    def abrir_explorador(self):
        options = QFileDialog.Options()

        filtro = "Archivos CSV (*.CSV)"
        
        fname, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo CSV', '/home', filtro, options=options)

        if fname:
            print(f'Selected file: {fname}')
            ruta_fichero_QLE = self.findChild(QLineEdit)
            ruta_fichero_QLE.setText(fname)

class SeccionModelo(QWidget):
    def __init__(self):
        super().__init__()
        self.ruta_fichero = ""

    def init_UI(self, texto):
        label = QLabel(texto)
        label.setParent(self)

        ruta_fichero_QLE = QLineEdit()
        ruta_fichero_QLE.setParent(self)
        ruta_fichero_QLE.setReadOnly(True)

        boton_explorar = QPushButton('Explorar', self)
        boton_explorar.setParent(self)
        boton_explorar.clicked.connect(self.abrir_explorador)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(ruta_fichero_QLE)
        layout.addWidget(boton_explorar)

        self.setLayout(layout)
    
    def abrir_explorador(self):
        options = QFileDialog.Options()

        filtro = "Archivos JOLIB (*.joblib)"
        
        fname, _ = QFileDialog.getOpenFileName(self, 'Abrir modelo de entrenamiento', '/home', filtro, options=options)

        if fname:
            print(f'Selected file: {fname}')
            ruta_fichero_QLE = self.findChild(QLineEdit)
            ruta_fichero_QLE.setText(fname)
            #self.parent().findChild(SeccionVistaPrevia).cargarVistaPrevia()

class BotonPredecir(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText('Predecir datos')
        self.clicked.connect(self.predecir)

        self.resultado = None

    def predecir(self):
        datosMiEquipo = self.parent().findChild(QCheckBox).isChecked()
        rutaFicheros = self.parent().findChildren(QLineEdit)
        fichero_csv = rutaFicheros[0].text()
        fichero_modelo = rutaFicheros[1].text()

        if(datosMiEquipo and fichero_modelo):
            df = JSONUtil.get_players_data_to_dataframe()
            df_predecir = df.drop(['ID', 'Nombre', 'Price'], axis=1)
            resultado_modelo = MLPrecios.predecir(modelo = MLPrecios.importar_modelo(fichero_modelo), ejemplares=df_predecir)
            
            df.insert(3, 'Precio predecido', resultado_modelo)

            print(df['Precio predecido'])
            print(df.columns)

            tabla_predicciones = self.parent().findChild(TablaPredicciones)
            tabla_predicciones.cargarDatos(df)
            

        elif(not datosMiEquipo and fichero_csv and fichero_modelo):
            print("true")
        else:
            mensaje = QMessageBox(self)
            mensaje.setWindowTitle('Error')
            mensaje.setText('Faltan datos para predecir')
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setStandardButtons(QMessageBox.Ok)  # Utiliza un botón estándar como Ok
            mensaje.exec_()

class TablaPredicciones(QTableWidget):
    def __init__(self):
        super().__init__()
        self.cargarEstructuraInicial()

    def cargarEstructuraInicial(self):
        columnas = ['Futbolista', 'Precio hoy', 'Predicción precio']
        self.setColumnCount(len(columnas))
        self.setRowCount(1)
        self.setHorizontalHeaderLabels(columnas)

        for col, columna in enumerate(columnas):
            item = QTableWidgetItem(columna)
            self.setItem(0, col, item)

        self.resizeColumnsToContents()
        for row in range(self.rowCount()):
            self.resizeRowToContents(row)
        self.viewport().update()
        self.updateGeometry()

    def cargarDatos(self, df):
        # Establecer el número de filas y columnas en la tabla
        self.setRowCount(len(df))
        self.setColumnCount(len(df.columns))

        # Establecer las etiquetas de encabezado horizontal
        self.setHorizontalHeaderLabels(df.columns)

        col_precio_hoy = None
        col_precio_predecido = df.columns.get_loc('Precio predecido')
        col_precio_hoy = df.columns.get_loc('Price')

        # Llenar la tabla con datos del DataFrame
        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iloc[row, col]))

                # Resaltar la columna 'Precio predecido' en negrita
                if col == col_precio_predecido:
                    item.setFont(QFont("Arial", 10, QFont.Bold))

                    # Comparar con 'Precio hoy' y asignar color si la columna 'Precio hoy' está presente
                    if col_precio_hoy is not None:
                        precio_hoy = float(df.iloc[row, col_precio_hoy])
                        precio_predecido = float(df.iloc[row, col_precio_predecido])

                        if precio_predecido > precio_hoy:
                            item.setForeground(QColor(0, 0, 0))
                            item.setBackground(QColor(170, 255, 128))  # Fondo verde
                        elif precio_predecido < precio_hoy:
                            item.setForeground(QColor(0, 0, 0))
                            item.setBackground(QColor(255, 102, 102))  # Fondo rojo
                    else:
                        print("Hello")
                self.setItem(row, col, item)

        self.resizeColumnsToContents()
        for row in range(self.rowCount()):
            self.resizeRowToContents(row)
        self.viewport().update()
        self.updateGeometry()

class BotonExportar(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Exportar resultados")
        self.clicked.connect(self.exportar)

    def exportar(self):
        # Obtener el nombre del archivo del usuario
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Guardar modelo", "", "Archivos (*.xlsx);;Todos los archivos (*)", options=options)

        if fileName:
            # Aquí es donde deberías realizar la lógica de exportación de tu modelo.
            # fileName contiene la ruta del archivo seleccionado por el usuario.
            print(f"Exportando modelo a: {fileName}")
        


class PrediccionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()
    
    def init_UI(self):
        layout = QVBoxLayout()
        seccion_ejemplares_predecir = SeccionEjemplaresPredecir()
        seccion_modelo = SeccionModelo()
        boton_predecir = BotonPredecir()
        tabla = TablaPredicciones()
        boton_exportar = BotonExportar()

        layout.addWidget(seccion_ejemplares_predecir)
        layout.addWidget(seccion_modelo)
        layout.addWidget(boton_predecir)
        layout.addWidget(tabla)
        layout.addStretch()
        layout.addWidget(boton_exportar)

        seccion_ejemplares_predecir.init_UI('Ejemplares a predecir: ')
        seccion_modelo.init_UI('Modelo a aplicar: ')

        seccion_ejemplares_predecir.setParent(self)
        seccion_modelo.setParent(self)
        boton_predecir.setParent(self)
        tabla.setParent(self)
        boton_exportar.setParent(self)

        self.setLayout(layout)