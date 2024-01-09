import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from Precios.PreciosWindow import PreciosWindow
from Puntuacion.PuntuacionWindow import PuntuacionWindow

"ENCABEZADO"
class Header(QWidget):
    def __init__ (self):
        super(Header, self).__init__()
        
        self.header_layout = QHBoxLayout()
        self.setLayout(self.header_layout)

        header_logo = QLabel()
        header_logo.setPixmap(QPixmap("./images/icono.png"))

        self.header_layout.addWidget(header_logo)



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        header = Header()
        header.show()

        "Pestañas"
        self.tabs = QTabWidget()

        precios = PreciosWindow()
        puntuacion = PuntuacionWindow()

        self.tabs.addTab(precios, "Precios")
        self.tabs.addTab(puntuacion, "Puntuacion")
        # Crear un widget central para la ventana y establecer el QTabWidget como widget central
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(header)
        central_layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)

        # # Ajustar el tamaño de la fuente de los títulos de las pestañas
        # font = self.tabs.tabBar().font()
        # font.setPointSize(14)  # Establecer el tamaño de la fuente de las pestañas
        # self.tabs.tabBar().setFont(font)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("CactusPanda Predicciones Fútbol")
    window.setWindowIcon(QIcon("icono.png"))
    # Establecer la ventana para que ocupe toda la pantalla
    window.showMaximized()
    
    sys.exit(app.exec())
