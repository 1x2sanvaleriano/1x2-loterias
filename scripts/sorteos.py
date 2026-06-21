import json, os, requests
from datetime import datetime

RUTA_JSON = 'datos.json'
URL = "https://www.loteriasyapuestas.es/loterias/json/ultimos-resultados.json"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

if os.path.exists(RUTA_JSON):
    with open(RUTA_JSON, 'r', encoding='utf-8') as f:
        datos = json.load(f)
else:
    datos = {}

def fecha(fecha_iso):
    return datetime.strptime(fecha_iso, '%Y-%m-%d').strftime('%d/%m/%Y')

def actualizar():
    r = requests.get(URL, headers=HEADERS, timeout=20)
    r.raise_for_status()
    res = r.json()

    for juego in res:
        nombre = juego['nombre'].lower()
        fecha_juego = fecha(juego['fecha_sorteo'])
        numeros = juego.get('combinacion', [])
        bote = juego.get('bote', '0') + '€'

        if 'primitiva' in nombre and 'jueves' not in nombre and 'sabado' not in nombre:
            datos['primitiva'] = {
                'fecha': fecha_juego,
                'numeros': " ".join(numeros[:6]),
                'complementario': numeros[6],
                'reintegro': juego.get('reintegro', ''),
                'bote': bote
            }
            print(f"primitiva actualizado: {fecha_juego}")

        elif 'bonoloto' in nombre:
            datos['bonoloto'] = {
                'fecha': fecha_juego,
                'numeros': " ".join(numeros[:6]),
                'complementario': numeros[6],
                'reintegro': juego.get('reintegro', ''),
                'bote': bote
            }
            print(f"bonoloto actualizado: {fecha_juego}")

        elif 'euromillones' in nombre:
            datos['euromillones'] = {
                'fecha': fecha_juego,
                'numeros': " ".join(numeros[:5]),
                'estrellas': " ".join(numeros[5:7]),
                'bote': bote
            }
            print(f"euromillones actualizado: {fecha_juego}")

        elif 'eurojackpot' in nombre or 'el gordo' in nombre:
            datos['gordo'] = {
                'fecha': fecha_juego,
                'numeros': " ".join(numeros[:5]),
                'clave': numeros[5],
                'bote': bote
            }
            print(f"gordo actualizado: {fecha_juego}")

        elif 'eurodreams' in nombre:
            datos['eurodreams'] = {
                'fecha': fecha_juego,
                'numeros': " ".join(numeros[:6]),
                'sueno': numeros[6],
                'premio': juego.get('premio_especial', '0€')
            }
            print(f"eurodreams actualizado: {fecha_juego}")

        elif 'quiniela' in nombre and 'gol' not in nombre:
            datos['quiniela'] = {
                'fecha': fecha_juego,
                'resultado': juego.get('combinacion_str', ''),
                'bote': bote
            }
            print(f"quiniela actualizado: {fecha_juego}")

        elif 'quinigol' in nombre:
            datos['quinigol'] = {
                'fecha': fecha_juego,
                'resultado': juego.get('combinacion_str', ''),
                'bote': bote
            }
            print(f"quinigol actualizado: {fecha_juego}")

        elif 'loteria nacional' in nombre:
            dia = datetime.strptime(fecha_juego, '%d/%m/%Y').weekday()
            item = {'fecha': fecha_juego, 'primero': numeros[0], 'reintegros': " ".join(juego.get('reintegros', []))}
            if dia == 3:
                datos['jueves'] = item
                print(f"jueves actualizado: {fecha_juego}")
            elif dia == 5:
                datos['sabado'] = item
                print(f"sabado actualizado: {fecha_juego}")

    with open(RUTA_JSON, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

    print("Proceso terminado. datos.json actualizado.")

try:
    actualizar()
except Exception as e:
    print(f"Error general: {e}")
