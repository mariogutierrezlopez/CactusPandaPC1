from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from .PreciosPrediccionWindow import PrediccionWindow
from .PreciosEntrenamientoWindow import EntrenamientoWindow

class PreciosWindow(QTabWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Crear widgets para las pestañas
        tab1 = EntrenamientoWindow()
        tab2 = PrediccionWindow()

        # Agregar contenido a las pestañas
        self.addTab(tab1, "Entrenamiento")
        self.addTab(tab2, "Predicción")
