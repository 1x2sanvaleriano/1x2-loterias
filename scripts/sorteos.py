import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

RUTA_JSON = 'datos.json'
BASE_URL = "https://www.loteriasyapuestas.es/es"
HEADERS = {'User-Agent': 'Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36'}

# 1. Cargar datos viejos si existen
if os.path.exists(RUTA_JSON):
    with open(RUTA_JSON, 'r', encoding='utf-8') as f:
        try:
            datos = json.load(f)
        except json.JSONDecodeError:
            datos = {}
else:
    datos = {}

def get_soup(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        return BeautifulSoup(r.text, 'lxml')
    except Exception as e:
        print(f"Error al cargar {url}: {e}")
        return None

def limpiar_bote(texto):
    return texto.replace('Bote', '').replace('Millones', 'M€').replace('Miles', 'K€').strip()

# 2. Funciones de scrape para cada juego
def scrape_primitiva():
    soup = get_soup(f"{BASE_URL}/la-primitiva")
    if not soup: return None
    try:
        fecha = soup.select_one('.last-draw-date').get_text(strip=True).split(' ')[-1]
        bolas = soup.select('.ball.drawn-ball')
        numeros = " ".join([b.get_text(strip=True) for b in bolas[:6]])
        complementario = soup.select_one('.ball.complementary').get_text(strip=True)
        reintegro = soup.select_one('.ball.reintegro').get_text(strip=True)
        bote = limpiar_bote(soup.select_one('.jackpot-amount').get_text(strip=True))
        return {'fecha': fecha, 'numeros': numeros, 'complementario': complementario, 'reintegro': reintegro, 'bote': bote}
    except Exception as e:
        print(f"Error Primitiva: {e}")
        return None

def scrape_bonoloto():
    soup = get_soup(f"{BASE_URL}/bonoloto")
    if not soup: return None
    try:
        fecha = soup.select_one('.last-draw-date').get_text(strip=True).split(' ')[-1]
        bolas = soup.select('.ball.drawn-ball')
        numeros = " ".join([b.get_text(strip=True) for b in bolas[:6]])
        complementario = soup.select_one('.ball.complementary').get_text(strip=True)
        reintegro = soup.select_one('.ball.reintegro').get_text(strip=True)
        bote = limpiar_bote(soup.select_one('.jackpot-amount').get_text(strip=True))
        return {'fecha': fecha, 'numeros': numeros, 'complementario': complementario, 'reintegro': reintegro, 'bote': bote}
    except Exception as e:
        print(f"Error Bonoloto: {e}")
        return None

def scrape_euromillones():
    soup = get_soup(f"{BASE_URL}/euromillones")
    if not soup: return None
    try:
        fecha = soup.select_one('.last-draw-date').get_text(strip=True).split(' ')[-1]
        bolas = soup.select('.ball.drawn-ball')
        numeros = " ".join([b.get_text(strip=True) for b in bolas[:5]])
        estrellas = " ".join([b.get_text(strip=True) for b in bolas[5:7]])
        bote = limpiar_bote(soup.select_one('.jackpot-amount').get_text(strip=True))
        return {'fecha': fecha, 'numeros': numeros, 'estrellas': estrellas, 'bote': bote}
    except Exception as e:
        print(f"Error Euromillones: {e}")
        return None

def scrape_gordo():
    soup = get_soup(f"{BASE_URL}/eurojackpot")
    if not soup: return None
    try:
        fecha = soup.select_one('.last-draw-date').get_text(strip=True).split(' ')[-1]
        bolas = soup.select('.ball.drawn-ball')
        numeros = " ".join([b.get_text(strip=True) for b in bolas[:5]])
        clave = " ".join([b.get_text(strip=True) for b in bolas[5:7]])
        bote = limpiar_bote(soup.select_one('.jackpot-amount').get_text(strip=True))
        return {'fecha': fecha, 'numeros': numeros, 'clave': clave, 'bote': bote}
    except Exception as e:
        print(f"Error Eurojackpot: {e}")
        return None

def scrape_eurodreams():
    soup = get_soup(f"{BASE_URL}/eurodreams")
    if not soup: return None
    try:
        fecha = soup.select_one('.last-draw-date').get_text(strip=True).split(' ')[-1]
        bolas = soup.select('.ball.drawn-ball')
        numeros = " ".join([b.get_text(strip=True) for b in bolas[:6]])
        sueno = soup.select_one('.ball.dream-number').get_text(strip=True)
        premio = soup.select_one('.jackpot-amount').get_text(strip=True)
        return {'fecha': fecha, 'numeros': numeros, 'sueno': sueno, 'premio': premio}
    except Exception as e:
        print(f"Error Eurodreams: {e}")
        return None

def scrape_quiniela():
    soup = get_soup(f"{BASE_URL}/quiniela")
    if not soup: return None
    try:
        fecha = soup.select_one('.last-draw-date').get_text(strip=True).split(' ')[-1]
        resultados = " ".join([r.get_text(strip=True) for r in soup.select('.quiniela-result span')[:15]])
        pleno = soup.select_one('.pleno-15').get_text(strip=True)
        bote = limpiar_bote(soup.select_one('.jackpot-amount').get_text(strip=True))
        return {'fecha': fecha, 'resultado': f"{resultados} {pleno}", 'bote': bote}
    except Exception as e:
        print(f"Error Quiniela: {e}")
        return None

def scrape_quinigol():
    soup = get_soup(f"{BASE_URL}/quinigol")
    if not soup: return None
    try:
        fecha = soup.select_one('.last-draw-date').get_text(strip=True).split(' ')[-1]
        resultados = " ".join([r.get_text(strip=True) for r in soup.select('.quinigol-result span')[:6]])
        bote = limpiar_bote(soup.select_one('.jackpot-amount').get_text(strip=True))
        return {'fecha': fecha, 'resultado': resultados, 'bote': bote}
    except Exception as e:
        print(f"Error Quinigol: {e}")
        return None

def scrape_nacional(dia):
    soup = get_soup(f"{BASE_URL}/loteria-nacional")
    if not soup: return None
    try:
        # Loteria Nacional tiene jueves y sabado en la misma pagina
        seccion = soup.select_one(f'.draw-{dia}')
        fecha = seccion.select_one('.draw-date').get_text(strip=True).split(' ')[-1]
        primero = seccion.select_one('.first-prize.number').get_text(strip=True)
        reintegros = " ".join([r.get_text(strip=True) for r in seccion.select('.reintegro.number')])
        return {'fecha': fecha, 'primero': primero, 'reintegros': reintegros}
    except Exception as e:
        print(f"Error Loteria Nacional {dia}: {e}")
        return None

# 3. Ejecutar scrapes y actualizar solo si hay datos nuevos
scrapers = {
    'primitiva': scrape_primitiva,
    'bonoloto': scrape_bonoloto,
    'euromillones': scrape_euromillones,
    'gordo': scrape_gordo,
    'eurodreams': scrape_eurodreams,
    'quiniela': scrape_quiniela,
    'quinigol': scrape_quinigol,
    'jueves': lambda: scrape_nacional('thursday'),
    'sabado': lambda: scrape_nacional('saturday'),
}

for key, funcion in scrapers.items():
    nuevo = funcion()
    if nuevo:
        datos[key] = nuevo
        print(f"{key} actualizado: {nuevo['fecha']}")
    else:
        print(f"{key} sin cambios, se mantiene el anterior.")

# 4. Guardar el json completo
with open(RUTA_JSON, 'w', encoding='utf-8') as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

print("Proceso terminado. datos.json actualizado.")
