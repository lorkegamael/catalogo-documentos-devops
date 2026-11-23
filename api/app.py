from catalogo import leer_catalogo
import os
from pathlib import Path
from flask import Flask, jsonify

app = Flask(__name__)
CATALOGO = Path(os.getenv("CATALOGO_ARCHIVO", Path(__file__).with_name("catalogo.json")))

@app.get("/health")
def health():
    leer_catalogo(CATALOGO)
    return jsonify(estado="ok", servicio="api")

@app.get("/api/documentos")
def documentos():
    return jsonify(documentos=leer_catalogo(CATALOGO))

@app.errorhandler(OSError)
@app.errorhandler(ValueError)
def catalogo_inaccesible(error):
    app.logger.error("Catálogo no disponible: %s", type(error).__name__)
    return jsonify(estado="error", mensaje="Catálogo no disponible"), 503

