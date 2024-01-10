from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

import JSONUtil;

class Login(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        email = QLineEdit()
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        boton = QPushButton("Iniciar sesión")
        boton.clicked.connect(self.iniciar_sesion)

        email.setParent(self)
        email.setParent(self)

        layout = QVBoxLayout()

        layout.addWidget(email)
        layout.addWidget(password)
        layout.addWidget(boton)

        self.setLayout(layout)

    def verificar_datos(self, email, password):
        #TODO linkear archivos luis selenium
        return False
    

    def iniciar_sesion(self):
        email = self.findChildren(QLineEdit)[0].text()
        password = self.findChildren(QLineEdit)[1].text()
        print(email)
        print(password)

        if(self.verificar_datos(email=email, password=password)):
            JSONUtil.guardarDatos(email=email, password=password)
        else:
            mensaje = QMessageBox(self)
            mensaje.setWindowTitle('Error')
            mensaje.setText('Datos de inicio de sesión incorrectos')
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()

