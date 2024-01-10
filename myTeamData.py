#TODO boton de actualizar y linkear con el codigo de login.py

import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import json


def is_valid_email(email):
    # Define una expresión regular para validar un correo electrónico
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Comprueba si el correo electrónico es válido
    if re.fullmatch(regex, email):
        return True
    else:
        return False


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

data["last-update"] = datetime.now().strftime('%Y-%m-%d') #TODO sacar hora de aqui

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

# Guardar el JSON actualizado en el archivo
with open('personal_data.json', 'w') as archivo_json:
    json.dump(data, archivo_json, indent=2)
