from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QLabel

class VentanaInformacion(QWidget):
    def __init__(self, informacion):
        super().__init__()

    def mostrarInformacion(self):
        print(f'Información adicional: {informacion}')

class TablaConBotones(QTableWidget):
    def __init__(self):
        super().__init__()

    def cargarDatos(self):
        columnas = ['Futbolista', 'Precio hoy', 'Predicción precio', 'Puntos hoy', 'Predicción puntos', 'Acción']
        informacion_extra = [
            "Información adicional para el futbolista 1",
            "Información adicional para el futbolista 2",
            "Información adicional para el futbolista 3",
            "Información adicional para el futbolista 4",
            "Información adicional para el futbolista 5"
        ]

        # Establecer el número de columnas y sus etiquetas
        self.setColumnCount(len(columnas))
        self.setHorizontalHeaderLabels(columnas)

        # Ajustar el tamaño de las columnas
        self.resizeColumnsToContents()

        # Establecer el número de filas
        self.setRowCount(len(informacion_extra))

        # Añadir celdas con los nombres de las columnas y botones de información
        for row, info_extra in enumerate(informacion_extra):
            for col, columna in enumerate(columnas):
                if col == len(columnas) - 1:
                    # Añadir un botón 'Más Información' en la última columna
                    boton = QPushButton('Más Información')
                    self.setCellWidget(row, col, boton)
                    boton.clicked.connect(self.mostrarInformacion)
                else:
                    # Añadir el contenido de la celda
                    item = QTableWidgetItem(f'{columna} {row}')
                    self.setItem(row, col, item)

        # Ajustar el tamaño de la fila según su contenido
        for row in range(self.rowCount()):
            self.resizeRowToContents(row)

        # Actualizar la vista y la geometría
        self.viewport().update()
        self.updateGeometry()

if __name__ == '__main__':
    app = QApplication([])

    tabla_con_botones = TablaConBotones()

    app.exec_()