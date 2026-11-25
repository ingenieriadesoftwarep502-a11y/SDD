"""Pruebas de TASK-003: repositorio JSON, cargar y guardar."""
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from biblioteca.errores import ErrorPersistencia
from biblioteca.modelo import Ejemplar, Prestamo
from biblioteca.repositorio import RepositorioJSON


def datos_d1():
    """D1 (plan de pruebas §2): 3 ejemplares y el préstamo P1 activo de E-02."""
    ejemplares = [
        Ejemplar("E-01", "Cálculo I", "Stewart"),
        Ejemplar("E-02", "Cálculo I", "Stewart"),
        Ejemplar("E-03", "Física", "Serway"),
    ]
    prestamos = [
        Prestamo("E-02", "2024001", "Ana Pérez",
                 date(2026, 11, 20), date(2026, 11, 30)),
    ]
    return ejemplares, prestamos


def datos_d2():
    """D2 (plan de pruebas §2): D1 más el préstamo P2, ya devuelto."""
    ejemplares, prestamos = datos_d1()
    prestamos.append(
        Prestamo("E-01", "2024002", "Luis Núñez",
                 date(2026, 11, 1), date(2026, 11, 10), date(2026, 11, 15))
    )
    return ejemplares, prestamos


class TestRepositorio(unittest.TestCase):

    def setUp(self):
        self._carpeta = tempfile.TemporaryDirectory()
        self.carpeta = Path(self._carpeta.name)
        self.ruta = self.carpeta / "biblioteca.json"

    def tearDown(self):
        self._carpeta.cleanup()

    def test_TEST_005_guardar_y_cargar_conserva_los_datos(self):
        """TEST-005 (RNF-001, RN-008): guardar y volver a cargar devuelve los mismos datos."""
        ejemplares, prestamos = datos_d2()
        # P3 (decisión del equipo): préstamo activo a un estudiante con tildes.
        prestamos.append(
            Prestamo("E-03", "2024003", "Ñuñez Álvarez",
                     date(2026, 11, 22), date(2026, 11, 29))
        )
        repositorio = RepositorioJSON(self.ruta)

        repositorio.guardar(ejemplares, prestamos)
        cargados = RepositorioJSON(self.ruta).cargar()

        self.assertEqual(cargados, (ejemplares, prestamos))

    def test_TEST_006_archivo_inexistente_devuelve_listas_vacias(self):
        """TEST-006 (CU-006 2a): sin archivo, cargar() devuelve listas vacías y no crea nada."""
        self.assertEqual(RepositorioJSON(self.ruta).cargar(), ([], []))
        self.assertFalse(self.ruta.exists())

    def test_TEST_007_guardar_crea_la_carpeta_y_no_deja_tmp(self):
        """TEST-007 (DEC-005, DEC-012): guardar crea la carpeta y no deja ningún .tmp."""
        ruta = self.carpeta / "datos" / "sub" / "biblioteca.json"

        RepositorioJSON(ruta).guardar(*datos_d1())

        self.assertTrue(ruta.is_file())
        self.assertEqual(list(ruta.parent.glob("*.tmp")), [])

    def test_TEST_008_fallo_al_reemplazar_conserva_el_archivo_anterior(self):
        """TEST-008 (RNF-005, DEC-005): si os.replace falla, el archivo anterior queda intacto y no queda .tmp."""
        repositorio = RepositorioJSON(self.ruta)
        repositorio.guardar(*datos_d1())
        contenido_d1 = self.ruta.read_bytes()

        with mock.patch("biblioteca.repositorio.os.replace",
                        side_effect=OSError("fallo simulado")):
            with self.assertRaises(ErrorPersistencia):
                repositorio.guardar(*datos_d2())

        self.assertEqual(self.ruta.read_bytes(), contenido_d1)
        self.assertEqual(list(self.carpeta.glob("*.tmp")), [])

    def test_TEST_009_formato_del_archivo(self):
        """TEST-009 (DEC-007, diseño §4.3): versión 1, fechas ISO y tildes legibles."""
        RepositorioJSON(self.ruta).guardar(*datos_d1())
        texto = self.ruta.read_text(encoding="utf-8")

        self.assertIn('"version": 1', texto)
        self.assertIn('"2026-11-20"', texto)
        self.assertIn("Pérez", texto)
        self.assertNotIn("\\u00e9", texto)


if __name__ == "__main__":
    unittest.main()
