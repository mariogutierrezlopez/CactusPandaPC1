from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class SeccionEjemplaresPredecir(QWidget):
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

        filtro = "Archivos CSV (*.csv)"
        
        fname, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo CSV', '/home', filtro, options=options)

        if fname:
            print(f'Selected file: {fname}')
            ruta_fichero_QLE = self.findChild(QLineEdit)
            ruta_fichero_QLE.setText(fname)
            #self.parent().findChild(SeccionVistaPrevia).cargarVistaPrevia()

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

        filtro = "Archivos CSV (*.csv)"
        
        fname, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo CSV', '/home', filtro, options=options)

        if fname:
            print(f'Selected file: {fname}')
            ruta_fichero_QLE = self.findChild(QLineEdit)
            ruta_fichero_QLE.setText(fname)
            #self.parent().findChild(SeccionVistaPrevia).cargarVistaPrevia()

class TablaPredicciones(QTableWidget):
    def __init__(self):
        super().__init__()
        self.cargarDatos()

    def cargarDatos(self):
        columnas = ['Futbolista', 'Precio hoy', 'Predicción precio', 'Puntos hoy', 'Predicción puntos']
        #datos = CSVUtil.obtener_primeras_filas_csv(ruta_archivo)

        self.setColumnCount(len(columnas))
        self.setRowCount(1)

        self.setHorizontalHeaderLabels(columnas)

        for col, columna in enumerate(columnas):
            item = QTableWidgetItem(columna)
            self.setItem(0, col, item)
        
        self.resizeColumnsToContents()
        
        # Ajustar el tamaño de la fila según su contenido
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
        tabla = TablaPredicciones()
        boton_exportar = BotonExportar()

        layout.addWidget(seccion_ejemplares_predecir)
        layout.addWidget(seccion_modelo)
        layout.addWidget(tabla)
        layout.addStretch()
        layout.addWidget(boton_exportar)

        seccion_ejemplares_predecir.init_UI('Ejemplares a predecir: ')
        seccion_modelo.init_UI('Molode a aplicar: ')

        seccion_ejemplares_predecir.setParent(self)
        seccion_modelo.setParent(self)
        tabla.setParent(self)
        boton_exportar.setParent(self)

        self.setLayout(layout)