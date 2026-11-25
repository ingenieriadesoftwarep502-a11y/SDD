"""Pruebas de TASK-007: servicio, registrar devolución (HOY = 24/11/2026)."""
import unittest
from datetime import date

from biblioteca.errores import (
    CampoVacio,
    EjemplarNoEncontrado,
    EjemplarNoPrestado,
    ErrorPersistencia,
)
from tests.test_repositorio import datos_d1
from tests.test_servicio_ejemplares import HOY, RepositorioFalso, biblioteca_con


class TestRegistrarDevolucion(unittest.TestCase):

    def setUp(self):
        self.repositorio = RepositorioFalso(*datos_d1())
        self.biblioteca = biblioteca_con(self.repositorio)
        self.p1 = self.biblioteca.activos["E-02"]

    def assert_sin_cambios(self):
        self.assertIsNone(self.p1.fecha_devolucion)
        self.assertIs(self.biblioteca.activos.get("E-02"), self.p1)
        self.assertEqual(len(self.biblioteca.prestamos), 1)
        self.assertEqual(self.repositorio.guardados, 0)

    def test_TEST_033_devolucion_valida(self):
        """TEST-033 (HU-005.CA1, CE-4): P1 se cierra con fecha de hoy y E-02 queda disponible."""
        devuelto = self.biblioteca.registrar_devolucion("E-02")

        self.assertIs(devuelto, self.p1)
        self.assertEqual(devuelto.fecha_devolucion, HOY)
        self.assertNotIn("E-02", self.biblioteca.activos)
        self.assertEqual(self.repositorio.guardados, 1)

    def test_TEST_034_ejemplar_disponible(self):
        """TEST-034 (HU-005.CA2, RN-007): devolver un ejemplar disponible se rechaza sin cambios."""
        with self.assertRaises(EjemplarNoPrestado):
            self.biblioteca.registrar_devolucion("E-01")
        self.assert_sin_cambios()

    def test_TEST_035_ejemplar_inexistente(self):
        """TEST-035 (HU-005.CA3): un identificador que no existe se rechaza; uno vacío da CampoVacio."""
        with self.assertRaises(EjemplarNoEncontrado):
            self.biblioteca.registrar_devolucion("E-99")

        # Decisión del equipo (TASK-007): identificador vacío o con solo espacios → CampoVacio.
        for valor in ("", "   "):
            with self.subTest(identificador=repr(valor)):
                with self.assertRaises(CampoVacio) as contexto:
                    self.biblioteca.registrar_devolucion(valor)
                self.assertEqual(contexto.exception.campo, "identificador")
        self.assert_sin_cambios()

    def test_TEST_036_prestamo_vencido_se_acepta(self):
        """TEST-036 (HU-005.CA4): un préstamo vencido se devuelve igual que uno a tiempo."""
        self.p1.fecha_prevista = date(2026, 11, 20)

        devuelto = self.biblioteca.registrar_devolucion("E-02")

        self.assertEqual(devuelto.fecha_devolucion, HOY)
        self.assertNotIn("E-02", self.biblioteca.activos)

    def test_TEST_037_el_prestamo_cerrado_se_conserva(self):
        """TEST-037 (HU-005.CA5, RN-008): P1 cerrado sigue en el historial con todos sus datos."""
        self.biblioteca.registrar_devolucion("E-02")

        self.assertEqual(len(self.biblioteca.prestamos), 1)
        cerrado = self.biblioteca.prestamos[0]
        self.assertIs(cerrado, self.p1)
        self.assertEqual(
            (cerrado.identificador_ejemplar, cerrado.codigo_estudiante, cerrado.nombre_estudiante,
             cerrado.fecha_prestamo, cerrado.fecha_prevista, cerrado.fecha_devolucion),
            ("E-02", "2024001", "Ana Pérez", date(2026, 11, 20), date(2026, 11, 30), HOY),
        )

    def test_TEST_038_se_puede_volver_a_prestar(self):
        """TEST-038 (RN-002, RN-007): después de devolver E-02 se puede prestar de nuevo."""
        self.biblioteca.registrar_devolucion("E-02")

        nuevo = self.biblioteca.registrar_prestamo("E-02", "2024003", "Marta Ríos", date(2026, 12, 1))

        self.assertIs(self.biblioteca.activos["E-02"], nuevo)
        self.assertEqual(len(self.biblioteca.prestamos), 2)

    def test_TEST_039_fallo_al_guardar_revierte(self):
        """TEST-039 (RNF-005): si guardar falla, P1 sigue activo y E-02 prestado."""
        self.repositorio.falla_al_guardar = True

        with self.assertRaises(ErrorPersistencia):
            self.biblioteca.registrar_devolucion("E-02")

        self.assert_sin_cambios()


if __name__ == "__main__":
    unittest.main()
