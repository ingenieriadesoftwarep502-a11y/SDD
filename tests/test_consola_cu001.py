"""Pruebas de TASK-011: consola, registrar ejemplar (CU-001), con el servicio real y repositorio falso."""
import unittest

from biblioteca.consola import Consola
from biblioteca.modelo import Ejemplar
from tests.test_consola_base import EntradaSimulada, SalidaSimulada
from tests.test_repositorio import datos_d1
from tests.test_servicio_ejemplares import RepositorioFalso, biblioteca_con

OPCION_REGISTRAR, OPCION_SALIR = "1", "6"
AVISO_CANCELAR = "Escriba cancelar"


def ejecutar_consola(repositorio, *respuestas):
    """Ejecuta el menú con las respuestas dadas, seguidas de Salir."""
    biblioteca = biblioteca_con(repositorio)
    salida = SalidaSimulada()
    Consola(biblioteca, entrada=EntradaSimulada(*respuestas, OPCION_SALIR), salida=salida).ejecutar()
    return biblioteca, salida


class TestConsolaRegistrarEjemplar(unittest.TestCase):

    def test_TEST_057_registro_valido(self):
        """TEST-057 (CU-001, HU-001.CA1, DEC-011): registra, confirma y avisa una vez cómo cancelar."""
        repositorio = RepositorioFalso()

        biblioteca, salida = ejecutar_consola(
            repositorio, OPCION_REGISTRAR, "E-01", "Cálculo I", "Stewart")

        self.assertEqual(biblioteca.ejemplares["E-01"], Ejemplar("E-01", "Cálculo I", "Stewart"))
        self.assertEqual(repositorio.guardados, 1)
        self.assertEqual(salida.contar("Ejemplar E-01 registrado"), 1)
        self.assertEqual(salida.contar(AVISO_CANCELAR), 1)

    def test_TEST_058_identificador_duplicado_se_vuelve_a_pedir(self):
        """TEST-058 (CU-001 4b, HU-001.CA2): E-01 ya existe; se vuelve a pedir y se registra E-04."""
        biblioteca, salida = ejecutar_consola(
            RepositorioFalso(*datos_d1()), OPCION_REGISTRAR, "E-01", "E-04", "Álgebra", "Grossman")

        self.assertEqual(salida.contar("ya registrado"), 1)
        self.assertEqual(biblioteca.ejemplares["E-04"], Ejemplar("E-04", "Álgebra", "Grossman"))
        self.assertEqual(biblioteca.ejemplares["E-01"].titulo, "Cálculo I")

    def test_TEST_059_titulo_vacio_se_vuelve_a_pedir(self):
        """TEST-059 (CU-001 6a, HU-001.CA3): un título vacío se informa y se vuelve a pedir."""
        biblioteca, salida = ejecutar_consola(
            RepositorioFalso(), OPCION_REGISTRAR, "E-01", "", "Cálculo I", "Stewart")

        self.assertEqual(salida.contar("Título» es obligatorio"), 1)
        self.assertEqual(biblioteca.ejemplares["E-01"].titulo, "Cálculo I")

    def test_TEST_060_cancelar_a_mitad_no_registra(self):
        """TEST-060 (RC-1): "cancelar" al pedir el autor vuelve al menú sin registrar nada."""
        repositorio = RepositorioFalso()

        biblioteca, salida = ejecutar_consola(
            repositorio, OPCION_REGISTRAR, "E-01", "Cálculo I", "cancelar")

        self.assertEqual(biblioteca.ejemplares, {})
        self.assertEqual(repositorio.guardados, 0)
        self.assertEqual(salida.contar("Operación cancelada"), 1)


if __name__ == "__main__":
    unittest.main()
