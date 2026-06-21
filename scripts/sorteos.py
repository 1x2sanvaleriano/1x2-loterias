import json
import os
import requests
from datetime import datetime

URL = "https://loterias-api.vercel.app/api/ultimosResultados"
FILE = "datos.json"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Cargar datos actuales
datos = {}
if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        datos = json.load(f)

def actualizar():
    r = requests.get(URL, headers=HEADERS, timeout=25)
    r.raise_for_status()
    api = r.json() # Dict: {"LA_PRIMITIVA": {...}, "EUROMILLONES": {...}, ...}
    print(f"Status: {r.status_code} OK")

    # LA_PRIMITIVA
    p = api.get("LA_PRIMITIVA")
    if p:
        datos["primitiva"] = {
            "fecha": p["fecha"],
            "numeros": " ".join(p["numeros"]),
            "complementario": p["complementario"],
            "reintegro": p["reintegro"],
            "bote": p["bote"]
        }
        print(f"primitiva actualizado: {p['fecha']}")

    # BONOLOTO
    b = api.get("BONOLOTO")
    if b:
        datos["bonoloto"] = {
            "fecha": b["fecha"],
            "numeros": " ".join(b["numeros"]),
            "complementario": b["complementario"],
            "reintegro": b["reintegro"],
            "bote": b["bote"]
        }
        print(f"bonoloto actualizado: {b['fecha']}")

    # EUROMILLONES
    em = api.get("EUROMILLONES")
    if em:
        datos["euromillones"] = {
            "fecha": em["fecha"],
            "numeros": " ".join(em["numeros"]),
            "estrellas": " ".join(em["estrellas"]),
            "bote": em["bote"]
        }
        print(f"euromillones actualizado: {em['fecha']}")

    # EUROJACKPOT = El Gordo
    ej = api.get("EUROJACKPOT")
    if ej:
        datos["gordo"] = {
            "fecha": ej["fecha"],
            "numeros": " ".join(ej["numeros"]),
            "clave": ej["clave"],
            "bote": ej["bote"]
        }
        print(f"gordo actualizado: {ej['fecha']}")

    # EURODREAMS
    ed = api.get("EURODREAMS")
    if ed:
        datos["eurodreams"] = {
            "fecha": ed["fecha"],
            "numeros": " ".join(ed["numeros"]),
            "sueno": ed["sueno"],
            "premio": ed["premio"]
        }
        print(f"eurodreams actualizado: {ed['fecha']}")

    # LOTERIA NACIONAL JUEVES
    lnj = api.get("LOTERIA_NACIONAL_JUEVES")
    if lnj:
        datos["jueves"] = {
            "fecha": lnj["fecha"],
            "primero": lnj["primero"],
            "reintegros": " ".join(lnj["reintegros"])
        }
        print(f"jueves actualizado: {lnj['fecha']}")

    # LOTERIA NACIONAL SABADO
    lns = api.get("LOTERIA_NACIONAL_SABADO")
    if lns:
        datos["sabado"] = {
            "fecha": lns["fecha"],
            "primero": lns["primero"],
            "reintegros": " ".join(lns["reintegros"])
        }
        print(f"sabado actualizado: {lns['fecha']}")

    # QUINIELA
    q = api.get("QUINIELA")
    if q:
        datos["quiniela"] = {
            "fecha": q["fecha"],
            "resultado": q["resultado"],
            "bote": q["bote"]
        }
        print(f"quiniela actualizado: {q['fecha']}")

    # QUINIGOL
    qg = api.get("QUINIGOL")
    if qg:
        datos["quinigol"] = {
            "fecha": qg["fecha"],
            "resultado": qg["resultado"],
            "bote": qg["bote"]
        }
        print(f"quinigol actualizado: {qg['fecha']}")

    # Guardar
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print("Proceso terminado. datos.json actualizado.")

try:
    actualizar()
except Exception as e:
    print(f"Error general: {e}")
