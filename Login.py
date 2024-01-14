from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import re
import json
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

from MainWindow import MainWindow
import JSONUtil


class Login(QWidget):
    def __init__(self):
        super().__init__()
        existe_usuario = JSONUtil.existe_personal_data()
        if(existe_usuario):
            self.initUIRegistrado()
        else:
            self.initUINuevo()

    def initUIRegistrado(self):
        data = JSONUtil.get_personal_data()
        layout = QFormLayout()
        logo = QLabel()
        logo.setPixmap(QPixmap("./images/icono.png"))
        logo.setAlignment(Qt.AlignCenter)
        layout.addRow(logo)
        layout.addWidget(QLabel("Se ha encontrado una sesion abierta"))
        layout.addWidget(QLabel("Email: " + data["user-data"]["email"]))
        layout.addWidget(QLabel("Ultima actualización: " + data['last-update']))

        actualizar_datos_button = QPushButton("Actualizar datos y entrar")
        actualizar_datos_button.clicked.connect(self.actualizar_datos)

        cerrar_sesion_button = QPushButton("Cerrar sesion")
        cerrar_sesion_button.clicked.connect(self.cerrar_sesion)
        
        layout.addWidget(actualizar_datos_button)
        layout.addWidget(cerrar_sesion_button)
        layout.setFormAlignment(Qt.AlignCenter)
        layout.setLabelAlignment(Qt.AlignCenter)

        # Establecer márgenes proporcionales al espacio disponible
        margen_proporcional = 1 # Ajusta según sea necesario

        # Obtener el ancho y alto de la ventana
        ancho_ventana = self.width()
        alto_ventana = self.height()

        # Calcular los márgenes proporcionales
        margen_izquierdo = ancho_ventana * margen_proporcional
        margen_derecho = ancho_ventana * margen_proporcional
        margen_superior = alto_ventana * margen_proporcional
        margen_inferior = alto_ventana * margen_proporcional

        # Establecer márgenes
        layout.setContentsMargins(margen_izquierdo, 0, margen_derecho, 0)
       


        self.setLayout(layout)
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QPushButton {
                padding: 5px;
                margin: 5px;
                font-size: 14px;
                max-width: 300px;
                margin: 0 auto;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px;
                max-width: 300px;
                margin: 0 auto;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
    def initUINuevo(self):

        logo = QLabel()
        logo.setPixmap(QPixmap("./images/icono.png"))
        logo.setAlignment(Qt.AlignCenter)
        self.email = QLineEdit()
        self.email.setPlaceholderText('Correo electrónico')
        self.password = QLineEdit()
        self.password.setPlaceholderText('Contraseña')
        self.password.setEchoMode(QLineEdit.Password)
        self.boton = QPushButton("Iniciar sesión")
        self.boton.clicked.connect(self.iniciar_sesion)

        self.layout = QFormLayout(self)
        self.layout.addRow(logo)
        self.layout.addRow(self.email)
        self.layout.addRow(self.password)
        self.layout.addRow(self.boton)
        self.layout.setFormAlignment(Qt.AlignCenter)
        self.layout.setLabelAlignment(Qt.AlignRight)

        # Establecer márgenes proporcionales al espacio disponible
        margen_proporcional = 1 # Ajusta según sea necesario

        # Obtener el ancho y alto de la ventana
        ancho_ventana = self.width()
        alto_ventana = self.height()

        # Calcular los márgenes proporcionales
        margen_izquierdo = ancho_ventana * margen_proporcional
        margen_derecho = ancho_ventana * margen_proporcional
        margen_superior = alto_ventana * margen_proporcional
        margen_inferior = alto_ventana * margen_proporcional

        # Establecer márgenes
        self.layout.setContentsMargins(margen_izquierdo, 0, margen_derecho, 0)
       

        self.setLayout(self.layout)

        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QPushButton {
                padding: 5px;
                margin: 5px;
                font-size: 14px;
                max-width: 300px;
                margin: 0 auto;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px;
                max-width: 300px;
                margin: 0 auto;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
    
    def cerrar_sesion(self):
        JSONUtil.eliminar_personal_data()  # Elimino el JSON que tiene los datos
        self.main_window = Login()
        self.main_window.setWindowTitle("CactusPanda Predicciones Fútbol")
        self.main_window.setWindowIcon(QIcon("icono.png"))
        self.main_window.showMaximized()
        self.close()

    def actualizar_datos(self):
        self.show_loading_dialog('Actualizando datos...')
        self.actualizarSeleniumThread = ActualizarSeleniumThread()  # Crear una instancia del hilo
        self.actualizarSeleniumThread.actualizar_datos_finished.connect(self.mostrar_main_window)  # Conectar la señal
        self.actualizarSeleniumThread.start()  # Iniciar el hilo

        

    def mostrar_main_window(self):
        self.hide_loading_dialog()

        self.main_window = MainWindow()
        self.main_window.setWindowTitle("CactusPanda Predicciones Fútbol")
        self.main_window.setWindowIcon(QIcon("icono.png"))
        self.main_window.showMaximized()
        self.close()
        

    def iniciar_sesion(self):
        email = self.email.text()
        password = self.password.text()

        # Crear una instancia del hilo de Selenium y conectar señales
        self.selenium_thread = SeleniumThread(email, password)
        self.selenium_thread.finished.connect(self.verificacion_terminada)
        self.selenium_thread.start()

        self.show_loading_dialog('Verificando datos...')
        # Mostrar la ventana de carga aquí si es necesario

    def verificacion_terminada(self, result):
        # Método que se ejecutará cuando la verificación en el hilo de Selenium haya terminado
        self.hide_loading_dialog()
        if result:
            JSONUtil.guardarDatos(email=self.email.text(), password=self.password.text())
            # Mostrar la ventana principal después de una sesión exitosa
            self.main_window = MainWindow()
            self.main_window.setWindowTitle("CactusPanda Predicciones Fútbol")
            self.main_window.setWindowIcon(QIcon("icono.png"))
            self.main_window.showMaximized()
            self.close()
        else:
            mensaje = QMessageBox(self)
            mensaje.setWindowTitle('Error')
            mensaje.setText('Datos de inicio de sesión incorrectos')
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
    
    def show_loading_dialog(self, texto):
        self.loading_dialog = QProgressDialog(self)
        self.loading_dialog.setLabelText(texto)
        self.loading_dialog.setCancelButton(None)
        self.loading_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.loading_dialog.setRange(0, 0)
        self.loading_dialog.show()

    def hide_loading_dialog(self):
        self.loading_dialog.close()

class SeleniumThread(QThread):
    finished = Signal(bool)

    def __init__(self, email, password):
        super().__init__()
        self.email = email
        self.password = password

    def run(self):
        # Lógica de verificación con Selenium
        result = self.verificar_datos(self.email, self.password)
        self.finished.emit(result)

    def verificar_datos(self, email, password):
        login_url = 'https://mister.mundodeportivo.com/new-onboarding/auth/email'

        driver = webdriver.Chrome()
        driver.minimize_window()

        try:
            driver.get(login_url)

            # Aceptar las cookies si aparecen
            cookies_accept_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'didomi-notice-agree-button')))
            cookies_accept_button.click()

            print(f'Welcome {email} con pass {password}')

            # Encontrar el campo de correo electrónico y contraseña e ingresar los datos
            email_field = driver.find_element(By.ID, 'email')
            password_field = driver.find_element(By.XPATH, '//input[@placeholder="Contraseña"]')

            email_field.send_keys(email)
            password_field.send_keys(password)

            # Enviar el formulario
            password_field.send_keys(Keys.RETURN)

            # Esperar a que se cargue la página después de enviar el formulario
            WebDriverWait(driver, 10).until(EC.url_changes(login_url))
            print(driver.current_url)
            # Verificar si la página después de enviar el formulario es la página de inicio
            if driver.current_url == 'https://mister.mundodeportivo.com/feed':
                print("Se ha entrado aqui")
                resultado = True
                data = JSONUtil.create_personal_data(email=email, password=password)
                # Haz clic en el botón "Omitir tutorial" en caso de que salga y si no hago un pass
                try:
                    skip_tutorial_button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'btn-tutorial-skip')))
                    skip_tutorial_button.click()
                except:
                    pass

                next_match = driver.find_element(By.CLASS_NAME, 'gameweek__name').text.strip()

                time_remaining = driver.find_element(By.CLASS_NAME, 'gameweek__detail').text.strip()

                driver.get('https://mister.mundodeportivo.com/team')

                time.sleep(2)

                real_balance = driver.find_element(By.CLASS_NAME, 'balance-real-current').text.strip()
                future_balance = driver.find_element(By.CLASS_NAME, 'balance-real-future').text.strip()
                max_debt = driver.find_element(By.CLASS_NAME, 'balance-real-maxdebt').text.strip()

                lineup_team = driver.find_element(By.CLASS_NAME, 'team__lineup')

                starting_team = lineup_team.find_element(By.CLASS_NAME, 'lineup-starting')

                gk = [ ]

                gk_line = starting_team.find_element(By.CLASS_NAME, 'line-1')
                players = gk_line.find_elements(By.TAG_NAME, 'button')

                for p in players:
                    gk.append(int(p.get_attribute('data-id_player')))

                defense = [ ]

                defense_line = starting_team.find_element(By.CLASS_NAME, 'line-2')
                players = defense_line.find_elements(By.TAG_NAME, 'button')

                for p in players:
                    defense.append(int(p.get_attribute('data-id_player')))

                mid = []

                mid_line = starting_team.find_element(By.CLASS_NAME, 'line-3')
                players = mid_line.find_elements(By.TAG_NAME, 'button')

                for p in players:
                    mid.append(int(p.get_attribute('data-id_player')))

                attack = [ ]

                attack_line = starting_team.find_element(By.CLASS_NAME, 'line-4')
                players = attack_line.find_elements(By.TAG_NAME, 'button')

                for p in players:
                    attack.append(int(p.get_attribute('data-id_player')))

                actual_team = [gk, defense, mid, attack]
                actual_formation = driver.find_element(By.CLASS_NAME, 'lineup-formation-subs').find_element(By.CLASS_NAME, 'btn-popup')

                plantilla = driver.find_element(By.CLASS_NAME, 'player-list').find_elements(By.TAG_NAME, 'li')
                link_players = [ ]

                for p in plantilla:
                    expresion_regex = r'/players/(\d+)'

                    # Intentar encontrar la coincidencia en la URL actual
                    match = re.search(expresion_regex, p.find_element(By.TAG_NAME, 'a').get_attribute('href'))

                    player_id = None

                    if match:
                        player_id = int(match.group(1))
                    else:
                        print('No id')

                    link_players.append(player_id)

                if "jornada-data" not in data:
                    data["jornada-data"] = {}

                if "money-data" not in data:
                    data["money-data"] = {}

                if "plantilla" not in data:
                    data["plantilla"] = {}

                if 'actual-formation' not in data['plantilla']:
                    data['plantilla']['actual-formation'] = {}

                if 'team' not in data['plantilla']['actual-formation']:
                    data['plantilla']['actual-formation']['team'] = {}

                if 'all_player' not in data['plantilla']:
                    data['plantilla']['all_player'] = {}

                data["last-update"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                data["jornada-data"]["prox-jornada"] = next_match
                data["jornada-data"]["time-remaining"] = time_remaining

                data["money-data"]["actual-money"] = int(real_balance.replace('.', ""))
                data["money-data"]["future-money"] = int(future_balance.replace('.', ""))
                data["money-data"]["max-debt"] = int(max_debt.replace('.', ""))

                data["plantilla"]["actual-formation"]["formation"] = actual_formation.text.strip()
                data["plantilla"]["actual-formation"]["team"]["gk"] = gk
                data["plantilla"]["actual-formation"]["team"]["defense"] = defense
                data["plantilla"]["actual-formation"]["team"]["mid"] = mid
                data["plantilla"]["actual-formation"]["team"]["att"] = attack
                data["plantilla"]["all_player"] = link_players

                JSONUtil.save_data(data)

                        
                driver.get('https://mister.mundodeportivo.com/market')

                player_list = driver.find_element(By.ID, 'list-on-sale')

                players_on_sale = player_list.find_elements(By.TAG_NAME, 'li')

                market_content = []

                csv_file_path = './data/currentMarket.csv'

                with open(csv_file_path, mode = 'w', newline = '', encoding = 'utf-8') as archivo_csv:
                    escritor = csv.writer(archivo_csv)

                    # Escribir encabezados
                    escritor.writerow(['PlayerId', 'PlayerName', 'PlayerPosition', 'PlayerOwner',
                                    'DataPrice', 'OwnerPrice', 'MaxPrice', 'MinPrice', 'TimeRemaining'])

                for p in players_on_sale:

                    if 'player' in p.get_attribute('class'):
                        player_id = p.find_element(By.CLASS_NAME, 'player-pic').get_attribute('data-id_player')
                        player_name = p.find_element(By.CLASS_NAME, 'btn-sw-link').get_attribute('data-title')
                        player_position = p.get_attribute('data-position')
                        data_price = p.get_attribute('data-price')
                        owner_price = p.find_element(By.CLASS_NAME, 'btn-bid').get_attribute('data-value')
                        print(owner_price)
                        max_price = int(int(owner_price) * 1.10)
                        min_price = int(int(owner_price) * 0.95)
                        player_owner = p.get_attribute('data-owner')
                        time_remaining = p.get_attribute('data-ends')

                        player = [player_id, player_name, player_position, player_owner, data_price,
                                owner_price, max_price, min_price, time_remaining]

                        with open(csv_file_path, mode = 'a', newline = '', encoding = 'utf-8') as archivo_csv:
                            escritor = csv.writer(archivo_csv)

                            # Escribir encabezados
                            escritor.writerow(player)
            else:
                resultado = False
        except Exception as e:
            print(f"Error: {e}")
            resultado = False
        finally:
            # Cerrar el navegador en cualquier 
            driver.quit()
        return resultado

class ActualizarSeleniumThread(QThread):
    actualizar_datos_finished = Signal()
    def __init__(self):
        super().__init__()
    
    def run(self):
        with open('personal_data.json', 'r') as personal_data:
            data = json.load(personal_data)

        email = data["user-data"]["email"]
        password = data["user-data"]["password"]

        # URL del formulario de inicio de sesión
        login_url = 'https://mister.mundodeportivo.com/new-onboarding/auth/email'

        # Configura el navegador
        driver = webdriver.Chrome()
        driver.minimize_window()
        driver.get(login_url)

        # Acepto las cookies si salen y si no hago un pass
        try:
            cookies_accept_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'didomi-notice-agree-button')))
            cookies_accept_button.click()
        except:
            pass

        print(f'Welcome {email} con pass {password}')

        # Encuentra el campo de correo electrónico y contraseña e ingresa los datos
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.XPATH, '//input[@placeholder="Contraseña"]')

        email_field.send_keys(email)
        password_field.send_keys(password)

        # Envía el formulario
        password_field.send_keys(Keys.RETURN)

        time.sleep(2)

        # Haz clic en el botón "Omitir tutorial" en caso de que salga y si no hago un pass
        try:
            skip_tutorial_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'btn-tutorial-skip')))
            skip_tutorial_button.click()
        except:
            pass

        next_match = driver.find_element(By.CLASS_NAME, 'gameweek__name').text.strip()

        time_remaining = driver.find_element(By.CLASS_NAME, 'gameweek__detail').text.strip()

        driver.get('https://mister.mundodeportivo.com/team')

        time.sleep(2)

        real_balance = driver.find_element(By.CLASS_NAME, 'balance-real-current').text.strip()
        future_balance = driver.find_element(By.CLASS_NAME, 'balance-real-future').text.strip()
        max_debt = driver.find_element(By.CLASS_NAME, 'balance-real-maxdebt').text.strip()

        lineup_team = driver.find_element(By.CLASS_NAME, 'team__lineup')

        starting_team = lineup_team.find_element(By.CLASS_NAME, 'lineup-starting')

        gk = [ ]

        gk_line = starting_team.find_element(By.CLASS_NAME, 'line-1')
        players = gk_line.find_elements(By.TAG_NAME, 'button')

        for p in players:
            gk.append(int(p.get_attribute('data-id_player')))

        defense = [ ]

        defense_line = starting_team.find_element(By.CLASS_NAME, 'line-2')
        players = defense_line.find_elements(By.TAG_NAME, 'button')

        for p in players:
            defense.append(int(p.get_attribute('data-id_player')))

        mid = []

        mid_line = starting_team.find_element(By.CLASS_NAME, 'line-3')
        players = mid_line.find_elements(By.TAG_NAME, 'button')

        for p in players:
            mid.append(int(p.get_attribute('data-id_player')))

        attack = [ ]

        attack_line = starting_team.find_element(By.CLASS_NAME, 'line-4')
        players = attack_line.find_elements(By.TAG_NAME, 'button')

        for p in players:
            attack.append(int(p.get_attribute('data-id_player')))

        actual_team = [gk, defense, mid, attack]
        actual_formation = driver.find_element(By.CLASS_NAME, 'lineup-formation-subs').find_element(By.CLASS_NAME, 'btn-popup')

        plantilla = driver.find_element(By.CLASS_NAME, 'player-list').find_elements(By.TAG_NAME, 'li')
        link_players = [ ]

        for p in plantilla:
            expresion_regex = r'/players/(\d+)'

            # Intentar encontrar la coincidencia en la URL actual
            match = re.search(expresion_regex, p.find_element(By.TAG_NAME, 'a').get_attribute('href'))

            player_id = None

            if match:
                player_id = int(match.group(1))
            else:
                print('No id')

            link_players.append(player_id)

        if "jornada-data" not in data:
            data["jornada-data"] = {}

        if "money-data" not in data:
            data["money-data"] = {}

        if "plantilla" not in data:
            data["plantilla"] = {}

        if 'actual-formation' not in data['plantilla']:
            data['plantilla']['actual-formation'] = {}

        if 'team' not in data['plantilla']['actual-formation']:
            data['plantilla']['actual-formation']['team'] = {}

        if 'all_player' not in data['plantilla']:
            data['plantilla']['all_player'] = {}

        data["last-update"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        data["jornada-data"]["prox-jornada"] = next_match
        data["jornada-data"]["time-remaining"] = time_remaining

        data["money-data"]["actual-money"] = int(real_balance.replace('.', ""))
        data["money-data"]["future-money"] = int(future_balance.replace('.', ""))
        data["money-data"]["max-debt"] = int(max_debt.replace('.', ""))

        data["plantilla"]["actual-formation"]["formation"] = actual_formation.text.strip()
        data["plantilla"]["actual-formation"]["team"]["gk"] = gk
        data["plantilla"]["actual-formation"]["team"]["defense"] = defense
        data["plantilla"]["actual-formation"]["team"]["mid"] = mid
        data["plantilla"]["actual-formation"]["team"]["att"] = attack
        data["plantilla"]["all_player"] = link_players

        JSONUtil.save_data(data=data)
        
        driver.get('https://mister.mundodeportivo.com/market')

        player_list = driver.find_element(By.ID, 'list-on-sale')

        players_on_sale = player_list.find_elements(By.TAG_NAME, 'li')

        market_content = []

        csv_file_path = './data/currentMarket.csv'

        with open(csv_file_path, mode = 'w', newline = '', encoding = 'utf-8') as archivo_csv:
            escritor = csv.writer(archivo_csv)

            # Escribir encabezados
            escritor.writerow(['PlayerId', 'PlayerName', 'PlayerPosition', 'PlayerOwner',
                            'DataPrice', 'OwnerPrice', 'MaxPrice', 'MinPrice', 'TimeRemaining'])

        for p in players_on_sale:

            if 'player' in p.get_attribute('class'):
                player_id = p.find_element(By.CLASS_NAME, 'player-pic').get_attribute('data-id_player')
                player_name = p.find_element(By.CLASS_NAME, 'btn-sw-link').get_attribute('data-title')
                player_position = p.get_attribute('data-position')
                data_price = p.get_attribute('data-price')
                owner_price = p.find_element(By.CLASS_NAME, 'btn-bid').get_attribute('data-value')
                print(owner_price)
                max_price = int(int(owner_price) * 1.10)
                min_price = int(int(owner_price) * 0.95)
                player_owner = p.get_attribute('data-owner')
                time_remaining = p.get_attribute('data-ends')

                player = [player_id, player_name, player_position, player_owner, data_price,
                        owner_price, max_price, min_price, time_remaining]

                with open(csv_file_path, mode = 'a', newline = '', encoding = 'utf-8') as archivo_csv:
                    escritor = csv.writer(archivo_csv)

                    # Escribir encabezados
                    escritor.writerow(player)

        driver.quit()
        self.actualizar_datos_finished.emit()