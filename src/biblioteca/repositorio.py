"""Persistencia en un archivo JSON local (diseño técnico §3.2 y §4.3).

Guarda y carga el estado completo: ejemplares y préstamos (activos y devueltos).
No aplica reglas de negocio.
"""
from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

from biblioteca.errores import ErrorPersistencia
from biblioteca.modelo import Ejemplar, Prestamo

VERSION_FORMATO = 1


class RepositorioJSON:
    """Lee y escribe el archivo de datos de la biblioteca."""

    def __init__(self, ruta: Path):
        self.ruta = Path(ruta)

    def cargar(self) -> tuple[list[Ejemplar], list[Prestamo]]:
        """Devuelve los ejemplares y préstamos guardados.

        Si el archivo no existe (primer uso), devuelve listas vacías y no crea
        nada (CU-006 2a).
        """
        if not self.ruta.exists():
            return [], []

        with open(self.ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)

        ejemplares = [_ejemplar_desde_dict(e) for e in datos["ejemplares"]]
        prestamos = [_prestamo_desde_dict(p) for p in datos["prestamos"]]
        return ejemplares, prestamos

    def guardar(self, ejemplares, prestamos) -> None:
        """Guarda el estado completo con escritura atómica (DEC-005).

        Escribe un archivo `.tmp`, lo vuelca a disco y lo pone en lugar del
        archivo real con `os.replace`. Si algo falla, el archivo anterior queda
        intacto, se borra el `.tmp` y se lanza `ErrorPersistencia`.
        """
        contenido = {
            "version": VERSION_FORMATO,
            "ejemplares": [_ejemplar_a_dict(e) for e in ejemplares],
            "prestamos": [_prestamo_a_dict(p) for p in prestamos],
        }
        temporal = self.ruta.with_name(self.ruta.name + ".tmp")

        try:
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(temporal, "w", encoding="utf-8") as archivo:
                json.dump(contenido, archivo, ensure_ascii=False, indent=2)
                archivo.flush()
                os.fsync(archivo.fileno())
            os.replace(temporal, self.ruta)
        except OSError as error:
            _borrar_sin_fallar(temporal)
            raise ErrorPersistencia(
                f"No se pudo guardar el archivo {self.ruta}: {error}"
            ) from error


def _ejemplar_a_dict(ejemplar: Ejemplar) -> dict:
    return {
        "identificador": ejemplar.identificador,
        "titulo": ejemplar.titulo,
        "autor": ejemplar.autor,
    }


def _ejemplar_desde_dict(datos: dict) -> Ejemplar:
    return Ejemplar(
        identificador=datos["identificador"],
        titulo=datos["titulo"],
        autor=datos["autor"],
    )


def _prestamo_a_dict(prestamo: Prestamo) -> dict:
    return {
        "identificador_ejemplar": prestamo.identificador_ejemplar,
        "codigo_estudiante": prestamo.codigo_estudiante,
        "nombre_estudiante": prestamo.nombre_estudiante,
        "fecha_prestamo": prestamo.fecha_prestamo.isoformat(),
        "fecha_prevista": prestamo.fecha_prevista.isoformat(),
        "fecha_devolucion": _fecha_a_texto(prestamo.fecha_devolucion),
    }


def _prestamo_desde_dict(datos: dict) -> Prestamo:
    return Prestamo(
        identificador_ejemplar=datos["identificador_ejemplar"],
        codigo_estudiante=datos["codigo_estudiante"],
        nombre_estudiante=datos["nombre_estudiante"],
        fecha_prestamo=date.fromisoformat(datos["fecha_prestamo"]),
        fecha_prevista=date.fromisoformat(datos["fecha_prevista"]),
        fecha_devolucion=_texto_a_fecha(datos["fecha_devolucion"]),
    )


def _fecha_a_texto(fecha: date | None) -> str | None:
    return None if fecha is None else fecha.isoformat()


def _texto_a_fecha(texto: str | None) -> date | None:
    return None if texto is None else date.fromisoformat(texto)


def _borrar_sin_fallar(ruta: Path) -> None:
    """Intenta borrar `ruta`; si no puede, no interrumpe el manejo del error original."""
    try:
        ruta.unlink(missing_ok=True)
    except OSError:
        pass
