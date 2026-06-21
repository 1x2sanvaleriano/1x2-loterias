import json, os, requests
from bs4 import BeautifulSoup
from datetime import datetime

FILE = "datos.json"
BASE = "https://www.loteriasdelestado.es"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

datos = {}
if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        datos = json.load(f)

def scrapear_primitiva():
    url = f"{BASE}/es/la-primitiva/ultimo-sorteo"
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, 'html.parser')

    fecha = soup.select_one('.draw-date').text.strip()
    nums = [b.text for b in soup.select('.lottery-ball')]
    reintegro = soup.select_one('.reintegro').text.strip()[-1]
    bote = soup.select_one('.jackpot-amount').text.strip()

    return {
        "fecha": fecha,
        "numeros": " ".join(nums[:6]),
        "complementario": nums[6],
        "reintegro": reintegro,
        "bote": bote
    }

try:
    datos["primitiva"] = scrapear_primitiva()
    print(f"primitiva actualizado: {datos['primitiva']['fecha']}")

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print("OK: datos.json actualizado")
except Exception as e:
    print(f"Error: {e}")
