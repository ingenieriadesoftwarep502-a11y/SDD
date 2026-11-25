"""Pruebas de TASK-008: servicio, consultas de catálogo y estado."""
import unittest
from datetime import date

from biblioteca.errores import CampoVacio, EjemplarNoEncontrado
from tests.test_repositorio import datos_d1
from tests.test_servicio_ejemplares import RepositorioFalso, biblioteca_con


def repositorio_d1_desordenado():
    """D1 con los ejemplares cargados en orden inverso (E-03, E-02, E-01).

    Así las pruebas de orden fallan si el servicio no ordena por identificador (QP3).
    """
    ejemplares, prestamos = datos_d1()
    return RepositorioFalso(list(reversed(ejemplares)), prestamos)


def identificadores(ejemplares):
    return [e.identificador for e in ejemplares]


class TestConsultas(unittest.TestCase):

    def setUp(self):
        self.repositorio = repositorio_d1_desordenado()
        self.biblioteca = biblioteca_con(self.repositorio)
        self.p1 = self.biblioteca.activos["E-02"]

    def test_TEST_040_catalogo_completo_ordenado(self):
        """TEST-040 (HU-002.CA1, QP3): los 3 ejemplares en orden; solo E-02 tiene préstamo."""
        catalogo = self.biblioteca.listar_catalogo()

        self.assertEqual(identificadores(e for e, _ in catalogo), ["E-01", "E-02", "E-03"])
        self.assertEqual([p for _, p in catalogo], [None, self.p1, None])

    def test_TEST_041_listas_vacias_con_catalogo_vacio(self):
        """TEST-041 (HU-002.CA2, HU-006.CA2, HU-007.CA2): con D0 las tres listas salen vacías."""
        biblioteca = biblioteca_con(RepositorioFalso())

        self.assertEqual(biblioteca.listar_catalogo(), [])
        self.assertEqual(biblioteca.listar_disponibles(), [])
        self.assertEqual(biblioteca.listar_prestados(), [])

    def test_TEST_042_consultar_por_identificador(self):
        """TEST-042 (HU-003.CA1, HU-003.CA2, CE-1): E-01 sin préstamo; E-02 con P1."""
        ejemplar, prestamo = self.biblioteca.consultar_ejemplar("E-01")
        self.assertEqual(ejemplar.identificador, "E-01")
        self.assertIsNone(prestamo)

        ejemplar, prestamo = self.biblioteca.consultar_ejemplar("E-02")
        self.assertEqual(ejemplar.identificador, "E-02")
        self.assertIs(prestamo, self.p1)
        self.assertEqual(
            (prestamo.codigo_estudiante, prestamo.nombre_estudiante, prestamo.fecha_prevista),
            ("2024001", "Ana Pérez", date(2026, 11, 30)),
        )

    def test_TEST_043_identificador_inexistente(self):
        """TEST-043 (HU-003.CA3): un identificador que no existe se rechaza; uno vacío da CampoVacio."""
        with self.assertRaises(EjemplarNoEncontrado):
            self.biblioteca.consultar_ejemplar("E-99")

        # Decisión del equipo (TASK-008): identificador vacío o con solo espacios → CampoVacio.
        for valor in ("", "   "):
            with self.subTest(identificador=repr(valor)):
                with self.assertRaises(CampoVacio) as contexto:
                    self.biblioteca.consultar_ejemplar(valor)
                self.assertEqual(contexto.exception.campo, "identificador")

    def test_TEST_044_disponibles(self):
        """TEST-044 (HU-006.CA1): solo E-01 y E-03, en orden."""
        self.assertEqual(identificadores(self.biblioteca.listar_disponibles()), ["E-01", "E-03"])

    def test_TEST_045_prestados(self):
        """TEST-045 (HU-007.CA1): solo E-02, con P1."""
        prestados = self.biblioteca.listar_prestados()

        self.assertEqual(len(prestados), 1)
        ejemplar, prestamo = prestados[0]
        self.assertEqual(ejemplar.identificador, "E-02")
        self.assertIs(prestamo, self.p1)

    def test_TEST_046_las_consultas_no_modifican_nada(self):
        """TEST-046 (diseño §3.1): las 4 consultas no llaman a guardar ni cambian el estado."""
        antes = (dict(self.biblioteca.ejemplares), list(self.biblioteca.prestamos),
                 dict(self.biblioteca.activos))

        self.biblioteca.listar_catalogo()
        self.biblioteca.consultar_ejemplar("E-02")
        self.biblioteca.listar_disponibles()
        self.biblioteca.listar_prestados()

        despues = (dict(self.biblioteca.ejemplares), list(self.biblioteca.prestamos),
                   dict(self.biblioteca.activos))
        self.assertEqual(despues, antes)
        self.assertEqual(self.repositorio.guardados, 0)


if __name__ == "__main__":
    unittest.main()
