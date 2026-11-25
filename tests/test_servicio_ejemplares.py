"""Pruebas de TASK-005: servicio, inicio y registro de ejemplares."""
import unittest
from datetime import date

from biblioteca.errores import CampoVacio, EjemplarDuplicado, ErrorPersistencia
from biblioteca.modelo import Ejemplar
from biblioteca.servicio import Biblioteca
from tests.test_repositorio import datos_d1

HOY = date(2026, 11, 24)


class RepositorioFalso:
    """Repositorio en memoria (plan de pruebas §1): cuenta los guardados y puede fallar."""

    def __init__(self, ejemplares=None, prestamos=None, falla_al_guardar=False):
        self._ejemplares = list(ejemplares or [])
        self._prestamos = list(prestamos or [])
        self.falla_al_guardar = falla_al_guardar
        self.guardados = 0

    def cargar(self):
        return list(self._ejemplares), list(self._prestamos)

    def guardar(self, ejemplares, prestamos):
        if self.falla_al_guardar:
            raise ErrorPersistencia("fallo simulado")
        self._ejemplares = list(ejemplares)
        self._prestamos = list(prestamos)
        self.guardados += 1


def biblioteca_con(repositorio):
    return Biblioteca(repositorio, reloj=lambda: HOY)


class TestRegistrarEjemplar(unittest.TestCase):

    def test_TEST_017_registro_valido(self):
        """TEST-017 (HU-001.CA1): el ejemplar queda registrado, disponible y guardado."""
        repositorio = RepositorioFalso()
        biblioteca = biblioteca_con(repositorio)

        ejemplar = biblioteca.registrar_ejemplar("E-01", "Cálculo I", "Stewart")

        self.assertEqual(ejemplar, Ejemplar("E-01", "Cálculo I", "Stewart"))
        self.assertEqual(biblioteca.ejemplares["E-01"], ejemplar)
        self.assertNotIn("E-01", biblioteca.activos)
        self.assertEqual(repositorio.guardados, 1)
        self.assertEqual(repositorio.cargar()[0], [ejemplar])

    def test_TEST_018_identificador_duplicado(self):
        """TEST-018 (HU-001.CA2, RN-001): un identificador existente se rechaza sin cambios."""
        repositorio = RepositorioFalso(*datos_d1())
        biblioteca = biblioteca_con(repositorio)
        antes = dict(biblioteca.ejemplares)

        with self.assertRaises(EjemplarDuplicado) as contexto:
            biblioteca.registrar_ejemplar("E-01", "Otro", "Otro")

        self.assertEqual(contexto.exception.identificador, "E-01")
        self.assertEqual(biblioteca.ejemplares, antes)
        self.assertEqual(repositorio.guardados, 0)

    def test_TEST_019_mayusculas_y_minusculas_son_distintas(self):
        """TEST-019 (RN-001, Q4): "e-01" y "E-01" son identificadores distintos."""
        biblioteca = biblioteca_con(RepositorioFalso())

        biblioteca.registrar_ejemplar("e-01", "Cálculo I", "Stewart")
        biblioteca.registrar_ejemplar("E-01", "Cálculo I", "Stewart")

        self.assertEqual(set(biblioteca.ejemplares), {"e-01", "E-01"})

    def test_TEST_020_espacios_al_inicio_y_al_final(self):
        """TEST-020 (RN-001): " E-04 " se registra como "E-04" y luego "E-04" es duplicado."""
        biblioteca = biblioteca_con(RepositorioFalso())

        ejemplar = biblioteca.registrar_ejemplar(" E-04 ", "Física", "Serway")
        self.assertEqual(ejemplar.identificador, "E-04")
        self.assertIn("E-04", biblioteca.ejemplares)

        with self.assertRaises(EjemplarDuplicado):
            biblioteca.registrar_ejemplar("E-04", "Física", "Serway")

    def test_TEST_021_campo_vacio(self):
        """TEST-021 (HU-001.CA3, RN-010): campo vacío o con solo espacios → CampoVacio con su nombre."""
        validos = {"identificador": "E-01", "titulo": "Cálculo I", "autor": "Stewart"}
        for campo in validos:
            for valor in ("", "   "):
                with self.subTest(campo=campo, valor=repr(valor)):
                    repositorio = RepositorioFalso()
                    biblioteca = biblioteca_con(repositorio)
                    datos = dict(validos, **{campo: valor})

                    with self.assertRaises(CampoVacio) as contexto:
                        biblioteca.registrar_ejemplar(**datos)

                    self.assertEqual(contexto.exception.campo, campo)
                    self.assertEqual(biblioteca.ejemplares, {})
                    self.assertEqual(repositorio.guardados, 0)

    def test_TEST_022_mismo_titulo_ejemplares_independientes(self):
        """TEST-022 (HU-001.CA4): dos ejemplares del mismo título son registros independientes."""
        biblioteca = biblioteca_con(RepositorioFalso())

        biblioteca.registrar_ejemplar("E-01", "Cálculo I", "Stewart")
        biblioteca.registrar_ejemplar("E-02", "Cálculo I", "Stewart")

        self.assertEqual(
            list(biblioteca.ejemplares.values()),
            [Ejemplar("E-01", "Cálculo I", "Stewart"), Ejemplar("E-02", "Cálculo I", "Stewart")],
        )

    def test_TEST_023_fallo_al_guardar_revierte(self):
        """TEST-023 (RNF-005, RC-3): si guardar falla, el ejemplar no queda en memoria."""
        biblioteca = biblioteca_con(RepositorioFalso(falla_al_guardar=True))

        with self.assertRaises(ErrorPersistencia):
            biblioteca.registrar_ejemplar("E-01", "Cálculo I", "Stewart")

        self.assertNotIn("E-01", biblioteca.ejemplares)

    def test_TEST_024_carga_los_datos_al_iniciar(self):
        """TEST-024 (DEC-006): Biblioteca carga los datos del repositorio al crearse."""
        biblioteca = biblioteca_con(RepositorioFalso(*datos_d1()))

        with self.assertRaises(EjemplarDuplicado):
            biblioteca.registrar_ejemplar("E-03", "Física", "Serway")


if __name__ == "__main__":
    unittest.main()
