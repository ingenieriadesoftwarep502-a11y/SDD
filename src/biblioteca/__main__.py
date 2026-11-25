"""Punto de entrada: `python -m biblioteca [RUTA]` (CU-006, DEC-012).

Arma el repositorio, el servicio y la consola, carga los datos y muestra el menú.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from biblioteca.consola import Consola, mensaje_error
from biblioteca.errores import DatosCorruptos
from biblioteca.repositorio import RepositorioJSON
from biblioteca.servicio import Biblioteca

RUTA_POR_DEFECTO = Path("datos") / "biblioteca.json"  # relativa a la carpeta de ejecución (DEC-012)


def main(argv=None, entrada=input, salida=print, reloj=date.today) -> int:
    """Ejecuta la aplicación y devuelve el código de salida.

    0: cierre normal (Salir, Ctrl+C o fin de la entrada).
    1: el archivo de datos está dañado o no se puede leer; no se modifica (QP1).
    2: argumentos no válidos.
    `entrada`, `salida` y `reloj` se reemplazan en las pruebas (DEC-009, DEC-010).
    """
    argumentos = sys.argv[1:] if argv is None else list(argv)
    if len(argumentos) > 1:
        salida("Uso: python -m biblioteca [RUTA]")
        return 2
    ruta = Path(argumentos[0]) if argumentos else RUTA_POR_DEFECTO

    try:
        biblioteca = Biblioteca(RepositorioJSON(ruta), reloj=reloj)
    except DatosCorruptos as error:  # CU-006 2b
        salida(mensaje_error(error))
        salida(f"Archivo: {ruta}. No se modificó; revíselo antes de volver a iniciar.")
        return 1
    except OSError as error:  # p. ej., sin permiso de lectura (decisión del equipo, TASK-015)
        salida(f"No se pudo leer el archivo de datos {ruta}: {error}")
        return 1

    try:
        Consola(biblioteca, entrada=entrada, salida=salida).ejecutar()
    except (KeyboardInterrupt, EOFError):  # RNF-004: cierre ordenado; los datos ya están guardados (QP5)
        salida("")
        salida("Aplicación cerrada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
