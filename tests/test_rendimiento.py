"""Prueba de TASK-016: rendimiento (RNF-006).

Es lenta, así que solo se ejecuta con la variable de entorno RENDIMIENTO=1 (QT2).
En PowerShell: $env:RENDIMIENTO="1"; python -m unittest tests.test_rendimiento -v
"""
import os
import tempfile
import time
import unittest
from datetime import date, timedelta
from pathlib import Path

from biblioteca.modelo import Ejemplar, Prestamo
from biblioteca.repositorio import RepositorioJSON
from biblioteca.servicio import Biblioteca
from tests.test_servicio_ejemplares import HOY

EJEMPLARES, PRESTAMOS, ACTIVOS, VENCIDOS = 5_000, 20_000, 1_000, 200
LIMITE_CONSULTA_S = 1.0  # RNF-006


def generar_datos():
    """5.000 ejemplares y 20.000 préstamos: 1.000 activos (200 vencidos a HOY) y 19.000 devueltos."""
    ejemplares = [Ejemplar(f"E-{i:05d}", f"Título {i}", f"Autor {i % 300}")
                  for i in range(1, EJEMPLARES + 1)]
    prestamos = []
    for i in range(ACTIVOS):  # un préstamo activo en cada uno de los primeros 1.000 ejemplares
        vencido = i < VENCIDOS
        prevista = HOY - timedelta(days=1 + i % 30) if vencido else HOY + timedelta(days=1 + i % 30)
        prestamos.append(Prestamo(ejemplares[i].identificador, f"{2024000 + i}", f"Estudiante {i}",
                                  prevista - timedelta(days=14), prevista))
    for i in range(PRESTAMOS - ACTIVOS):  # historial de préstamos devueltos
        inicio = date(2025, 1, 1) + timedelta(days=i % 600)
        prestamos.append(Prestamo(ejemplares[i % EJEMPLARES].identificador, f"{2025000 + i % 3000}",
                                  f"Estudiante {i % 3000}", inicio, inicio + timedelta(days=14),
                                  inicio + timedelta(days=10)))
    return ejemplares, prestamos


def medir(funcion):
    inicio = time.perf_counter()
    resultado = funcion()
    return resultado, time.perf_counter() - inicio


@unittest.skipUnless(os.environ.get("RENDIMIENTO") == "1",
                     "prueba lenta: defina RENDIMIENTO=1 para ejecutarla (QT2)")
class TestRendimiento(unittest.TestCase):

    def test_TEST_081_consultas_con_5000_ejemplares_y_20000_prestamos(self):
        """TEST-081 (RNF-006): cada consulta tarda menos de 1 s; carga y guardado se miden y registran."""
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "biblioteca.json"
            RepositorioJSON(ruta).guardar(*generar_datos())
            tamano_mb = ruta.stat().st_size / 1_000_000

            biblioteca, t_carga = medir(lambda: Biblioteca(RepositorioJSON(ruta), reloj=lambda: HOY))
            consultas = {
                "listar_catalogo": biblioteca.listar_catalogo,
                "listar_disponibles": biblioteca.listar_disponibles,
                "listar_prestados": biblioteca.listar_prestados,
                "listar_vencidos": biblioteca.listar_vencidos,
                "consultar_ejemplar": lambda: biblioteca.consultar_ejemplar("E-02500"),
            }
            resultados, tiempos = {}, {}
            for nombre, consulta in consultas.items():
                resultados[nombre], tiempos[nombre] = medir(consulta)
            _, t_guardado = medir(lambda: biblioteca.registrar_prestamo(
                "E-04000", "2026999", "Estudiante de prueba", HOY + timedelta(days=7)))

        # Los datos generados son los previstos, así que las mediciones son válidas.
        self.assertEqual(len(resultados["listar_catalogo"]), EJEMPLARES)
        self.assertEqual(len(resultados["listar_prestados"]), ACTIVOS)
        self.assertEqual(len(resultados["listar_disponibles"]), EJEMPLARES - ACTIVOS)
        self.assertEqual(len(resultados["listar_vencidos"][1]), VENCIDOS)

        print(f"\n  Archivo: {tamano_mb:.2f} MB")
        print(f"  Carga inicial: {t_carga:.3f} s (se registra, sin límite)")
        for nombre, segundos in tiempos.items():
            print(f"  {nombre}: {segundos:.4f} s (límite {LIMITE_CONSULTA_S} s)")
        print(f"  registrar_prestamo con guardado: {t_guardado:.3f} s (se registra, sin límite)")

        for nombre, segundos in tiempos.items():
            with self.subTest(consulta=nombre):
                self.assertLess(segundos, LIMITE_CONSULTA_S)


if __name__ == "__main__":
    unittest.main()
