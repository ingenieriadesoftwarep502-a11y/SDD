"""Pruebas de TASK-014: consola, registrar devolución (CU-004) y préstamos vencidos (CU-005). HOY = 24/11/2026."""
import unittest
from datetime import date

from tests.test_consola_cu001 import ejecutar_consola
from tests.test_repositorio import datos_d1
from tests.test_servicio_ejemplares import RepositorioFalso

OPCION_DEVOLVER, OPCION_VENCIDOS = "4", "5"


class TestConsolaDevolucion(unittest.TestCase):

    def test_TEST_071_devolucion_valida(self):
        """TEST-071 (CU-004, HU-005.CA1): devolver E-02 confirma y lo deja disponible."""
        repositorio = RepositorioFalso(*datos_d1())

        biblioteca, salida = ejecutar_consola(repositorio, OPCION_DEVOLVER, "E-02")

        self.assertEqual(salida.contar("Devolución registrada"), 1)
        self.assertNotIn("E-02", biblioteca.activos)
        self.assertEqual(repositorio.guardados, 1)

    def test_TEST_072_ejemplar_no_prestado(self):
        """TEST-072 (CU-004 4b, HU-005.CA2): devolver E-01 informa que no tiene préstamo activo."""
        repositorio = RepositorioFalso(*datos_d1())

        biblioteca, salida = ejecutar_consola(repositorio, OPCION_DEVOLVER, "E-01", "cancelar")

        self.assertEqual(salida.contar("no tiene préstamo activo"), 1)
        self.assertIn("E-02", biblioteca.activos)
        self.assertEqual(repositorio.guardados, 0)

        # Decisión del equipo (TASK-014): CU-004 4a, un ejemplar inexistente se informa y se vuelve a pedir.
        with self.subTest(caso="4a: ejemplar inexistente"):
            biblioteca, salida = ejecutar_consola(
                RepositorioFalso(*datos_d1()), OPCION_DEVOLVER, "E-99", "E-02")
            self.assertEqual(salida.contar("no está registrado"), 1)
            self.assertEqual(salida.contar("Devolución registrada"), 1)
            self.assertNotIn("E-02", biblioteca.activos)


class TestConsolaVencidos(unittest.TestCase):

    def test_TEST_073_listado_de_vencidos(self):
        """TEST-073 (CU-005, HU-008.CA3): fecha usada y, por préstamo, todos los campos y días de atraso."""
        ejemplares, prestamos = datos_d1()
        prestamos[0].fecha_prevista = date(2026, 11, 20)  # P1 vencido hace 4 días

        _, salida = ejecutar_consola(RepositorioFalso(ejemplares, prestamos), OPCION_VENCIDOS)

        self.assertEqual(salida.contar("24/11/2026"), 1)
        linea = [l for l in salida.lineas if l.startswith("E-02 |")]
        self.assertEqual(len(linea), 1)
        for campo in ("Cálculo I", "2024001", "Ana Pérez", "20/11/2026", "4 días"):
            self.assertIn(campo, linea[0])

    def test_TEST_074_sin_vencidos(self):
        """TEST-074 (HU-008.CA4): sin vencidos se informa, junto con la fecha usada."""
        _, salida = ejecutar_consola(RepositorioFalso(*datos_d1()), OPCION_VENCIDOS)

        mensajes = [l for l in salida.lineas if "No hay préstamos vencidos" in l]
        self.assertEqual(len(mensajes), 1)
        self.assertIn("24/11/2026", mensajes[0])

        # Decisión del equipo (TASK-014): "Préstamos vencidos" no pide datos y no muestra el aviso de cancelar.
        self.assertEqual(salida.contar("Escriba cancelar"), 0)


if __name__ == "__main__":
    unittest.main()
