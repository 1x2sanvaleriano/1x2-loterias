import json, os, requests
from datetime import datetime

RUTA_JSON = 'datos.json'
API_URL = "https://www.loteriasyapuestas.es/servicios/buscadorSorteos"
HEADERS = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}

if os.path.exists(RUTA_JSON):
    with open(RUTA_JSON, 'r', encoding='utf-8') as f:
        datos = json.load(f)
else:
    datos = {}

def fecha(fecha_iso):
    return datetime.strptime(fecha_iso, '%Y-%m-%d').strftime('%d/%m/%Y')

def get_ultimo(juego):
    print(f"--- Probando {juego} ---")
    try:
        r = requests.get(API_URL, params={'juego': juego, 'nSorteos': 1}, headers=HEADERS, timeout=20)
        print(f"Status: {r.status_code}")
        res = r.json()
        print(f"JSON crudo: {res}") # Esto nos dirá todo
        if not res or 'sorteos' not in res or len(res['sorteos']) == 0:
            print("No hay sorteos en la respuesta")
            return None
        s = res['sorteos'][0]
        c = s.get('combinacion', '').split(',')
        print(f"Fecha API: {s['fechaSorteo']} | Combinacion: {c}")

        return {'fecha': fecha(s['fechaSorteo']), 'numeros': " ".join(c[:6]), 'complementario': c[6], 'reintegro': s.get('reintegro', ''), 'bote': s.get('bote', '0€')}
    except Exception as e:
        print(f"Error {juego}: {e}")
    return None

nuevo = get_ultimo('LA_PRIMITIVA')
if nuevo:
    datos['primitiva'] = nuevo
    print(f"primitiva actualizado: {nuevo['fecha']}")
else:
    print("primitiva sin datos nuevos")

with open(RUTA_JSON, 'w', encoding='utf-8') as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

print("Proceso terminado.")
