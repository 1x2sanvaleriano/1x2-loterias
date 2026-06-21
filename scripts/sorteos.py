import json, os, requests
from datetime import datetime

RUTA_JSON = 'datos.json'
BASE_URL = "https://resultados-loterias.com/api/ultimos"

if os.path.exists(RUTA_JSON):
    with open(RUTA_JSON, 'r', encoding='utf-8') as f:
        datos = json.load(f)
else:
    datos = {}

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fecha_ddmmyyyy(fecha_str):
    # La API devuelve YYYY-MM-DD
    return datetime.strptime(fecha_str, '%Y-%m-%d').strftime('%d/%m/%Y')

def get_datos():
    try:
        r = requests.get(BASE_URL, headers=HEADERS, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error API externa: {e}")
        return None

api_data = get_datos()
if not api_data:
    print("No se pudieron obtener datos")
    exit(0)

# Mapeo de la API externa a tu estructura
mapa = {
    'primitiva': 'la-primitiva',
    'bonoloto': 'bonoloto',
    'euromillones': 'euromillones',
    'gordo': 'euromillones-superenalotto', # Eurojackpot
    'eurodreams': 'eurodreams',
    'quiniela': 'la-quiniela',
    'quinigol': 'quinigol',
    'jueves': 'loteria-nacional-jueves',
    'sabado': 'loteria-nacional-sabado'
}

for key, slug in mapa.items():
    if slug not in api_data:
        print(f"{key} sin datos en API")
        continue

    s = api_data[slug]
    try:
        if key in ['primitiva', 'bonoloto']:
            datos[key] = {
                'fecha': fecha_ddmmyyyy(s['date']),
                'numeros': " ".join(map(str, s['numbers'][:6])),
                'complementario': str(s['numbers'][6]),
                'reintegro': str(s.get('reintegro', '')),
                'bote': s.get('jackpot', '0€')
            }
        elif key == 'euromillones':
            datos[key] = {
                'fecha': fecha_ddmmyyyy(s['date']),
                'numeros': " ".join(map(str, s['numbers'][:5])),
                'estrellas': " ".join(map(str, s['stars'])),
                'bote': s.get('jackpot', '0€')
            }
        elif key == 'gordo': # Eurojackpot
            datos[key] = {
                'fecha': fecha_ddmmyyyy(s['date']),
                'numeros': " ".join(map(str, s['numbers'][:5])),
                'clave': str(s['stars'][0]),
                'bote': s.get('jackpot', '0€')
            }
        elif key == 'eurodreams':
            datos[key] = {
                'fecha': fecha_ddmmyyyy(s['date']),
                'numeros': " ".join(map(str, s['numbers'][:6])),
                'sueno': str(s['stars'][0]),
                'premio': s.get('jackpot', '0€')
            }
        elif key in ['quiniela', 'quinigol']:
            datos[key] = {
                'fecha': fecha_ddmmyyyy(s['date']),
                'resultado': s['result'],
                'bote': s.get('jackpot', '0€')
            }
        elif key in ['jueves', 'sabado']: # Loteria Nacional
            datos[key] = {
                'fecha': fecha_ddmmyyyy(s['date']),
                'primero': str(s['first']),
                'reintegros': " ".join(map(str, s.get('reintegros', [])))
            }
        print(f"{key} actualizado: {datos[key]['fecha']}")
    except Exception as e:
        print(f"Error parseando {key}: {e}")

with open(RUTA_JSON, 'w', encoding='utf-8') as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

print("Proceso terminado. datos.json actualizado.")
