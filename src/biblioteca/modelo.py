"""Entidades del dominio (diseño técnico §4.1).

Solo contienen datos y cálculos derivados de esos datos. Las reglas de negocio
(validaciones, unicidad, disponibilidad) se aplican en `servicio.py`.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class Ejemplar:
    """Copia física de un libro (RES-002).

    No almacena su estado: un ejemplar está prestado si tiene un préstamo
    activo y disponible en otro caso (RN-009, DEC-003).
    """

    identificador: str
    titulo: str
    autor: str


@dataclass
class Prestamo:
    """Préstamo de un ejemplar a un estudiante (RES-003).

    Se conserva después de la devolución como historial (RN-008).
    """

    identificador_ejemplar: str
    codigo_estudiante: str
    nombre_estudiante: str
    fecha_prestamo: date
    fecha_prevista: date
    fecha_devolucion: date | None = None

    @property
    def activo(self) -> bool:
        """Un préstamo está activo mientras no tenga fecha de devolución."""
        return self.fecha_devolucion is None

    def dias_atraso(self, hoy: date) -> int:
        """Días de atraso a la fecha `hoy` (RN-006).

        Devuelve 0 si el préstamo no está vencido: si ya fue devuelto o si
        `hoy` no es posterior a la fecha prevista.
        """
        if not self.activo or hoy <= self.fecha_prevista:
            return 0
        return (hoy - self.fecha_prevista).days
