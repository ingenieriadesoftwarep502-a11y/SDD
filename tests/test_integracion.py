"""Pruebas de TASK-015: punto de entrada e inicio/cierre (CU-006), con el archivo real en una carpeta temporal."""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from biblioteca.__main__ import main
from tests.test_consola_base import EntradaSimulada, SalidaSimulada
from tests.test_servicio_ejemplares import HOY


def ejecutar(ruta, *respuestas):
    """Ejecuta la aplicación completa con la ruta y las respuestas dadas; devuelve (código, salida)."""
    salida = SalidaSimulada()
    codigo = main([str(ruta)], entrada=EntradaSimulada(*respuestas), salida=salida, reloj=lambda: HOY)
    return codigo, salida


class TestIntegracion(unittest.TestCase):

    def setUp(self):
        self._carpeta = tempfile.TemporaryDirectory()
        self.ruta = Path(self._carpeta.name) / "datos" / "biblioteca.json"

    def tearDown(self):
        self._carpeta.cleanup()

    def test_TEST_075_los_datos_se_conservan_entre_ejecuciones(self):
        """TEST-075 (RNF-001, CE-5): lo registrado en una ejecución sigue en la siguiente."""
        codigo, _ = ejecutar(
            self.ruta,
            "1", "E-01", "Cálculo I", "Stewart",                      # registrar ejemplar
            "3", "E-01", "2024003", "Marta Ríos", "01/12/2026",       # prestarlo
            "6")                                                       # salir
        self.assertEqual(codigo, 0)

        codigo, salida = ejecutar(self.ruta, "2", "2", "E-01", "6")    # consultar E-01 y salir
        self.assertEqual(codigo, 0)
        linea = [l for l in salida.lineas if l.startswith("E-01 |")]
        self.assertEqual(len(linea), 1)
        for campo in ("Cálculo I", "Stewart", "prestado", "2024003", "Marta Ríos", "01/12/2026"):
            self.assertIn(campo, linea[0])

    def test_TEST_076_archivo_danado(self):
        """TEST-076 (QP1, CU-006 2b): JSON inválido → mensaje con la ruta, código 1, archivo intacto."""
        self.ruta.parent.mkdir(parents=True)
        self.ruta.write_text("{ejemplares: [", encoding="utf-8")
        antes = self.ruta.read_bytes()

        codigo, salida = ejecutar(self.ruta)

        self.assertEqual(codigo, 1)
        self.assertEqual(salida.contar(str(self.ruta)), 1)
        self.assertEqual(self.ruta.read_bytes(), antes)

        # Decisiones del equipo (TASK-015): otros inicios fallidos.
        with self.subTest(caso="sin permiso de lectura"):
            with mock.patch.object(Path, "read_bytes", side_effect=PermissionError("Permiso denegado")):
                codigo, salida = ejecutar(self.ruta)
            self.assertEqual(codigo, 1)
            self.assertEqual(salida.contar("No se pudo leer el archivo de datos"), 1)
            self.assertEqual(self.ruta.read_bytes(), antes)

        with self.subTest(caso="argumentos de más"):
            salida = SalidaSimulada()
            otra = self.ruta.parent / "otra.json"
            codigo = main([str(self.ruta), str(otra)], entrada=EntradaSimulada(), salida=salida)
            self.assertEqual(codigo, 2)
            self.assertEqual(salida.contar("Uso: python -m biblioteca [RUTA]"), 1)
            self.assertFalse(otra.exists())

    def test_TEST_077_fin_de_entrada_termina_ordenadamente(self):
        """TEST-077 (RNF-004): con fin de entrada (EOF) o Ctrl+C en el menú, cierra sin error y lo informa."""
        for interrupcion in (EOFError, KeyboardInterrupt):
            with self.subTest(interrupcion=interrupcion.__name__):
                def entrada_interrumpida(pregunta=""):
                    raise interrupcion

                salida = SalidaSimulada()
                try:
                    codigo = main([str(self.ruta)], entrada=entrada_interrumpida,
                                  salida=salida, reloj=lambda: HOY)
                except (EOFError, KeyboardInterrupt):
                    self.fail(f"La aplicación no manejó {interrupcion.__name__}")

                self.assertEqual(codigo, 0)
                # Decisión del equipo (TASK-015): se muestra "Aplicación cerrada.".
                self.assertEqual(salida.contar("Aplicación cerrada."), 1)

    def test_TEST_078_primer_uso_sin_archivo(self):
        """TEST-078 (CU-006 2a): sin archivo, inicia con el catálogo vacío y sin error."""
        codigo, salida = ejecutar(self.ruta, "2", "1", "6")

        self.assertEqual(codigo, 0)
        self.assertEqual(salida.contar("No hay ejemplares registrados"), 1)


if __name__ == "__main__":
    unittest.main()
