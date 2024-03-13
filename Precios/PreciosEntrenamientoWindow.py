from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from datetime import date #Para obtener la fecha de hoy
import os #para obtener el nombre de un archivo a partir de la ruta completa
import CSVUtil
from MachineLearning import MLPrecios
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import PLTUtil
class SeccionPedirDatos(QWidget):
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
            self.parent().findChild(SeccionVistaPrevia).cargarVistaPrevia()

class SeccionAlgoritmo(QWidget):
    def __init__(self):
        super().__init__()

    def init_UI(self):
        layout = QHBoxLayout()

        label = QLabel("Seleccionar algoritmo: ")
        label.setParent(self)

        opciones_algoritmo = QComboBox()
        opciones_algoritmo.setParent(self)
        opciones_algoritmo.addItems(['Selecciona un algoritmo','KNN','Árbol de decisión','Random Forest'])
        opciones_algoritmo.activated.connect(self.parent().findChild(SeccionVistaPrevia).cargarVistaPrevia)

        layout.addWidget(label)
        layout.addWidget(opciones_algoritmo)

        self.setLayout(layout)

class SeccionVistaPrevia(QWidget):
    def __init__(self):
        super().__init__()
    
    def init_UI(self):
        layout = QHBoxLayout()
        self.setFixedHeight(150)

        vista_previa_text = QTextEdit()
        vista_previa_text.setFixedWidth(460)
        vista_previa_text.setParent(self)
        screen_width = QApplication.primaryScreen().size().width()
        vista_previa_text.setLineWidth(screen_width*0.1)
        vista_previa_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        tabla_csv = TablaEjemplaresCSV()
        tabla_csv.setParent(self)



        layout.addWidget(vista_previa_text)
        layout.addWidget(tabla_csv)
        layout.addStretch()
        self.setLayout(layout)

    #Método que carga toda la información del archivo csv y el algoritmo en la pantalla
    def cargarVistaPrevia(self):
        
        ruta_fichero = self.parent().findChild(QLineEdit).text()
        algoritmo_seleccionado = self.parent().findChild(QComboBox).currentText()
        vista_previa_text = self.findChild(QTextEdit)
        vista_previa_text.clear()
        vista_previa_text.setReadOnly(True)
        text = ""

        if not ruta_fichero:
            text += 'Vista previa\nSelecciona un fichero para empezar'

        elif(algoritmo_seleccionado == 'Selecciona un algoritmo'):
            text += "Vista previa\n" + algoritmo_seleccionado

        else:
            #Cargar el texto de vista previa
            text += "Vista previa\n"
            text += "Fecha: " + str(date.today()) + "\n";
            text += "Nombre del fichero: " + os.path.basename(ruta_fichero) + "\n"
            text += "Ejemplares: " + str(CSVUtil.contar_ejemplares(ruta_fichero)) + "\n"
            text += "Tamaño del fichero: " + str(CSVUtil.obtener_tamano_archivo(ruta_fichero)) + "KB\n"
            text += "Algoritmo seleccionado: " + algoritmo_seleccionado + "\n"

            # Eliminar el Stretch para mostrar la tabla
            layout = self.layout()
            if layout.count() > 2:  # al menos 2 elementos (TextEdit y Tabla)
                layout.takeAt(layout.count() - 1).widget()

            #Mostrar la tabla
            self.findChild(TablaEjemplaresCSV).setVisible(True)
            self.findChild(TablaEjemplaresCSV).cargarDatos(ruta_fichero)

        #Cargar el texto
        vista_previa_text.append(text)

        #Poner "Vista previa" en negrita
        char_format = QTextCharFormat()
        char_format.setFontWeight(QFont.Weight.Bold)
        cursor = vista_previa_text.textCursor()
        cursor.setPosition(text.find("Vista previa"), QTextCursor.MoveAnchor)
        cursor.setPosition(cursor.position() + len("Vista previa"), QTextCursor.KeepAnchor)
        cursor.setCharFormat(char_format)

