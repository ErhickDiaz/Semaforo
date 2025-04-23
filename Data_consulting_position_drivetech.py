import requests
import csv
from datetime import datetime

# === CONFIGURACIÓN ===
API_URL = "https://www.drivetech.pro/api/v1/get_vehicles_positions/"
TOKEN = "3942dc171775f7c00862ac8010e77c88198f3db6"
CLIENT_ID = "transportes_san_gabriel"
PLATES = []

# === SOLICITUD A LA API ===
headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "client_id": CLIENT_ID,
    "plates": PLATES
}

response = requests.post(API_URL, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    if data.get("success"):
        posiciones = data["positions"]

        with open("viajes.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Transporte", "Ruta", "Hora Salida", "ETA",
                "Semáforo", "Última Actualización"
            ])

            for pos in posiciones:
                plate = pos.get("plate", "")
                geofences = pos.get("geofences", [])
                ruta = ", ".join(g.get("name", "") for g in geofences) if geofences else "Fuera de zona"
                ultima_actualizacion = pos.get("datetime", "")

                # Estado semáforo simplificado
                if geofences:
                    estado = "A tiempo"
                else:
                    estado = "Retrasado"

                writer.writerow([
                    plate,
                    ruta,
                    "",         # Hora Salida (opcional)
                    "",         # ETA (opcional)
                    estado,
                    ultima_actualizacion
                ])

        print("✅ Archivo viajes.csv generado para el semáforo.")
    else:
        print("❌ Error en respuesta:", data.get("error"))
else:
    print(f"❌ Error HTTP {response.status_code}: {response.text}")
