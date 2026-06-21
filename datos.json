import json
import os
import requests
from bs4 import BeautifulSoup

FILE = "datos.json"
URL = "https://loterianuevocentro.es/resultados"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

datos = {}
if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        datos = json.load(f)
print(f"Datos iniciales cargados. Primitiva: {datos.get('primitiva',{}).get('fecha','N/A')}")

r = requests.get(URL, headers=HEADERS, timeout=30)
print(f"Status: {r.status_code}")

soup = BeautifulSoup(r.text, 'lxml')

bloques = soup.select('.sorteo')
print(f"Bloques .sorteo encontrados: {len(bloques)}")

if len(bloques) == 0:
    print("ERROR: La web no tiene .sorteo. Guardando HTML para debug")
    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Revisa el artifact debug.html")
else:
    for bloque in bloques:
        juego_id = bloque.get('id', 'sin-id')
        print(f"Encontrado: id={juego_id}")
        fecha = bloque.select_one('.fecha-sorteo')
        if fecha:
            print(f"  -> Fecha: {fecha.text.strip()}")

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print("Proceso terminado. datos.json re-guardado.")