class TablaEjemplaresCSV(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setVisible(False)
        
    def cargarDatos(self, ruta_archivo):
        columnas = CSVUtil.obtener_titulos_csv(ruta_archivo)
        datos = CSVUtil.obtener_primeras_filas_csv(ruta_archivo)

        self.setColumnCount(len(columnas))
        self.setRowCount(len(datos))

        self.setHorizontalHeaderLabels(columnas)

        
        for row, rowData in enumerate(datos):
            for col, value in enumerate(rowData):
                item = QTableWidgetItem(value)
                self.setItem(row, col, item)
        
        self.resizeColumnsToContents()
        
        # Ajustar el tamaño de la fila según su contenido
        for row in range(self.rowCount()):
            self.resizeRowToContents(row)
        self.viewport().update()
        self.updateGeometry()

class BotonEjecutar(QPushButton):
    modelo = None
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.ejecutar)
        self.setText("Ejecutar")

    def ejecutar(self):
        self.seccionResultado = self.parent().findChild(SeccionResultado)
        print("Se esta ejecutando")
        ruta_fichero = self.parent().findChild(QLineEdit).text()
        algoritmo = self.parent().findChild(QComboBox).currentText()
        if not ruta_fichero:
            #Mostrar un mensaje de error
            mensaje = QMessageBox(self)
            mensaje.setWindowTitle('Error')
            mensaje.setText('Inserte un archivo CSV')
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()

        elif(algoritmo == 'Selecciona un algoritmo'):
            #Mostrar un mensaje de error
            mensaje = QMessageBox(self)
            mensaje.setWindowTitle('Error')
            mensaje.setText('Seleccione un algoritmo')
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
        else: #Si se han expecificado los 
            print("todo correcto")
        #'KNN','Árbol de decisión','Random Forest'
        seccion_resultado = self.parent().findChild(SeccionResultado)
        if(self.parent().findChild(QComboBox).currentText() == 'KNN'):
            self.modelo = MLPrecios.knn(ruta_fichero=ruta_fichero)
            seccion_resultado.knn()
            print("knn")
        elif(self.parent().findChild(QComboBox).currentText() == 'Árbol de decisión'):
            self.modelo = MLPrecios.arbol_decision(ruta_fichero=ruta_fichero)
            seccion_resultado.decision_tree()
            print("redes decision")
        elif(self.parent().findChild(QComboBox).currentText() == 'Random Forest'):
            self.modelo = MLPrecios.random_forest(ruta_fichero=ruta_fichero)
            seccion_resultado.random_forest()
            print("random forest")

class SeccionResultado(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        layout = QVBoxLayout()

        label = QLabel("Gráfica:")
        label.setParent(self)

        self.figure, self.ax = plt.subplots()

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(label)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.grafica_vacia()

    def grafica_vacia(self):
        PLTUtil.grafica_vacia(self.ax)

    def knn(self):
        PLTUtil.knn_precios(self.ax)  # Pasa el eje a la función knn_precios
        self.canvas.draw()
    def decision_tree(self):
        PLTUtil.decision_tree_precios(self.ax)
        self.canvas.draw()
    
    def random_forest(self):
        PLTUtil.random_forest_precios(self.ax)
        self.canvas.draw()

class BotonExportar(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Exportar modelo")
        self.clicked.connect(self.exportar)

    def exportar(self):
        modelo = self.parent().findChild(BotonEjecutar).modelo
        if modelo is not None:
            # Obtener el nombre del archivo del usuario
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Guardar modelo", "", "Archivos (*.joblib);", options=options)
            if fileName:
                MLPrecios.exportar_modelo(modelo = modelo, ruta_fichero = fileName)
                mensaje = QMessageBox(self)
                mensaje.setWindowTitle('Éxito')
                mensaje.setText('El modelo se ha guardado correctamente')
                mensaje.setIcon(QMessageBox.Information)
                mensaje.setStandardButtons(QMessageBox.Ok)
                mensaje.exec_()
        else:
            # Mostrar un mensaje de error si no hay modelo
            mensaje = QMessageBox(self)
            mensaje.setWindowTitle('Error')
            mensaje.setText('No hay un modelo para exportar. Ejecuta un algoritmo primero.')
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
        

class EntrenamientoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        pedir_datos = SeccionPedirDatos()
        pedir_algoritmo = SeccionAlgoritmo()
        vista_previa = SeccionVistaPrevia()
        ejecutar = BotonEjecutar()
        seccion_resultado = SeccionResultado()
        exportar = BotonExportar()

        layout = QVBoxLayout()
        layout.addWidget(pedir_datos)
        layout.addWidget(pedir_algoritmo)
        layout.addWidget(vista_previa)
        layout.addWidget(ejecutar)
        layout.addWidget(seccion_resultado)
        layout.addStretch()
        layout.addWidget(exportar)
        self.setLayout(layout)

        # Establecer la política de tamaño del widget contenedor
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Establecer padres después de que se hayan creado las instancias
        vista_previa.setParent(self)
        pedir_datos.setParent(self)
        pedir_algoritmo.setParent(self)
        ejecutar.setParent(self)
        seccion_resultado.setParent(self)
        exportar.setParent(self)
        # Llamar al método init_UI de SeccionVistaPrevia después de establecer los padres
        vista_previa.init_UI()
        pedir_datos.init_UI('Fuente de datos para precios: ')
        pedir_algoritmo.init_UI()

        vista_previa.cargarVistaPrevia()