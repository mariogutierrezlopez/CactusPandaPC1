import csv
import os
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
    print(nombre_archivo)
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