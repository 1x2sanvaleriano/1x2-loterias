import json, os, requests
from datetime import datetime

RUTA_JSON = 'datos.json'
API_URL = "https://www.loteriasyapuestas.es/servicios/buscadorSorteos"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

if os.path.exists(RUTA_JSON):
    with open(RUTA_JSON, 'r', encoding='utf-8') as f:
        datos = json.load(f)
else:
    datos = {}

def fecha(fecha_iso):
    return datetime.strptime(fecha_iso, '%Y-%m-%d').strftime('%d/%m/%Y')

def get_ultimo(juego):
    try:
        r = requests.get(API_URL, params={'juego': juego, 'nSorteos': 1}, headers=HEADERS, timeout=20)
        r.raise_for_status()
        s = r.json()['sorteos'][0]
        c = s.get('combinacion', '').split(',')
        
        if juego in ['LA_PRIMITIVA', 'BONOLOTO']:
            return {'fecha': fecha(s['fechaSorteo']), 'numeros': " ".join(c[:6]), 'complementario': c[6], 'reintegro': s.get('reintegro', ''), 'bote': s.get('bote', '0€')}
        if juego == 'EUROMILLONES':
            return {'fecha': fecha(s['fechaSorteo']), 'numeros': " ".join(c[:5]), 'estrellas': " ".join(c[5:7]), 'bote': s.get('bote', '0€')}
        if juego == 'EUROJACKPOT':
            return {'fecha': fecha(s['fechaSorteo']), 'numeros': " ".join(c[:5]), 'clave': c[5], 'bote': s.get('bote', '0€')}
        if juego == 'EURODREAMS':
            return {'fecha': fecha(s['fechaSorteo']), 'numeros': " ".join(c[:6]), 'sueno': c[6], 'premio': s.get('premioEspecial', '0€')}
        if juego == 'LA_QUINIELA':
            return {'fecha': fecha(s['fechaSorteo']), 'resultado': s.get('combinacion', ''), 'bote': s.get('bote', '0€')}
        if juego == 'QUINIGOL':
            return {'fecha': fecha(s['fechaSorteo']), 'resultado': s.get('combinacion', ''), 'bote': s.get('bote', '0€')}
        if juego == 'LOTERIANACIONAL':
            return {'fecha': fecha(s['fechaSorteo']), 'primero': c[0], 'reintegros': " ".join(s.get('reintegros', []))}
    except Exception as e:
        print(f"Error {juego}: {e}")
    return None

mapa = {'primitiva':'LA_PRIMITIVA','bonoloto':'BONOLOTO','euromillones':'EUROMILLONES','gordo':'EUROJACKPOT','eurodreams':'EURODREAMS','quiniela':'LA_QUINIELA','quinigol':'QUINIGOL','jueves':'LOTERIANACIONAL','sabado':'LOTERIANACIONAL'}

for key, codigo in mapa.items():
    nuevo = get_ultimo(codigo)
    if nuevo:
        dia = datetime.strptime(nuevo['fecha'], '%d/%m/%Y').weekday()
        if key == 'jueves' and dia == 3: datos[key] = nuevo
        elif key == 'sabado' and dia == 5: datos[key] = nuevo
        elif key not in ['jueves','sabado']: datos[key] = nuevo
        print(f"{key} actualizado: {nuevo['fecha']}")
    else:
        print(f"{key} sin datos nuevos")

with open(RUTA_JSON, 'w', encoding='utf-8') as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

print("Proceso terminado. datos.json actualizado.")
