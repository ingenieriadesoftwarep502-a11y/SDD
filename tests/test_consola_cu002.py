"""Pruebas de TASK-012: consola, consultar ejemplares (CU-002), con el servicio real y repositorio falso."""
import unittest

from tests.test_consola_cu001 import ejecutar_consola
from tests.test_repositorio import datos_d1
from tests.test_servicio_ejemplares import RepositorioFalso

OPCION_CONSULTAR = "2"
CATALOGO, POR_IDENTIFICADOR, DISPONIBLES, PRESTADOS = "1", "2", "3", "4"


def consultar(repositorio, *respuestas):
    """Entra a "Consultar ejemplares" con las respuestas dadas y devuelve la salida."""
    _, salida = ejecutar_consola(repositorio, OPCION_CONSULTAR, *respuestas)
    return salida


def linea_de(salida, identificador):
    """La única línea de resultado que empieza con el identificador dado."""
    lineas = [l for l in salida.lineas if l.startswith(f"{identificador} |")]
    assert len(lineas) == 1, f"Se esperaba una línea para {identificador}: {lineas}"
    return lineas[0]


def lineas_de_resultado(salida):
    return [l for l in salida.lineas if " | " in l]


class TestConsolaConsultas(unittest.TestCase):

    def test_TEST_061_catalogo(self):
        """TEST-061 (HU-002.CA1, CA2): catálogo con identificador, título, autor y estado; vacío con D0."""
        salida = consultar(RepositorioFalso(*datos_d1()), CATALOGO)

        esperados = {
            "E-01": ("Cálculo I", "Stewart", "disponible"),
            "E-02": ("Cálculo I", "Stewart", "prestado"),
            "E-03": ("Física", "Serway", "disponible"),
        }
        for identificador, campos in esperados.items():
            with self.subTest(ejemplar=identificador):
                linea = linea_de(salida, identificador)
                for campo in campos:
                    self.assertIn(campo, linea)

        with self.subTest(caso="D0"):
            salida = consultar(RepositorioFalso(), CATALOGO)
            self.assertEqual(salida.contar("No hay ejemplares registrados"), 1)

        # Decisiones del equipo (TASK-012): una opción inválida del submenú se vuelve a pedir,
        # y el aviso de "cancelar" aparece una sola vez por operación (DEC-011).
        with self.subTest(caso="opción inválida y aviso de cancelar"):
            salida = consultar(RepositorioFalso(*datos_d1()), "9", CATALOGO)
            self.assertEqual(salida.contar("Consulta no válida"), 1)
            self.assertEqual(len(lineas_de_resultado(salida)), 3)
            self.assertEqual(salida.contar("Escriba cancelar"), 1)

    def test_TEST_062_por_identificador(self):
        """TEST-062 (HU-003.CA1, CA2): E-01 disponible; E-02 prestado con estudiante y fecha prevista."""
        salida = consultar(RepositorioFalso(*datos_d1()), POR_IDENTIFICADOR, "E-01")
        linea = linea_de(salida, "E-01")
        for campo in ("Cálculo I", "Stewart", "disponible"):
            self.assertIn(campo, linea)

        salida = consultar(RepositorioFalso(*datos_d1()), POR_IDENTIFICADOR, "E-02")
        linea = linea_de(salida, "E-02")
        for campo in ("Cálculo I", "Stewart", "prestado", "2024001", "Ana Pérez", "30/11/2026"):
            self.assertIn(campo, linea)

    def test_TEST_063_identificador_inexistente(self):
        """TEST-063 (HU-003.CA3): consultar E-99 informa que no está registrado."""
        salida = consultar(RepositorioFalso(*datos_d1()), POR_IDENTIFICADOR, "E-99")

        self.assertEqual(salida.contar("no está registrado"), 1)
        self.assertEqual(lineas_de_resultado(salida), [])

    def test_TEST_064_disponibles_y_prestados(self):
        """TEST-064 (HU-006.CA1–2, HU-007.CA1–2): solo los que corresponden; mensajes de lista vacía con D0."""
        salida = consultar(RepositorioFalso(*datos_d1()), DISPONIBLES)
        self.assertEqual([l.split(" | ")[0] for l in lineas_de_resultado(salida)], ["E-01", "E-03"])
        for campo in ("Física", "Serway"):
            self.assertIn(campo, linea_de(salida, "E-03"))

        salida = consultar(RepositorioFalso(*datos_d1()), PRESTADOS)
        self.assertEqual([l.split(" | ")[0] for l in lineas_de_resultado(salida)], ["E-02"])
        for campo in ("Cálculo I", "2024001", "Ana Pérez", "20/11/2026", "30/11/2026"):
            self.assertIn(campo, linea_de(salida, "E-02"))

        with self.subTest(caso="D0"):
            self.assertEqual(consultar(RepositorioFalso(), DISPONIBLES)
                             .contar("No hay ejemplares disponibles"), 1)
            self.assertEqual(consultar(RepositorioFalso(), PRESTADOS)
                             .contar("No hay ejemplares prestados"), 1)


if __name__ == "__main__":
    unittest.main()
