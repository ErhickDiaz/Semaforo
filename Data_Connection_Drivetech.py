import requests
import pandas as pd
import schedule
import time
from datetime import datetime

# Configuración de la API de Drivetech
API_URL = "https://www.drivetech.pro/api/v1/get_vehicles_positions/"  # Reemplaza con el endpoint real
API_KEY = "3942dc171775f7c00862ac8010e77c88198f3db6"  # Reemplaza con tu API Key

# Función para obtener los datos de la API
def obtener_datos():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        datos = response.json()
        return datos
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API: {e}")
        return []

# Función para procesar los datos y generar el archivo CSV
def generar_csv():
    datos = obtener_datos()
    if not datos:
        print("No se obtuvieron datos de la API.")
        return

    registros = []
    for vehiculo in datos:
        transporte = vehiculo.get("vehicle_id", "N/A")
        origen = vehiculo.get("origin", "N/A")
        destino = vehiculo.get("destination", "N/A")
        ruta = f"{origen} – {destino}"
        hora_salida = vehiculo.get("planned_departure", "N/A")
        eta = vehiculo.get("estimated_arrival", "N/A")
        estado = vehiculo.get("status", "N/A")
        ultima_actualizacion = vehiculo.get("last_gps_update", "N/A")

        registros.append({
            "transporte": transporte,
            "ruta": ruta,
            "hora_salida": hora_salida,
            "eta": eta,
            "estado": estado,
            "ultima_actualizacion": ultima_actualizacion
        })

    df = pd.DataFrame(registros)
    df.to_csv("viajes.csv", index=False)
    print(f"{datetime.now()}: Archivo 'viajes.csv' actualizado correctamente.")

# Programar la ejecución cada 10 minutos
schedule.every(10).minutes.do(generar_csv)

print("Iniciando la actualización automática de 'viajes.csv' cada 10 minutos.")
generar_csv()  # Ejecutar inmediatamente al iniciar

while True:
    schedule.run_pending()
    time.sleep(1)
