import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

API = Path(__file__).resolve().parents[1] / "api"
sys.path.insert(0, str(API))
from catalogo import leer_catalogo

class CatalogoTest(unittest.TestCase):
    def test_documento_finanzas(self):
        filas = leer_catalogo(API / "catalogo.json")
        self.assertEqual([d["id"] for d in filas if d["categoria"] == "Finanzas"], ["ADM-002"])
        self.assertEqual(len(filas), len({d["id"] for d in filas}))

    def test_catalogo_vacio(self):
        with TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "datos.json"
            ruta.write_text("[]", encoding="utf-8")
            self.assertEqual(leer_catalogo(ruta), [])

    def test_rechaza_documento_incompleto(self):
        with TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "datos.json"
            ruta.write_text('[{"id":"ADM-004"}]', encoding="utf-8")
            with self.assertRaises(ValueError):
                leer_catalogo(ruta)

    def test_archivo_ausente(self):
        with TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                leer_catalogo(Path(tmp) / "ausente.json")
