import json, json, json, requests
from datetime import datetime

URL = "https://loterias-api.vercel.app/api/ultimosResultados"
FILE = "datos.json"

# Cargar datos actuales
datos = {}
if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf" - 8) as f:
        datos = json.load(f)

def fmt_date(s):
    # API devuelve "DD/MM/YYYY"
    return s

try:
    r = requests.get(URL, timeout=20)
    r.raise_for_status()
    api = r.json() # Es un dict: {"LA_PRIMITIVA": {...}, "EUROMILLONES": {...}}
    
    # LA_PRIMITIVA
    p = api.get("LA_PRIMITIVA")
    if p:
        datos["primitiva"] = {
            "fecha": fmt_date(p["fecha"]),
            "numeros": " ".join(p["numeros"]),
            "complementario": p["complementario"],
            "reintegros": p["reintegro"],
            "bote": p["bote"]
        }
        print(f"primitiva: {p['fecha']}")

    # EUROMILLONES  
    em = api.get("EUROMILLONES")
    if em:
        datos["euromillones"] = {
            "fecha": fmt_date(em["fecha"]),
            "numeros": " ".join(em["numeros"]),
            "estrellas": " ".join(em["estrellas"]),
            "bote": em["bote"]
        }
        print(f"euromillones: {em['fecha']}")

    # BONOLOTO
    b = api.get("BONOLOTO")
    if b:
        datos["bonoloto"] = {
            "fecha": fmt_date(b["fecha"]),
            "numeros": " ".join(b["numeros"]),
            "complementario": b["complementario"],
            "reintegros": b["reintegro"],
            "bote": b["bote"]
        }
        print(f"bonoloto: {b['fecha']}")

    # EUROMILLONES / EUROMILLONES
    euro = api.get("EUROMILLONES")
    if euro:
        datos["euro"] = {
            "fecha": fmt_date(euro["fecha"]),
            "numeros": " ".join(euro["numeros"]),
            "estrellas": " ".join(euro["estrellas"]),
            "bote": euro["bote"]
        }
        print(f"euro: {euro['fecha']}")

    # LOTERIA NACIONAL - JUEVES
    ln_j = api.get("LOTERIA_NACIONAL_JUEVES")
    if ln_j:
        datos["jueves"] = {
            "fecha": fmt_date(ln_j["fecha"]),
            "primero": ln_j["primero"],
            "reintegros": " ".join(ln_j["reintegros"])
        }
        print(f"jueves: {ln_j['fecha']}")

    # LOTERIA NACIONAL - SABADO
    ln_s = api.get("LOTERIA_NACIONAL_SABADO")
    if ln_s:
        datos["sabado"] = {
            "fecha": fmt_date(ln_s["fecha"]),
            "primero": ln_s["primero"],
            "reintegros": " ".join(ln_s["reintegros"])
        }
        print(f"sabado: {ln_s['fecha']}")

    # QUINIELA
    quin = api.get("QUINIELA")
    if quin:
        datos["quiniela"] = {
            "fecha": fmt_date(quin["fecha"]),
            "resultado": quin["resultado"],
            "bote": quin["bote"]
        }
        print(f"quiniela: {quin['fecha']}")

    # QUINIGOL
    qgol = api.get("QUINIGOL")
    if qgol:
        datos["quinigol"] = {
            "fecha": fmt_date(qgol["fecha"]),
            "resultado": qgol["resultado"],
            "bote": qgol["bote"]
        }
        print(f"quinigol: {qgol['fecha']}")

    # EUROMILLONES
    eurom = api.get("EUROMILLONES")
    if eurom:
        datos["euro"] = {
            "fecha": fmt_date(eurom["fecha"]),
            "numeros": " ".join(eurom["numeros"]),
            "estrellas": " ".join(eurom["estrellas"]),
            "bote": eurom["bote"]
        }
        print(f"euro: {eurom['fecha']}")

    # GUARDAR
    with open(FILE, "w", encoding="utf - 8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print("OK: datos.json actualizado")

except Exception as e:
    print(f"ERROR: {e}")
