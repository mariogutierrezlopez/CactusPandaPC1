import json
import os
import pandas as pd

fichero = "./personal_data.json"

def guardarDatos(email, password):
    # Cargar el JSON existente desde el archivo o crear una estructura vacía si el archivo no existe
    try:
        with open(fichero, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error, no se ha encontrado el fichero")

    # Actualizar los datos con la nueva información
    data["user-data"]["email"] = email
    data["user-data"]["password"] = password

    # Guardar los datos actualizados en el archivo
    with open(fichero, 'w') as file:
        json.dump(data, file, indent=2)

def get_personal_data():
    # Leer datos desde el archivo personal_data.json
    with open('personal_data.json', 'r', encoding='utf-8') as archivo_json:
        data = json.load(archivo_json)

    return data

def eliminar_personal_data():
    # Ruta del archivo personal_data.json en el mismo directorio
    archivo_path = 'personal_data.json'

    try:
        # Intentar eliminar el archivo
        os.remove(archivo_path)
        print(f"El archivo {archivo_path} ha sido eliminado.")
    except FileNotFoundError:
        print(f"El archivo {archivo_path} no existe.")
    except Exception as e:
        print(f"Error al intentar eliminar el archivo: {e}")

def existe_personal_data():
    return os.path.exists('personal_data.json')

def create_personal_data(email, password):
    data = {
        "user-data": {
            "password": email,
            "email": password
        },
        "formations": {
            "free": ["4-4-2", "4-5-1", "4-3-3", "3-4-3", "3-5-2", "5-4-1", "5-3-2"],
            "premium": ["4-2-4", "4-6-0", "3-3-4", "3-6-1", "5-5-0"]
        }
    }

    return data

def save_data(data):

    with open("personal_data.json", 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2)

# def update_data(data):

def get_datos_por_id(id):
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv('./data/exactPricesPlayer_23-24.csv')

    # Filtrar las filas que coincidan con el ID
    fila_id_buscado = df[df['Id'] == id]

    # Obtener la última fila que coincida con el ID
    ultima_fila_id_buscado = fila_id_buscado.iloc[-1]

    return ultima_fila_id_buscado

def get_players_data_to_dataframe():
    with open('personal_data.json', 'r', encoding='utf-8') as archivo_json:
        data = json.load(archivo_json)

    player_ids = data["plantilla"]["all_player"]
    df_resultado = pd.DataFrame()
    for player_id in player_ids:
        datos_player = get_datos_por_id(player_id)
        df_resultado = df_resultado._append({'ID': player_id, 'Nombre': datos_player['Name'],'Price': datos_player['Price'], 'AveragePoints': datos_player['AveragePoints'], 
                   'Goals': datos_player['Goals'], 'Matches': datos_player['Matches'], 'AveragePtsLastThreeMatches': datos_player['AveragePtsLastThreeMatches'],
                   'AverageCardsLastThreeMatches': datos_player['AverageCardsLastThreeMatches']}, ignore_index=True)
    
    return df_resultado
