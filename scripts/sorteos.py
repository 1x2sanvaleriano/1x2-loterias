import json
import os
from datetime import datetime

RUTA_JSON = 'datos.json' # Ruta donde tienes el json en tu repo

# 1. Cargar datos viejos si existen. Si no, empezar vacío
if os.path.exists(RUTA_JSON):
    with open(RUTA_JSON, 'r', encoding='utf-8') as f:
        try:
            datos = json.load(f)
        except json.JSONDecodeError:
            datos = {} # Si el json está corrupto, empezamos de 0
else:
    datos = {}

hoy = datetime.now().strftime("%d/%m")

# 2. Ejemplo: Actualizar solo Primitiva si ya ha salido
# Tu función de scraping te da estos valores
primitiva_nueva = scrape_primitiva() # Esta es tu función

if primitiva_nueva: # Solo actualiza si el scrape ha devuelto algo
    datos['primitiva'] = {
        'fecha': hoy,
        'numeros': primitiva_nueva['numeros'],
        'complementario': primitiva_nueva['complementario'],
        'reintegro': primitiva_nueva['reintegro'],
        'bote': primitiva_nueva['bote']
    }
# Si primitiva_nueva es None/vacío, no tocas datos['primitiva']. Se queda como estaba.

# 3. Repite lo mismo para Bonoloto, Euromillones, etc
bonoloto_nuevo = scrape_bonoloto()
if bonoloto_nuevo:
    datos['bonoloto'] = {
        'fecha': hoy,
        'numeros': bonoloto_nuevo['numeros'],
        'complementario': bonoloto_nuevo['complementario'],
        'reintegro': bonoloto_nuevo['reintegro'],
        'bote': bonoloto_nuevo['bote']
    }

# Para Nacional Jueves/Sábado igual
jueves_nuevo = scrape_jueves()
if jueves_nuevo:
    datos['jueves'] = {
        'fecha': '17/04', # o la que toque
        'primero': jueves_nuevo['primero'],
        'reintegros': jueves_nuevo['reintegros']
    }

# 4. Guardar el json completo, con lo viejo + lo nuevo
with open(RUTA_JSON, 'w', encoding='utf-8') as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)
