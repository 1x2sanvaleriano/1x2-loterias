import requests
import json
from datetime import datetime, date
from pathlib import Path

BASE_URL = "https://www.loteriasyapuestas.es/es/api/resultados"
DATA_FILE = Path("datos/sorteos.json")

JUEGOS = {
    "primitiva": {"nombre": "La Primitiva", "dias": [3, 5]},
    "bonoloto": {"nombre": "Bonoloto", "dias": [0,1,2,3,4,5,6]},
    "euromillones": {"nombre": "Euromillones", "dias": [1, 4]},
    "gordo": {"nombre": "El Gordo de la Primitiva", "dias": [6]},
    "eurodreams": {"nombre": "EuroDreams", "dias": [0, 3]},
    "loteria-nacional": {"nombre": "Lotería Nacional", "dias": [3, 5]},
    "quiniela": {"nombre": "La Quiniela", "dias": [6, 0]},
    "quinigol": {"nombre": "Quinigol", "dias": [6, 0]}
}

def obtener_resultado(juego_id):
    try:
        url = f"{BASE_URL}/{juego_id}"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()

        if not data or "resultado" not in data[0]:
            return None

        ultimo = data[0]
        fecha_sorteo = datetime.strptime(ultimo["fechaSorteo"], "%Y-%m-%d").date()

        if fecha_sorteo!= date.today():
            return None

        return {
            "fecha": ultimo["fechaSorteo"],
            "combinacion": ultimo["combinacion"],
            "reintegro": ultimo.get("reintegro", ""),
            "complementario": ultimo.get("complementario", ""),
            "estrellas": ultimo.get("estrellas", "")
        }
    except Exception as e:
        print(f"Error en {juego_id}: {e}")
        return None

def main():
    hoy = date.today()
    dia_semana = hoy.weekday()

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            historico = json.load(f)
    else:
        historico = {}

    nuevos = {}
    for juego_id, info in JUEGOS.items():
        if dia_semana in info["dias"]:
            print(f"Consultando {info['nombre']}...")
            resultado = obtener_resultado(juego_id)
            if resultado:
                nuevos[juego_id] = resultado
                print(f" -> OK: {resultado['fecha']}")
            else:
                print(f" -> Sin datos aún para hoy")

    if nuevos:
        historico[hoy.isoformat()] = nuevos
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
        print(f"Guardado: {DATA_FILE}")
    else:
        print("Sin resultados nuevos que guardar.")

if __name__ == "__main__":
    main()
