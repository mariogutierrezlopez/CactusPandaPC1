import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from EntrenamientoWindow import EntrenamientoWindow
from PrediccionWindow import PrediccionWindow

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

        # Crear el QTabWidget
        self.tabs = QTabWidget()

        # Crear widgets para las pestañas
        tab1 = EntrenamientoWindow()
        tab2 = PrediccionWindow()

        # Agregar contenido a las pestañas
        self.tabs.addTab(tab1, "Entrenamiento")
        self.tabs.addTab(tab2, "Predicción")


        # Crear un widget central para la ventana y establecer el QTabWidget como widget central
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(header)
        central_layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)

        # Ajustar el tamaño de la fuente de los títulos de las pestañas
        font = self.tabs.tabBar().font()
        font.setPointSize(14)  # Establecer el tamaño de la fuente de las pestañas
        self.tabs.tabBar().setFont(font)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("CactusPanda Predicciones Fútbol")
    window.setWindowIcon(QIcon("icono.png"))
    # Establecer la ventana para que ocupe toda la pantalla
    window.showMaximized()
    
    sys.exit(app.exec())
