"""Pruebas de TASK-013: consola, registrar préstamo (CU-003). HOY = 24/11/2026."""
import unittest
from datetime import date

from tests.test_consola_cu001 import ejecutar_consola
from tests.test_repositorio import datos_d1
from tests.test_servicio_ejemplares import HOY, RepositorioFalso

OPCION_PRESTAR = "3"
ESTUDIANTE = ("2024003", "Marta Ríos")


def prestar(*respuestas):
    """Entra a "Registrar préstamo" con D1 y las respuestas dadas, seguidas de Salir."""
    repositorio = RepositorioFalso(*datos_d1())
    biblioteca, salida = ejecutar_consola(repositorio, OPCION_PRESTAR, *respuestas)
    return biblioteca, salida, repositorio


class TestConsolaRegistrarPrestamo(unittest.TestCase):

    def assert_prestado_a_marta(self, biblioteca, identificador, fecha_prevista):
        prestamo = biblioteca.activos[identificador]
        self.assertEqual(
            (prestamo.codigo_estudiante, prestamo.nombre_estudiante,
             prestamo.fecha_prestamo, prestamo.fecha_prevista),
            (*ESTUDIANTE, HOY, fecha_prevista),
        )

    def test_TEST_065_prestamo_valido(self):
        """TEST-065 (CU-003, HU-004.CA1): muestra título y autor, crea el préstamo y confirma."""
        biblioteca, salida, repositorio = prestar("E-01", *ESTUDIANTE, "01/12/2026")

        self.assertEqual(salida.contar("Cálculo I"), 1)
        self.assertEqual(salida.contar("Stewart"), 1)
        self.assert_prestado_a_marta(biblioteca, "E-01", date(2026, 12, 1))
        self.assertEqual(repositorio.guardados, 1)
        self.assertEqual(salida.contar("Préstamo registrado"), 1)

    def test_TEST_066_ejemplar_prestado_se_vuelve_a_pedir(self):
        """TEST-066 (CU-003 4b, HU-004.CA2): E-02 está prestado; se vuelve a pedir y se presta E-01."""
        biblioteca, salida, _ = prestar("E-02", "E-01", *ESTUDIANTE, "01/12/2026")

        self.assertEqual(salida.contar("ya está prestado"), 1)
        self.assert_prestado_a_marta(biblioteca, "E-01", date(2026, 12, 1))
        self.assertEqual(biblioteca.activos["E-02"].codigo_estudiante, "2024001")

        # Decisión del equipo (TASK-013): CU-003 4a, un ejemplar inexistente se informa y se vuelve a pedir.
        with self.subTest(caso="4a: ejemplar inexistente"):
            biblioteca, salida, _ = prestar("E-99", "E-01", *ESTUDIANTE, "01/12/2026")
            self.assertEqual(salida.contar("no está registrado"), 1)
            self.assert_prestado_a_marta(biblioteca, "E-01", date(2026, 12, 1))

    def test_TEST_067_fecha_inexistente_se_vuelve_a_pedir(self):
        """TEST-067 (CU-003 11a, HU-004.CA6): "31/02/2026" muestra el formato y se vuelve a pedir."""
        biblioteca, salida, _ = prestar("E-01", *ESTUDIANTE, "31/02/2026", "01/12/2026")

        self.assertEqual(salida.contar("Fecha no válida"), 1)
        self.assertGreaterEqual(salida.contar("DD/MM/AAAA"), 1)
        self.assert_prestado_a_marta(biblioteca, "E-01", date(2026, 12, 1))

    def test_TEST_068_fecha_anterior_se_vuelve_a_pedir(self):
        """TEST-068 (CU-003 11b, HU-004.CA4): 23/11/2026 se rechaza; se vuelve a pedir y 24/11/2026 se acepta."""
        biblioteca, salida, _ = prestar("E-01", *ESTUDIANTE, "23/11/2026", "24/11/2026")

        self.assertEqual(salida.contar("no puede ser anterior"), 1)
        self.assert_prestado_a_marta(biblioteca, "E-01", date(2026, 11, 24))

    def test_TEST_069_cancelar_no_presta(self):
        """TEST-069 (RC-1): "cancelar" al pedir la fecha no crea el préstamo; E-01 sigue disponible."""
        biblioteca, salida, repositorio = prestar("E-01", *ESTUDIANTE, "cancelar")

        self.assertNotIn("E-01", biblioteca.activos)
        self.assertEqual(len(biblioteca.prestamos), 1)
        self.assertEqual(repositorio.guardados, 0)
        self.assertEqual(salida.contar("Operación cancelada"), 1)

    def test_TEST_070_no_se_pide_confirmacion(self):
        """TEST-070 (QP4 rechazada): con exactamente 4 datos y Salir, el préstamo se crea.

        Si la consola pidiera una confirmación, consumiría el "6" de Salir y luego pediría
        otro dato; la entrada simulada falla en ese caso.
        """
        biblioteca, _, _ = prestar("E-01", *ESTUDIANTE, "01/12/2026")

        self.assertIn("E-01", biblioteca.activos)


if __name__ == "__main__":
    unittest.main()
