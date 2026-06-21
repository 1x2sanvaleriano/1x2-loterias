import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

RUTA_JSON = 'datos.json'

# Cargar datos viejos
if os.path.exists(RUTA_JSON):
    with open(RUTA_JSON, 'r', encoding='utf-8') as f:
        try:
            datos = json.load(f)
        except json.JSONDecodeError:
            datos = {}
else:
    datos = {}

hoy = datetime.now().strftime("%d/%m/%Y") # FIX: Año completo

def scrape_primitiva():
    try:
        url = "https://www.loteriasyapuestas.es/es/la-primitiva"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'lxml')

        # Selectores de loteriasyapuestas.es a 20/04/2026. Si cambian la web, hay que tocar esto
        fecha = soup.select_one('.last-draw-date').text.strip().split(' ')[-1] # "Sorteo del 20/04/2026" -> "20/04/2026"
        numeros = " ".join([b.text.strip() for b in soup.select('.ball.drawn-ball')[:6]])
        complementario = soup.select_one('.ball.complementary').text.strip()
        reintegro = soup.select_one('.ball.reintegro').text.strip()
        bote = soup.select_one('.jackpot-amount').text.strip().replace('Bote', '').strip()

        return {
            'fecha': fecha,
            'numeros': numeros,
            'complementario': complementario,
            'reintegro': reintegro,
            'bote': bote
        }
    except Exception as e:
        print(f"Error Primitiva: {e}")
        return None # Si falla, no actualiza y se queda el dato viejo

# Tus otras funciones. Copia la estructura de arriba
def scrape_bonoloto(): return None
def scrape_euromillones(): return None
def scrape_gordo(): return None
def scrape_eurodreams(): return None
def scrape_quiniela(): return None
def scrape_quinigol(): return None
def scrape_jueves(): return None
def scrape_sabado(): return None

# 2. Actualizar solo si el scrape ha devuelto algo
primitiva_nueva = scrape_primitiva()
if primitiva_nueva:
    datos['primitiva'] = primitiva_nueva

bonoloto_nuevo = scrape_bonoloto()
if bonoloto_nuevo:
    datos['bonoloto'] = bonoloto_nuevo

# Repite para todos...
# euromillones_nuevo = scrape_euromillones()
# if euromillones_nuevo: datos['euromillones'] = euromillones_nuevo

# 4. Guardar
with open(RUTA_JSON, 'w', encoding='utf-8') as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

print("Datos actualizados:", hoy)
