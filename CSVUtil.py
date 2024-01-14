import csv
import os
import pandas as pd
import sys

# Cambiar la codificación de la salida estándar
sys.stdout.reconfigure(encoding='utf-8')


def contar_ejemplares(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', newline='', encoding='utf-8') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            
            # Suponiendo que la primera fila contiene encabezados y cada fila es un ejemplar
            numero_ejemplares = sum(1 for fila in lector_csv)
            
            return numero_ejemplares
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no fue encontrado.")
        return 0
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return 0
    
def obtener_tamano_archivo(ruta):
    try:
        # Obtener el tamaño del archivo en bytes
        tamano_bytes = os.path.getsize(ruta)

        # Convertir el tamaño a kilobytes (1 KB = 1024 bytes)
        tamano_kb = tamano_bytes / 1024

        tamano_kb_aproximado = round(tamano_kb, 2)
        
        return tamano_kb_aproximado
    except FileNotFoundError:
        print(f"El archivo {ruta} no fue encontrado.")
        return None

def obtener_titulos_csv(nombre_archivo):
    with open(nombre_archivo, newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        # Leer la primera fila que contiene los títulos
        titulos = next(lector_csv, None)
    return titulos


def obtener_primeras_filas_csv(nombre_archivo, num_filas=10):
    datos = []

    with open(nombre_archivo, newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        # Saltar la primera fila que contiene los títulos
        next(lector_csv, None)

        # Leer las siguientes filas hasta el límite especificado (num_filas)
        for _ in range(num_filas):
            fila = next(lector_csv, None)
            if fila is not None:
                datos.append(fila)

    return datos

def get_market_players_dataframe():
    # Abre el archivo CSV y lee los datos
    with open('./data/currentMarket.csv', newline='', encoding='utf-8') as csvfile:
        # Crea un lector CSV
        csv_reader = csv.reader(csvfile)

        # Lee la primera línea del archivo (encabezados)
        headers = next(csv_reader)

        # Encuentra el índice de la columna 'PlayerId'
        player_id_index = headers.index('PlayerId')

        # Crea un array para almacenar las IDs de los jugadores
        player_ids = []

        # Lee cada fila y extrae la ID del jugador
        for row in csv_reader:
            player_id = int(row[player_id_index])
            player_ids.append(player_id)
    
    
    df_resultado = pd.DataFrame()
    for player_id in player_ids:
        datos_player = get_datos_por_id_precios(player_id)
        df_resultado = df_resultado._append({'ID': player_id, 'Nombre': datos_player['Name'],'Price': datos_player['Price'], 'AveragePoints': datos_player['AveragePoints'], 
                   'Goals': datos_player['Goals'], 'Matches': datos_player['Matches'], 'AveragePtsLastThreeMatches': datos_player['AveragePtsLastThreeMatches'],
                   'AverageCardsLastThreeMatches': datos_player['AverageCardsLastThreeMatches']}, ignore_index=True)
    
    return df_resultado

        
def get_datos_por_id_precios(id):
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv('./data/exactPricesPlayer_23-24.csv')

    # Filtrar las filas que coincidan con el ID
    fila_id_buscado = df[df['Id'] == id]

    # Filtrar las filas que no contengan NaN
    fila_sin_nan = fila_id_buscado[fila_id_buscado.notna().all(axis=1)]

    if(fila_sin_nan.empty):
        return fila_id_buscado.iloc[0]
    else:
        ultima_fila_sin_nan = fila_sin_nan.iloc[-1]
        return ultima_fila_sin_nan

def get_datos_por_id_puntuacion(id):
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv('./data/jugadoresFantasyActualizado.csv')

    # Filtrar las filas que coincidan con el ID
    fila_id_buscado = df[df['ID'] == id]

    # Filtrar las filas que no contengan NaN
    fila_sin_nan = fila_id_buscado[fila_id_buscado.notna().all(axis=1)]

    if fila_sin_nan.empty:
        with open('./data/currentMarket.csv', 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                if row['PlayerId'] == str(id):
                    return row
    else:
        ultima_fila_sin_nan = fila_sin_nan.iloc[-1]
        return ultima_fila_sin_nan


def get_puntuacion_mercado():
    with open('./data/currentMarket.csv', newline='', encoding='utf-8') as csvfile:
        # Crea un lector CSV
        csv_reader = csv.reader(csvfile)

        # Lee la primera línea del archivo (encabezados)
        headers = next(csv_reader)

        # Encuentra el índice de la columna 'PlayerId'
        player_id_index = headers.index('PlayerId')

        # Crea un array para almacenar las IDs de los jugadores
        player_ids = []

        # Lee cada fila y extrae la ID del jugador
        for row in csv_reader:
            player_id = int(row[player_id_index])
            player_ids.append(player_id)
        
    df_resultado = pd.DataFrame()
    for player_id in player_ids:
        datos_player = get_datos_por_id_puntuacion(player_id)
        if(isinstance(datos_player, dict)):
            df_resultado = df_resultado._append({
                    'ID': player_id,
                    'Nombre': datos_player['PlayerName'],
                    'Ultima jornada': 0,
                    'Puntos totales': 0,
                    'SOFASCORE': 0,
                    'puntos_SOFASCORE': 0,
                    'AS': 0,
                    'puntos_AS': 0,
                    'MD': 0,
                    'puntos_MD': 0,
                    'MARCA': 0,
                    'puntos_MARCA': 0,
                    'puntos_Goles': 0
                }, ignore_index=True)
        else:
            if(not pd.isna(datos_player['puntos_Jornada'])):
                df_resultado = df_resultado._append({
                    'ID': player_id,
                    'Nombre': datos_player['Name'],
                    'Ultima jornada': datos_player['Jornada'],
                    'Puntos totales': int(datos_player['puntos_Jornada']),
                    'SOFASCORE': datos_player['SOFASCORE'],
                    'puntos_SOFASCORE': int(datos_player['puntos_SOFASCORE']),
                    'AS': int(datos_player['AS']),
                    'puntos_AS': int(datos_player['puntos_AS']),
                    'MD': int(datos_player['MD']),
                    'puntos_MD': int(datos_player['puntos_MD']),
                    'MARCA': int(datos_player['MARCA']),
                    'puntos_MARCA': int(datos_player['puntos_MARCA']),
                    'puntos_Goles': int(datos_player['puntos_Goles'])
                }, ignore_index=True)
            else:
                df_resultado = df_resultado._append({
                    'ID': player_id,
                    'Nombre': datos_player['Name'],
                    'Ultima jornada': 0,
                    'Puntos totales': 0,
                    'SOFASCORE': 0,
                    'puntos_SOFASCORE': 0,
                    'AS': 0,
                    'puntos_AS': 0,
                    'MD': 0,
                    'puntos_MD': 0,
                    'MARCA': 0,
                    'puntos_MARCA': 0,
                    'puntos_Goles': 0
                }, ignore_index=True)

    
    return df_resultado

def get_custom_puntuacion():
    with open('./data/customPlayers.csv', newline='', encoding='utf-8') as csvfile:
        # Crea un lector CSV
        csv_reader = csv.reader(csvfile)

        # Lee la primera línea del archivo (encabezados)
        headers = next(csv_reader)

        # Encuentra el índice de la columna 'PlayerId'
        player_id_index = headers.index('PlayerId')

        # Crea un array para almacenar las IDs de los jugadores
        player_ids = []

        # Lee cada fila y extrae la ID del jugador
        for row in csv_reader:
            player_id = int(row[player_id_index])
            player_ids.append(player_id)
    df_resultado = pd.DataFrame()
    for player_id in player_ids:
        datos_player = get_datos_por_id_puntuacion(player_id)
        df_resultado = df_resultado._append({
                    'ID': player_id,
                    'Nombre': datos_player['Name'],
                    'Ultima jornada': datos_player['Jornada'],
                    'Puntos totales': int(datos_player['puntos_Jornada']),
                    'SOFASCORE': datos_player['SOFASCORE'],
                    'puntos_SOFASCORE': int(datos_player['puntos_SOFASCORE']),
                    'AS': int(datos_player['AS']),
                    'puntos_AS': int(datos_player['puntos_AS']),
                    'MD': int(datos_player['MD']),
                    'puntos_MD': int(datos_player['puntos_MD']),
                    'MARCA': int(datos_player['MARCA']),
                    'puntos_MARCA': int(datos_player['puntos_MARCA']),
                    'puntos_Goles': int(datos_player['puntos_Goles'])
                }, ignore_index=True)
    
    return df_resultado

def get_custom_precio():
    with open('./data/customPlayers.csv', newline='', encoding='utf-8') as csvfile:
        # Crea un lector CSV
        csv_reader = csv.reader(csvfile)

        # Lee la primera línea del archivo (encabezados)
        headers = next(csv_reader)

        # Encuentra el índice de la columna 'PlayerId'
        player_id_index = headers.index('PlayerId')

        # Crea un array para almacenar las IDs de los jugadores
        player_ids = []

        # Lee cada fila y extrae la ID del jugador
        for row in csv_reader:
            player_id = int(row[player_id_index])
            player_ids.append(player_id)
    df_resultado = pd.DataFrame()
    for player_id in player_ids:
        datos_player = get_datos_por_id_precios(player_id)
        df_resultado = df_resultado._append({'ID': player_id, 'Nombre': datos_player['Name'],'Price': datos_player['Price'], 'AveragePoints': datos_player['AveragePoints'], 
                   'Goals': datos_player['Goals'], 'Matches': datos_player['Matches'], 'AveragePtsLastThreeMatches': datos_player['AveragePtsLastThreeMatches'],
                   'AverageCardsLastThreeMatches': datos_player['AverageCardsLastThreeMatches']}, ignore_index=True)
    
    return df_resultado
