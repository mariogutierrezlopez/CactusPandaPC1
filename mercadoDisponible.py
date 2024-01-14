from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import csv

with open('personal_data.json', 'r') as personal_data:
    data = json.load(personal_data)

email = data["user-data"]["email"]
password = data["user-data"]["password"]

# URL del formulario de inicio de sesión
login_url = 'https://mister.mundodeportivo.com/new-onboarding/auth/email'

# Configura el navegador
driver = webdriver.Chrome()
driver.get(login_url)

# Acepto las cookies si salen y si no hago un pass
try:
    cookies_accept_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'didomi-notice-agree-button')))
    cookies_accept_button.click()
except:
    pass

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

driver.get('https://mister.mundodeportivo.com/market')

player_list = driver.find_element(By.ID, 'list-on-sale')

players_on_sale = player_list.find_elements(By.TAG_NAME, 'li')

market_content = []

csv_file_path = './currentMarket.csv'

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