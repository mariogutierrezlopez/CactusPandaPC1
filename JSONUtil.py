import json

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

# Ejemplo de uso
guardarDatos("", "")