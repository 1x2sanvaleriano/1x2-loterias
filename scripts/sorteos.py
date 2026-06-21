import json
import os
import requests
from bs4 import BeautifulSoup
import re

FILE = "datos.json"
URL = "https://loterianuevocentro.es/resultados"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

datos = {}
if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        datos = json.load(f)

def clean_num(s):
    return re.sub(r'\D', '', s)

def get_soup():
    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    print(f"Status: {r.status_code} OK")
    return BeautifulSoup(r.text, 'lxml')

soup = get_soup()

try:
    # La web tiene 1 bloque por sorteo: <div class="sorteo" id="la-primitiva"> etc
    for bloque in soup.select('.sorteo'):
        juego_id = bloque.get('id', '').lower()
        fecha = bloque.select_one('.fecha-sorteo').text.strip()
        bote = bloque.select_one('.bote').text.strip() if bloque.select_one('.bote') else "0€"

        bolas = [b.text.strip() for b in bloque.select('.bola')]

        if 'primitiva' in juego_id:
            datos['primitiva'] = {
                'fecha': fecha,
                'numeros': " ".join(bolas[:6]),
                'complementario': bolas[6] if len(bolas) > 6 else "",
                'reintegro': bloque.select_one('.reintegro').text.strip()[-1] if bloque.select_one('.reintegro') else "",
                'bote': bote
            }
            print(f"primitiva: {fecha}")

        elif 'bonoloto' in juego_id:
            datos['bonoloto'] = {
                'fecha': fecha,
                'numeros': " ".join(bolas[:6]),
                'complementario': bolas[6] if len(bolas) > 6 else "",
                'reintegro': bloque.select_one('.reintegro').text.strip()[-1] if bloque.select_one('.reintegro') else "",
                'bote': bote
            }
            print(f"bonoloto: {fecha}")

        elif 'euromillones' in juego_id:
            estrellas = [e.text.strip() for e in bloque.select('.estrella')]
            datos['euromillones'] = {
                'fecha': fecha,
                'numeros': " ".join(bolas[:5]),
                'estrellas': " ".join(estrellas),
                'bote': bote
            }
            print(f"euromillones: {fecha}")

        elif 'eurojackpot' in juego_id or 'el-gordo' in juego_id:
            claves = [e.text.strip() for e in bloque.select('.clave')]
            datos['gordo'] = {
                'fecha': fecha,
                'numeros': " ".join(bolas[:5]),
                'clave': claves[0] if claves else "",
                'bote': bote
            }
            print(f"gordo: {fecha}")

        elif 'eurodreams' in juego_id:
            sueno = bloque.select_one('.sueno').text.strip() if bloque.select_one('.sueno') else ""
            datos['eurodreams'] = {
                'fecha': fecha,
                'numeros': " ".join(bolas[:6]),
                'sueno': sueno,
                'premio': bote
            }
            print(f"eurodreams: {fecha}")

        elif 'loteria-nacional' in juego_id:
            tipo = 'jueves' if 'jueves' in bloque.text.lower() else 'sabado'
            datos[tipo] = {
                'fecha': fecha,
                'primero': bolas[0] if bolas else "",
                'reintegros': " ".join([r.text.strip() for r in bloque.select('.reintegro')])
            }
            print(f"{tipo}: {fecha}")

        elif 'quiniela' in juego_id and 'gol' not in juego_id:
            res = bloque.select_one('.resultado').text.strip()
            datos['quiniela'] = {
                'fecha': fecha,
                'resultado': res,
                'bote': bote
            }
            print(f"quiniela: {fecha}")

        elif 'quinigol' in juego_id:
            res = bloque.select_one('.resultado').text.strip()
            datos['quinigol'] = {
                'fecha': fecha,
                'resultado': res,
                'bote': bote
            }
            print(f"quinigol: {fecha}")

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print("Proceso terminado. datos.json actualizado.")

except Exception as e:
    print(f"Error parseando: {e}")
