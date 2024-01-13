from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from Precios.PreciosWindow import PreciosWindow
from Puntuacion.PuntuacionWindow import PuntuacionWindow

import JSONUtil

"ENCABEZADO"
class Header(QWidget):
    def __init__ (self):
        super(Header, self).__init__()
        
        self.header_layout = QHBoxLayout()
        self.setLayout(self.header_layout)

        header_logo = QLabel()
        header_logo.setPixmap(QPixmap("./images/icono.png"))

        cerrar_sesion_button = QPushButton("Cerrar Sesion")
        cerrar_sesion_button.clicked.connect(self.cerrar_sesion)


        self.header_layout.addWidget(header_logo)
        self.header_layout.addWidget(cerrar_sesion_button)

        self.setStyleSheet("""
            QPushButton {
                background-color: #000;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px;
                max-width: 200px;
                margin: 0 auto;
            }
            QPushButton:hover {
                background-color: #222;
            }
        """)
    
    def cerrar_sesion(self):
        JSONUtil.eliminar_personal_data() #Elimino el JSON que tiene los datos
        # Crea una nueva instancia de la ventana de inicio de sesión
        from Login import Login
        self.main_window = Login()
        self.main_window.setWindowTitle("CactusPanda Predicciones Fútbol")
        self.main_window.setWindowIcon(QIcon("icono.png"))
        self.main_window.showMaximized()
        self.close()

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