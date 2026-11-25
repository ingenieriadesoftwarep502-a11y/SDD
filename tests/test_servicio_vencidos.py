"""Pruebas de TASK-009: servicio, préstamos vencidos (HOY = 24/11/2026)."""
import unittest
from datetime import date

from biblioteca.modelo import Prestamo
from tests.test_repositorio import datos_d1, datos_d2
from tests.test_servicio_ejemplares import HOY, RepositorioFalso, biblioteca_con


def activo(identificador, fecha_prevista):
    """Préstamo activo de un ejemplar de D1, prestado el 01/11/2026."""
    return Prestamo(identificador, "2024001", "Ana Pérez", date(2026, 11, 1), fecha_prevista)


def biblioteca_con_prestamos(prestamos):
    """Catálogo de D1 (E-01, E-02, E-03) con los préstamos indicados."""
    ejemplares, _ = datos_d1()
    return biblioteca_con(RepositorioFalso(ejemplares, prestamos))


def previstas(vencidos):
    return [p.fecha_prevista for _, p in vencidos]


class TestListarVencidos(unittest.TestCase):

    def test_TEST_047_solo_los_anteriores_a_hoy(self):
        """TEST-047 (HU-008.CA1, RN-006, CE-2): con previstas 20/11, 24/11 y 30/11, solo vence la del 20/11."""
        biblioteca = biblioteca_con_prestamos([
            activo("E-01", date(2026, 11, 20)),
            activo("E-02", date(2026, 11, 24)),
            activo("E-03", date(2026, 11, 30)),
        ])

        fecha_usada, vencidos = biblioteca.listar_vencidos()

        self.assertEqual(fecha_usada, HOY)
        self.assertEqual(len(vencidos), 1)
        ejemplar, prestamo = vencidos[0]
        self.assertEqual(ejemplar.identificador, "E-01")
        self.assertEqual(prestamo.fecha_prevista, date(2026, 11, 20))

    def test_TEST_048_un_prestamo_devuelto_tarde_no_aparece(self):
        """TEST-048 (HU-008.CA2): con D2, P2 (devuelto con atraso) no aparece y P1 está a tiempo."""
        biblioteca = biblioteca_con(RepositorioFalso(*datos_d2()))

        self.assertEqual(biblioteca.listar_vencidos(), (HOY, []))

    def test_TEST_049_sin_vencidos(self):
        """TEST-049 (HU-008.CA4): con D1 no hay vencidos y se devuelve la fecha usada."""
        biblioteca = biblioteca_con(RepositorioFalso(*datos_d1()))

        self.assertEqual(biblioteca.listar_vencidos(), (HOY, []))

    def test_TEST_050_orden_de_mas_a_menos_atraso(self):
        """TEST-050 (QP3): de más a menos atraso; a igual atraso, por identificador."""
        biblioteca = biblioteca_con_prestamos([
            activo("E-01", date(2026, 11, 20)),
            activo("E-02", date(2026, 11, 10)),
            activo("E-03", date(2026, 11, 15)),
        ])
        _, vencidos = biblioteca.listar_vencidos()
        self.assertEqual(previstas(vencidos),
                         [date(2026, 11, 10), date(2026, 11, 15), date(2026, 11, 20)])

        # Decisión del equipo (TASK-009): a igual atraso, se ordena por identificador.
        with self.subTest(caso="empate de atraso"):
            biblioteca = biblioteca_con_prestamos([
                activo("E-03", date(2026, 11, 15)),
                activo("E-02", date(2026, 11, 20)),
                activo("E-01", date(2026, 11, 15)),
            ])
            _, vencidos = biblioteca.listar_vencidos()
            self.assertEqual([e.identificador for e, _ in vencidos], ["E-01", "E-03", "E-02"])


if __name__ == "__main__":
    unittest.main()
