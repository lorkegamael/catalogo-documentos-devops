import json
from pathlib import Path

def leer_catalogo(ruta: Path):
    with ruta.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)
    if not isinstance(datos, list) or not all(
        isinstance(fila, dict) and all(isinstance(fila.get(k), str) and fila[k].strip()
        for k in ("id", "titulo", "categoria", "version")) for fila in datos
    ):
        raise ValueError("Estructura de catálogo inválida")
    return datos


