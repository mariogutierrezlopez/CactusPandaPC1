import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from Login import Login

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.setWindowTitle("CactusPanda Predicciones Fútbol")
    window.setWindowIcon(QIcon("icono.png"))
    # Establecer la ventana para que ocupe toda la pantalla
    window.showMaximized()
    
    sys.exit(app.exec())
