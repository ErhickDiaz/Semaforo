import requests
import csv
import os
from datetime import datetime

# === CONFIGURACIÓN ===
API_URL = "https://www.drivetech.pro/api/v1/get_vehicles_positions/"
TOKEN = "3942dc171775f7c00862ac8010e77c88198f3db6"
CLIENT_ID = "transportes_san_gabriel"
PLATES = []  # Si se deja vacío, se traen todos

# === CABECERAS ===
headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# === PAYLOAD DE CONSULTA ===
payload = {
    "client_id": CLIENT_ID,
    "plates": PLATES
}

# === RUTA DE SALIDA ===
os.makedirs("output_files", exist_ok=True)
output_file = os.path.join("output_files", "detalle_drivetech.csv")

# === LLAMADA A LA API ===
try:
    print("🔍 Consultando información detallada desde Drivetech...")
    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()

        if data.get("success"):
            posiciones = data.get("positions", [])

            if posiciones:
                # Detectar automáticamente las claves del primer registro
                columnas = list(posiciones[0].keys())

                with open(output_file, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=columnas)
                    writer.writeheader()
                    writer.writerows(posiciones)

                print(f"✅ Archivo generado correctamente: {output_file}")
            else:
                print("⚠️ La respuesta fue exitosa pero no contiene posiciones.")
        else:
            print("❌ Error en respuesta:", data.get("error"))
    else:
        print(f"❌ Error HTTP {response.status_code}: {response.text}")

except Exception as e:
    print(f"❌ Error al realizar la solicitud: {e}")
