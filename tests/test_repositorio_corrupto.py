"""Pruebas de TASK-004: el repositorio rechaza archivos de datos dañados sin modificarlos."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from biblioteca.errores import DatosCorruptos
from biblioteca.repositorio import RepositorioJSON

# Contenido válido equivalente a D1 (plan de pruebas §2); cada prueba lo daña de una forma.
CONTENIDO_D1 = {
    "version": 1,
    "ejemplares": [
        {"identificador": "E-01", "titulo": "Cálculo I", "autor": "Stewart"},
        {"identificador": "E-02", "titulo": "Cálculo I", "autor": "Stewart"},
        {"identificador": "E-03", "titulo": "Física", "autor": "Serway"},
    ],
    "prestamos": [
        {"identificador_ejemplar": "E-02", "codigo_estudiante": "2024001",
         "nombre_estudiante": "Ana Pérez", "fecha_prestamo": "2026-11-20",
         "fecha_prevista": "2026-11-30", "fecha_devolucion": None},
    ],
}


class TestRepositorioCorrupto(unittest.TestCase):

    def setUp(self):
        self._carpeta = tempfile.TemporaryDirectory()
        self.ruta = Path(self._carpeta.name) / "biblioteca.json"

    def tearDown(self):
        self._carpeta.cleanup()

    def contenido_valido(self):
        return copy.deepcopy(CONTENIDO_D1)

    def assert_rechazado_sin_modificar(self, texto):
        """Común a TEST-010…016: DatosCorruptos con detalle y archivo idéntico byte a byte."""
        self.assert_bytes_rechazados(texto.encode("utf-8"))

    def assert_bytes_rechazados(self, contenido):
        self.ruta.write_bytes(contenido)
        antes = self.ruta.read_bytes()

        with self.assertRaises(DatosCorruptos) as contexto:
            RepositorioJSON(self.ruta).cargar()

        self.assertTrue(contexto.exception.detalle)
        self.assertEqual(self.ruta.read_bytes(), antes)

    def assert_contenido_rechazado(self, contenido):
        self.assert_rechazado_sin_modificar(json.dumps(contenido, ensure_ascii=False))

    def test_TEST_010_json_invalido(self):
        """TEST-010 (QP1): contenido base válido (control); texto que no es JSON; archivo que no es UTF-8."""
        with self.subTest(caso="control: contenido base válido"):
            # Asegura que en TEST-010…016 cada rechazo se debe al daño introducido.
            self.ruta.write_text(json.dumps(CONTENIDO_D1, ensure_ascii=False), encoding="utf-8")
            ejemplares, prestamos = RepositorioJSON(self.ruta).cargar()
            self.assertEqual((len(ejemplares), len(prestamos)), (3, 1))

        with self.subTest(caso="texto que no es JSON"):
            self.assert_rechazado_sin_modificar("{ejemplares: [")

        with self.subTest(caso="archivo que no es UTF-8"):
            contenido_latin1 = json.dumps(CONTENIDO_D1, ensure_ascii=False).encode("latin-1")
            self.assert_bytes_rechazados(contenido_latin1)

    def test_TEST_011_version_distinta(self):
        """TEST-011 (QP1): versión de formato distinta de 1."""
        contenido = self.contenido_valido()
        contenido["version"] = 2
        self.assert_contenido_rechazado(contenido)

    def test_TEST_012_campo_faltante_o_de_tipo_incorrecto(self):
        """TEST-012 (QP1): ejemplar sin autor; ejemplar con título numérico."""
        sin_autor = self.contenido_valido()
        del sin_autor["ejemplares"][0]["autor"]

        titulo_numerico = self.contenido_valido()
        titulo_numerico["ejemplares"][0]["titulo"] = 123

        for caso, contenido in (("sin autor", sin_autor), ("título numérico", titulo_numerico)):
            with self.subTest(caso=caso):
                self.assert_contenido_rechazado(contenido)

    def test_TEST_013_fecha_no_iso(self):
        """TEST-013 (QP1, DEC-007): fecha prevista en formato DD/MM/AAAA."""
        contenido = self.contenido_valido()
        contenido["prestamos"][0]["fecha_prevista"] = "24/11/2026"
        self.assert_contenido_rechazado(contenido)

    def test_TEST_014_identificador_duplicado(self):
        """TEST-014 (QP1, RN-001): dos ejemplares con identificador E-01."""
        contenido = self.contenido_valido()
        contenido["ejemplares"][1]["identificador"] = "E-01"
        contenido["prestamos"] = []
        self.assert_contenido_rechazado(contenido)

    def test_TEST_015_prestamo_de_ejemplar_inexistente(self):
        """TEST-015 (QP1): préstamo de E-99, que no está en el catálogo."""
        contenido = self.contenido_valido()
        contenido["prestamos"][0]["identificador_ejemplar"] = "E-99"
        self.assert_contenido_rechazado(contenido)

    def test_TEST_016_dos_prestamos_activos_del_mismo_ejemplar(self):
        """TEST-016 (QP1, RN-002): dos préstamos activos de E-02."""
        contenido = self.contenido_valido()
        segundo = dict(contenido["prestamos"][0], codigo_estudiante="2024003",
                       nombre_estudiante="Marta Ríos")
        contenido["prestamos"].append(segundo)
        self.assert_contenido_rechazado(contenido)


if __name__ == "__main__":
    unittest.main()
