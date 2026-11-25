"""Pruebas de TASK-002: modelo y excepciones."""
import unittest
from datetime import date

from biblioteca.errores import (
    CampoVacio,
    DatosCorruptos,
    EjemplarDuplicado,
    EjemplarNoDisponible,
    EjemplarNoEncontrado,
    EjemplarNoPrestado,
    ErrorBiblioteca,
    ErrorPersistencia,
    FechaPrevistaInvalida,
)
from biblioteca.modelo import Ejemplar, Prestamo


def _prestamo(fecha_prevista=date(2026, 11, 24), fecha_devolucion=None):
    return Prestamo(
        identificador_ejemplar="E-02",
        codigo_estudiante="2024001",
        nombre_estudiante="Ana Pérez",
        fecha_prestamo=date(2026, 11, 20),
        fecha_prevista=fecha_prevista,
        fecha_devolucion=fecha_devolucion,
    )


class TestModelo(unittest.TestCase):

    def test_TEST_002_activo_segun_fecha_de_devolucion(self):
        """TEST-002 (RN-009, DEC-003): un préstamo está activo mientras no tenga fecha de devolución."""
        prestamo = _prestamo()
        self.assertTrue(prestamo.activo)

        prestamo.fecha_devolucion = date(2026, 11, 24)
        self.assertFalse(prestamo.activo)

        # DEC-003: el estado no se almacena en el ejemplar; se deduce de los préstamos.
        ejemplar = Ejemplar("E-01", "Cálculo I", "Stewart")
        self.assertEqual(
            (ejemplar.identificador, ejemplar.titulo, ejemplar.autor),
            ("E-01", "Cálculo I", "Stewart"),
        )
        self.assertFalse(hasattr(ejemplar, "estado"))

    def test_TEST_003_dias_atraso(self):
        """TEST-003 (RN-006): 0 hasta la fecha prevista inclusive; luego, los días transcurridos."""
        prestamo = _prestamo(fecha_prevista=date(2026, 11, 24))
        self.assertEqual(prestamo.dias_atraso(date(2026, 11, 20)), 0)
        self.assertEqual(prestamo.dias_atraso(date(2026, 11, 24)), 0)
        self.assertEqual(prestamo.dias_atraso(date(2026, 11, 25)), 1)


class TestErrores(unittest.TestCase):

    def test_TEST_004_excepciones_conservan_dato_y_jerarquia(self):
        """TEST-004 (diseño §6): cada excepción conserva su dato y respeta la jerarquía."""
        casos = [
            (CampoVacio("titulo"), "campo", "titulo"),
            (EjemplarDuplicado("E-01"), "identificador", "E-01"),
            (EjemplarNoEncontrado("E-99"), "identificador", "E-99"),
            (EjemplarNoDisponible("E-02"), "identificador", "E-02"),
            (EjemplarNoPrestado("E-01"), "identificador", "E-01"),
        ]
        for error, atributo, valor in casos:
            with self.subTest(error=type(error).__name__):
                self.assertEqual(getattr(error, atributo), valor)
                self.assertIsInstance(error, ErrorBiblioteca)

        fecha = FechaPrevistaInvalida(date(2026, 11, 23), date(2026, 11, 24))
        self.assertEqual(fecha.fecha_prevista, date(2026, 11, 23))
        self.assertEqual(fecha.fecha_prestamo, date(2026, 11, 24))
        self.assertIsInstance(fecha, ErrorBiblioteca)

        for error in (ErrorPersistencia("disco lleno"), DatosCorruptos("JSON inválido")):
            with self.subTest(error=type(error).__name__):
                self.assertTrue(error.detalle)
                self.assertNotIsInstance(error, ErrorBiblioteca)


if __name__ == "__main__":
    unittest.main()
