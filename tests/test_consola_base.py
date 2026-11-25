"""Pruebas de TASK-010: consola, menú y entrada de datos (E/S simulada, DEC-010)."""
import unittest
from datetime import date

from biblioteca.consola import Consola, mensaje_error
from biblioteca.errores import (
    CampoVacio,
    DatosCorruptos,
    EjemplarDuplicado,
    EjemplarNoDisponible,
    EjemplarNoEncontrado,
    EjemplarNoPrestado,
    ErrorPersistencia,
    FechaPrevistaInvalida,
)
from tests.test_servicio_ejemplares import RepositorioFalso, biblioteca_con


class EntradaSimulada:
    """Reemplaza a input(): devuelve las respuestas en orden y registra cada pregunta."""

    def __init__(self, *respuestas):
        self._respuestas = list(respuestas)
        self.preguntas = []

    def __call__(self, pregunta=""):
        self.preguntas.append(pregunta)
        if not self._respuestas:
            raise AssertionError("La consola pidió más datos de los previstos en la prueba")
        return self._respuestas.pop(0)


class SalidaSimulada:
    """Reemplaza a print(): guarda cada línea mostrada."""

    def __init__(self):
        self.lineas = []

    def __call__(self, texto=""):
        self.lineas.append(str(texto))

    def contar(self, fragmento):
        return sum(fragmento in linea for linea in self.lineas)


def consola_con(*respuestas):
    entrada, salida = EntradaSimulada(*respuestas), SalidaSimulada()
    consola = Consola(biblioteca_con(RepositorioFalso()), entrada=entrada, salida=salida)
    return consola, entrada, salida


class TestMenu(unittest.TestCase):

    def test_TEST_051_opcion_invalida(self):
        """TEST-051 (CU-006 3a, RNF-004): cada opción inválida se informa y el menú se muestra de nuevo."""
        consola, _, salida = consola_con("9", "abc", "", "6")

        consola.ejecutar()

        self.assertEqual(salida.contar("Opción no válida"), 3)
        self.assertEqual(salida.contar("6. Salir"), 4)

    def test_TEST_052_salir_termina(self):
        """TEST-052 (CU-006): la opción 6 (Salir) termina el bucle."""
        consola, entrada, _ = consola_con("6")

        consola.ejecutar()

        self.assertEqual(len(entrada.preguntas), 1)


class TestPedirDatos(unittest.TestCase):

    def test_TEST_053_texto_obligatorio(self):
        """TEST-053 (RC-2, RN-010): un texto vacío o con solo espacios se vuelve a pedir."""
        consola, _, salida = consola_con("", "  ", "Hola")

        self.assertEqual(consola.pedir_texto("Título"), "Hola")
        self.assertEqual(salida.contar("obligatorio"), 2)

    def test_TEST_054_fecha_dd_mm_aaaa(self):
        """TEST-054 (RNF-009, HU-004.CA6): solo se acepta una fecha DD/MM/AAAA existente."""
        consola, _, salida = consola_con("31/02/2026", "2026-11-24", "hola", "24/11/2026")

        self.assertEqual(consola.pedir_fecha("Fecha prevista"), date(2026, 11, 24))
        self.assertEqual(salida.contar("DD/MM/AAAA"), 3)

    def test_TEST_055_cancelar_vuelve_al_menu(self):
        """TEST-055 (RC-1, DEC-011): "cancelar" (sin distinguir mayúsculas) interrumpe la operación."""
        for palabra in ("cancelar", "CANCELAR"):
            for ayuda in ("pedir_texto", "pedir_fecha"):
                with self.subTest(palabra=palabra, ayuda=ayuda):
                    consola, _, salida = consola_con(palabra)
                    ejecutada = []

                    def operacion():
                        getattr(consola, ayuda)("Dato")
                        ejecutada.append(True)

                    consola.ejecutar_operacion(operacion)

                    self.assertEqual(ejecutada, [])
                    self.assertEqual(salida.contar("Operación cancelada"), 1)


class TestMensajes(unittest.TestCase):

    def test_TEST_056_mensajes_en_espanol_con_el_dato(self):
        """TEST-056 (RNF-003, RNF-008): cada excepción del diseño §6 da un mensaje en español con su dato."""
        casos = [
            (CampoVacio("titulo"), ["título", "obligatorio"]),
            (EjemplarDuplicado("E-01"), ["E-01", "ya existe"]),
            (EjemplarNoEncontrado("E-99"), ["E-99", "no está registrado"]),
            (EjemplarNoDisponible("E-02"), ["E-02", "ya está prestado"]),
            (EjemplarNoPrestado("E-01"), ["E-01", "no tiene préstamo activo"]),
            (FechaPrevistaInvalida(date(2026, 11, 23), date(2026, 11, 24)),
             ["23/11/2026", "24/11/2026", "no puede ser anterior"]),
            (ErrorPersistencia("disco lleno"), ["disco lleno", "No se pudo guardar"]),
            (DatosCorruptos("JSON inválido"), ["JSON inválido", "dañado"]),
        ]
        for error, fragmentos in casos:
            with self.subTest(error=type(error).__name__):
                mensaje = mensaje_error(error)
                for fragmento in fragmentos:
                    self.assertIn(fragmento.lower(), mensaje.lower())


if __name__ == "__main__":
    unittest.main()
