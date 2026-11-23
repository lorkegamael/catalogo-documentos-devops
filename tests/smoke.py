"""Prueba el recorrido completo a través del frontend publicado."""
import json
import sys
from urllib.request import urlopen

def comprobar(base):
    def leer(ruta):
        with urlopen(base + ruta, timeout=5) as respuesta:
            assert respuesta.status == 200
            return respuesta.read()
    assert "Catálogo documental" in leer("/").decode("utf-8")
    print("OK interfaz HTML")
    assert json.loads(leer("/health")) == {"estado": "ok", "servicio": "api"}
    print("OK /health")
    filas = json.loads(leer("/api/documentos"))["documentos"]
    assert filas and len({d["id"] for d in filas}) == len(filas)
    assert all(all(d[k].strip() for k in ("id","titulo","categoria","version")) for d in filas)
    assert any(d["id"] == "ADM-002" and d["categoria"] == "Finanzas" for d in filas)
    print(f"OK /api/documentos: {len(filas)} documentos; ADM-002 en Finanzas")

if __name__ == "__main__":
    comprobar(sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080")
