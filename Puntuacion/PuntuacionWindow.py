from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from .PuntuacionEntrenamientoWindow import EntrenamientoWindow
from .PuntuacionPrediccionWindow import PrediccionWindow

class PuntuacionWindow(QTabWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        entrenamiento = EntrenamientoWindow()
        prediccion = PrediccionWindow()

        self.addTab(entrenamiento, "Entrenamiento")
        self.addTab(prediccion, "Predicción")
