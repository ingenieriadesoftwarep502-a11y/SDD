"""Excepciones de la aplicación (diseño técnico §6).

Las subclases de `ErrorBiblioteca` son errores de negocio que la consola
informa al bibliotecario. `ErrorPersistencia` y `DatosCorruptos` son fallos
de almacenamiento y se tratan aparte.
"""
from __future__ import annotations

from datetime import date


class ErrorBiblioteca(Exception):
    """Base de los errores de negocio."""


class CampoVacio(ErrorBiblioteca):
    """Un dato obligatorio está vacío o solo tiene espacios (RN-010)."""

    def __init__(self, campo: str):
        super().__init__(f"El campo '{campo}' es obligatorio.")
        self.campo = campo


class EjemplarDuplicado(ErrorBiblioteca):
    """Ya existe un ejemplar con ese identificador (RN-001)."""

    def __init__(self, identificador: str):
        super().__init__(f"Ya existe un ejemplar con el identificador '{identificador}'.")
        self.identificador = identificador


class EjemplarNoEncontrado(ErrorBiblioteca):
    """No existe un ejemplar con ese identificador."""

    def __init__(self, identificador: str):
        super().__init__(f"No existe un ejemplar con el identificador '{identificador}'.")
        self.identificador = identificador


class EjemplarNoDisponible(ErrorBiblioteca):
    """El ejemplar ya tiene un préstamo activo (RN-002, RN-003)."""

    def __init__(self, identificador: str):
        super().__init__(f"El ejemplar '{identificador}' ya está prestado.")
        self.identificador = identificador


class EjemplarNoPrestado(ErrorBiblioteca):
    """El ejemplar no tiene un préstamo activo que devolver (RN-007)."""

    def __init__(self, identificador: str):
        super().__init__(f"El ejemplar '{identificador}' no tiene un préstamo activo.")
        self.identificador = identificador


class FechaPrevistaInvalida(ErrorBiblioteca):
    """La fecha prevista es anterior a la fecha del préstamo (RN-005)."""

    def __init__(self, fecha_prevista: date, fecha_prestamo: date):
        super().__init__(
            f"La fecha prevista ({fecha_prevista}) no puede ser anterior "
            f"a la fecha del préstamo ({fecha_prestamo})."
        )
        self.fecha_prevista = fecha_prevista
        self.fecha_prestamo = fecha_prestamo


class ErrorPersistencia(Exception):
    """No se pudo guardar el archivo de datos (RNF-005)."""

    def __init__(self, detalle: str):
        super().__init__(detalle)
        self.detalle = detalle


class DatosCorruptos(Exception):
    """El archivo de datos no se puede leer o es inconsistente (QP1)."""

    def __init__(self, detalle: str):
        super().__init__(detalle)
        self.detalle = detalle
