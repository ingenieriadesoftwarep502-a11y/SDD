"""Persistencia en un archivo JSON local (diseño técnico §3.2 y §4.3).

Guarda y carga el estado completo: ejemplares y préstamos (activos y devueltos).
No aplica reglas de negocio.
"""
from __future__ import annotations

import json
import os
import re
from datetime import date
from pathlib import Path

from biblioteca.errores import DatosCorruptos, ErrorPersistencia
from biblioteca.modelo import Ejemplar, Prestamo

VERSION_FORMATO = 1

# Formato de fecha del archivo: AAAA-MM-DD (diseño §4.3). Se exige de forma
# estricta porque date.fromisoformat acepta otros formatos desde Python 3.11.
_PATRON_FECHA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


class RepositorioJSON:
    """Lee y escribe el archivo de datos de la biblioteca."""

    def __init__(self, ruta: Path):
        self.ruta = Path(ruta)

    def cargar(self) -> tuple[list[Ejemplar], list[Prestamo]]:
        """Devuelve los ejemplares y préstamos guardados.

        Si el archivo no existe (primer uso), devuelve listas vacías y no crea
        nada (CU-006 2a). Si el contenido está dañado, lanza `DatosCorruptos`
        sin modificar el archivo (QP1, diseño §5). Los errores del sistema al
        leer (p. ej., permisos) se propagan como `OSError`.
        """
        if not self.ruta.exists():
            return [], []

        contenido = self.ruta.read_bytes()
        try:
            datos = json.loads(contenido.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise DatosCorruptos(f"El archivo no es un JSON UTF-8 válido: {error}") from error

        return _validar_y_convertir(datos)

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


def _validar_y_convertir(datos) -> tuple[list[Ejemplar], list[Prestamo]]:
    """Aplica las validaciones del diseño §5 y convierte el contenido en entidades."""
    _exigir(isinstance(datos, dict), "el contenido no es un objeto JSON")
    version = datos.get("version")
    _exigir(type(version) is int and version == VERSION_FORMATO,
            f"versión de formato no soportada: {version!r} (se esperaba {VERSION_FORMATO})")

    ejemplares = [
        _ejemplar_desde_dict(registro, f"ejemplares[{i}]")
        for i, registro in enumerate(_lista(datos, "ejemplares"))
    ]
    prestamos = [
        _prestamo_desde_dict(registro, f"prestamos[{i}]")
        for i, registro in enumerate(_lista(datos, "prestamos"))
    ]

    identificadores = set()
    for ejemplar in ejemplares:
        _exigir(ejemplar.identificador not in identificadores,
                f"identificador de ejemplar duplicado: '{ejemplar.identificador}'")
        identificadores.add(ejemplar.identificador)

    con_prestamo_activo = set()
    for prestamo in prestamos:
        _exigir(prestamo.identificador_ejemplar in identificadores,
                f"préstamo de un ejemplar inexistente: '{prestamo.identificador_ejemplar}'")
        if prestamo.activo:
            _exigir(prestamo.identificador_ejemplar not in con_prestamo_activo,
                    f"el ejemplar '{prestamo.identificador_ejemplar}' tiene más de un préstamo activo")
            con_prestamo_activo.add(prestamo.identificador_ejemplar)

    return ejemplares, prestamos


def _exigir(condicion: bool, detalle: str) -> None:
    if not condicion:
        raise DatosCorruptos(detalle)


def _lista(datos: dict, clave: str) -> list:
    valor = datos.get(clave)
    _exigir(isinstance(valor, list), f"falta la lista '{clave}' o no es una lista")
    return valor


def _texto(registro: dict, campo: str, ubicacion: str) -> str:
    _exigir(campo in registro, f"{ubicacion}: falta el campo '{campo}'")
    valor = registro[campo]
    _exigir(isinstance(valor, str), f"{ubicacion}: el campo '{campo}' debe ser texto")
    return valor


def _fecha(registro: dict, campo: str, ubicacion: str) -> date:
    texto = _texto(registro, campo, ubicacion)
    try:
        _exigir(_PATRON_FECHA.fullmatch(texto) is not None, "")
        return date.fromisoformat(texto)
    except (DatosCorruptos, ValueError):
        raise DatosCorruptos(
            f"{ubicacion}: el campo '{campo}' no es una fecha AAAA-MM-DD válida: '{texto}'"
        ) from None


def _ejemplar_desde_dict(registro, ubicacion: str) -> Ejemplar:
    _exigir(isinstance(registro, dict), f"{ubicacion}: no es un objeto")
    return Ejemplar(
        identificador=_texto(registro, "identificador", ubicacion),
        titulo=_texto(registro, "titulo", ubicacion),
        autor=_texto(registro, "autor", ubicacion),
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


def _prestamo_desde_dict(registro, ubicacion: str) -> Prestamo:
    _exigir(isinstance(registro, dict), f"{ubicacion}: no es un objeto")
    _exigir("fecha_devolucion" in registro, f"{ubicacion}: falta el campo 'fecha_devolucion'")
    devolucion = (
        None if registro["fecha_devolucion"] is None
        else _fecha(registro, "fecha_devolucion", ubicacion)
    )
    return Prestamo(
        identificador_ejemplar=_texto(registro, "identificador_ejemplar", ubicacion),
        codigo_estudiante=_texto(registro, "codigo_estudiante", ubicacion),
        nombre_estudiante=_texto(registro, "nombre_estudiante", ubicacion),
        fecha_prestamo=_fecha(registro, "fecha_prestamo", ubicacion),
        fecha_prevista=_fecha(registro, "fecha_prevista", ubicacion),
        fecha_devolucion=devolucion,
    )


def _fecha_a_texto(fecha: date | None) -> str | None:
    return None if fecha is None else fecha.isoformat()


def _borrar_sin_fallar(ruta: Path) -> None:
    """Intenta borrar `ruta`; si no puede, no interrumpe el manejo del error original."""
    try:
        ruta.unlink(missing_ok=True)
    except OSError:
        pass
