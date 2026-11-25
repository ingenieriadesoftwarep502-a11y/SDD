"""Pruebas de TASK-006: servicio, registrar préstamo (HOY = 24/11/2026)."""
import unittest
from datetime import date

from biblioteca.errores import (
    CampoVacio,
    EjemplarNoDisponible,
    EjemplarNoEncontrado,
    ErrorPersistencia,
    FechaPrevistaInvalida,
)
from biblioteca.modelo import Prestamo
from tests.test_repositorio import datos_d1
from tests.test_servicio_ejemplares import HOY, RepositorioFalso, biblioteca_con


class TestRegistrarPrestamo(unittest.TestCase):

    def setUp(self):
        self.repositorio = RepositorioFalso(*datos_d1())
        self.biblioteca = biblioteca_con(self.repositorio)
        self.prestamos_iniciales = list(self.biblioteca.prestamos)

    def assert_sin_prestamo_nuevo(self):
        self.assertEqual(self.biblioteca.prestamos, self.prestamos_iniciales)
        self.assertEqual(self.repositorio.guardados, 0)

    def test_TEST_025_prestamo_valido(self):
        """TEST-025 (HU-004.CA1, RN-004): préstamo activo con fecha de préstamo igual a hoy."""
        prestamo = self.biblioteca.registrar_prestamo(
            "E-01", "2024003", "Marta Ríos", date(2026, 12, 1))

        self.assertEqual(prestamo, Prestamo("E-01", "2024003", "Marta Ríos",
                                            HOY, date(2026, 12, 1), None))
        self.assertTrue(prestamo.activo)
        self.assertIs(self.biblioteca.activos["E-01"], prestamo)
        self.assertIn(prestamo, self.biblioteca.prestamos)
        self.assertEqual(self.repositorio.guardados, 1)

    def test_TEST_026_ejemplar_ya_prestado(self):
        """TEST-026 (HU-004.CA2, RN-002, CE-3): E-02 prestado no se presta a otro ni al mismo estudiante."""
        for codigo, nombre in (("2024003", "Marta Ríos"), ("2024001", "Ana Pérez")):
            with self.subTest(codigo=codigo):
                with self.assertRaises(EjemplarNoDisponible):
                    self.biblioteca.registrar_prestamo("E-02", codigo, nombre, date(2026, 12, 1))
        self.assert_sin_prestamo_nuevo()

    def test_TEST_027_ejemplar_inexistente(self):
        """TEST-027 (HU-004.CA3): un identificador que no existe se rechaza; uno vacío da CampoVacio."""
        with self.assertRaises(EjemplarNoEncontrado):
            self.biblioteca.registrar_prestamo("E-99", "2024003", "Marta Ríos", date(2026, 12, 1))

        # Decisión del equipo (TASK-006): identificador vacío o con solo espacios → CampoVacio.
        for valor in ("", "   "):
            with self.subTest(identificador=repr(valor)):
                with self.assertRaises(CampoVacio) as contexto:
                    self.biblioteca.registrar_prestamo(valor, "2024003", "Marta Ríos", date(2026, 12, 1))
                self.assertEqual(contexto.exception.campo, "identificador")
        self.assert_sin_prestamo_nuevo()

    def test_TEST_028_fecha_prevista_anterior_a_hoy(self):
        """TEST-028 (HU-004.CA4, RN-005): fecha prevista 23/11/2026 se rechaza."""
        with self.assertRaises(FechaPrevistaInvalida):
            self.biblioteca.registrar_prestamo("E-01", "2024003", "Marta Ríos", date(2026, 11, 23))
        self.assert_sin_prestamo_nuevo()

    def test_TEST_029_fecha_prevista_igual_a_hoy(self):
        """TEST-029 (HU-004.CA5, RN-005): fecha prevista igual a hoy se acepta (caso límite)."""
        prestamo = self.biblioteca.registrar_prestamo(
            "E-01", "2024003", "Marta Ríos", date(2026, 11, 24))
        self.assertEqual(prestamo.fecha_prevista, HOY)
        self.assertIn("E-01", self.biblioteca.activos)

    def test_TEST_030_codigo_o_nombre_vacio(self):
        """TEST-030 (RN-010): código vacío y, aparte, nombre con solo espacios → CampoVacio."""
        casos = (("codigo", "", "Marta Ríos"), ("nombre", "2024003", "  "))
        for campo, codigo, nombre in casos:
            with self.subTest(campo=campo):
                with self.assertRaises(CampoVacio) as contexto:
                    self.biblioteca.registrar_prestamo("E-01", codigo, nombre, date(2026, 12, 1))
                self.assertEqual(contexto.exception.campo, campo)

        # Decisión del equipo (TASK-006): con varios errores, se informa el primero según CU-003
        # (ejemplar → código → nombre → fecha prevista).
        anterior = date(2026, 11, 23)
        casos_de_orden = (
            ("ejemplar antes que código", ("E-99", "", "Marta Ríos", anterior), EjemplarNoEncontrado),
            ("disponibilidad antes que código", ("E-02", "", "Marta Ríos", anterior), EjemplarNoDisponible),
            ("código antes que nombre", ("E-01", "", "", anterior), CampoVacio),
            ("nombre antes que fecha", ("E-01", "2024003", "", anterior), CampoVacio),
        )
        for caso, argumentos, error_esperado in casos_de_orden:
            with self.subTest(orden=caso):
                with self.assertRaises(error_esperado) as contexto:
                    self.biblioteca.registrar_prestamo(*argumentos)
                if caso == "código antes que nombre":
                    self.assertEqual(contexto.exception.campo, "codigo")
                if caso == "nombre antes que fecha":
                    self.assertEqual(contexto.exception.campo, "nombre")
        self.assert_sin_prestamo_nuevo()

    def test_TEST_031_sin_limite_por_estudiante(self):
        """TEST-031 (HU-004.CA7, RN-011): el mismo estudiante puede tener varios préstamos activos."""
        self.biblioteca.registrar_prestamo("E-01", "2024001", "Ana Pérez", date(2026, 12, 1))
        self.biblioteca.registrar_prestamo("E-03", "2024001", "Ana Pérez", date(2026, 12, 1))

        activos_del_estudiante = [
            p for p in self.biblioteca.activos.values() if p.codigo_estudiante == "2024001"
        ]
        self.assertEqual(len(activos_del_estudiante), 3)

    def test_TEST_032_fallo_al_guardar_revierte(self):
        """TEST-032 (RNF-005): si guardar falla, E-01 sigue disponible y no hay préstamo nuevo."""
        self.repositorio.falla_al_guardar = True

        with self.assertRaises(ErrorPersistencia):
            self.biblioteca.registrar_prestamo("E-01", "2024003", "Marta Ríos", date(2026, 12, 1))

        self.assertNotIn("E-01", self.biblioteca.activos)
        self.assert_sin_prestamo_nuevo()


if __name__ == "__main__":
    unittest.main()
