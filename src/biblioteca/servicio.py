"""Capa de negocio: operaciones de la biblioteca y reglas RN-001…RN-012 (diseño §3.1).

No lee el teclado, no imprime y no conoce el formato del archivo de datos.
"""
from __future__ import annotations

from datetime import date

from biblioteca.errores import (
    CampoVacio,
    EjemplarDuplicado,
    EjemplarNoDisponible,
    EjemplarNoEncontrado,
    EjemplarNoPrestado,
    FechaPrevistaInvalida,
)
from biblioteca.modelo import Ejemplar, Prestamo


class Biblioteca:
    """Catálogo de ejemplares y préstamos del bibliotecario."""

    def __init__(self, repositorio, reloj=date.today):
        """Carga los datos guardados y construye los índices en memoria (DEC-006).

        `reloj` devuelve la fecha actual; las pruebas lo reemplazan por una
        fecha fija (DEC-009).
        """
        self._repositorio = repositorio
        self._reloj = reloj

        ejemplares, prestamos = repositorio.cargar()
        self.ejemplares: dict[str, Ejemplar] = {e.identificador: e for e in ejemplares}
        self.prestamos = list(prestamos)
        self.activos = {p.identificador_ejemplar: p for p in self.prestamos if p.activo}

    def registrar_ejemplar(self, identificador: str, titulo: str, autor: str) -> Ejemplar:
        """Registra un ejemplar nuevo, disponible (HU-001).

        Quita los espacios al inicio y al final de cada campo, exige que no
        queden vacíos (RN-010) y que el identificador no exista (RN-001).
        Si no se puede guardar, deshace el registro (RNF-005).
        """
        identificador = _obligatorio("identificador", identificador)
        titulo = _obligatorio("titulo", titulo)
        autor = _obligatorio("autor", autor)
        if identificador in self.ejemplares:
            raise EjemplarDuplicado(identificador)

        ejemplar = Ejemplar(identificador, titulo, autor)
        self.ejemplares[identificador] = ejemplar
        try:
            self._guardar()
        except BaseException:
            del self.ejemplares[identificador]
            raise
        return ejemplar

    def registrar_prestamo(self, identificador: str, codigo: str, nombre: str,
                           fecha_prevista: date) -> Prestamo:
        """Presta un ejemplar disponible a un estudiante (HU-004).

        Valida en el orden de CU-003: ejemplar (existe y está disponible,
        RN-002, RN-003), código, nombre y fecha prevista (RN-005). La fecha
        de préstamo es la fecha actual (RN-004). No hay límite de préstamos
        por estudiante (RN-011). Si no se puede guardar, deshace el préstamo.
        """
        identificador = _obligatorio("identificador", identificador)
        if identificador not in self.ejemplares:
            raise EjemplarNoEncontrado(identificador)
        if identificador in self.activos:
            raise EjemplarNoDisponible(identificador)
        codigo = _obligatorio("codigo", codigo)
        nombre = _obligatorio("nombre", nombre)
        hoy = self._reloj()
        if fecha_prevista < hoy:
            raise FechaPrevistaInvalida(fecha_prevista, hoy)

        prestamo = Prestamo(identificador, codigo, nombre, hoy, fecha_prevista)
        self.prestamos.append(prestamo)
        self.activos[identificador] = prestamo
        try:
            self._guardar()
        except BaseException:
            self.prestamos.pop()
            del self.activos[identificador]
            raise
        return prestamo

    def registrar_devolucion(self, identificador: str) -> Prestamo:
        """Cierra el préstamo activo de un ejemplar (HU-005).

        Valida en el orden de CU-004: el ejemplar existe y tiene un préstamo
        activo (RN-007). La fecha de devolución es la fecha actual. El préstamo
        se conserva como historial (RN-008). Si no se puede guardar, deshace
        la devolución.
        """
        identificador = _obligatorio("identificador", identificador)
        if identificador not in self.ejemplares:
            raise EjemplarNoEncontrado(identificador)
        if identificador not in self.activos:
            raise EjemplarNoPrestado(identificador)

        prestamo = self.activos.pop(identificador)
        prestamo.fecha_devolucion = self._reloj()
        try:
            self._guardar()
        except BaseException:
            prestamo.fecha_devolucion = None
            self.activos[identificador] = prestamo
            raise
        return prestamo

    def listar_catalogo(self) -> list[tuple[Ejemplar, Prestamo | None]]:
        """Todos los ejemplares con su préstamo activo, o None si están disponibles (HU-002, RN-009)."""
        return [(e, self.activos.get(e.identificador)) for e in self._ordenados()]

    def consultar_ejemplar(self, identificador: str) -> tuple[Ejemplar, Prestamo | None]:
        """Un ejemplar con su préstamo activo, o None si está disponible (HU-003)."""
        identificador = _obligatorio("identificador", identificador)
        if identificador not in self.ejemplares:
            raise EjemplarNoEncontrado(identificador)
        return self.ejemplares[identificador], self.activos.get(identificador)

    def listar_disponibles(self) -> list[Ejemplar]:
        """Ejemplares sin préstamo activo (HU-006)."""
        return [e for e in self._ordenados() if e.identificador not in self.activos]

    def listar_prestados(self) -> list[tuple[Ejemplar, Prestamo]]:
        """Ejemplares con préstamo activo, junto con ese préstamo (HU-007)."""
        return [(e, self.activos[e.identificador])
                for e in self._ordenados() if e.identificador in self.activos]

    def _ordenados(self) -> list[Ejemplar]:
        """Ejemplares ordenados por identificador, como texto (QP3)."""
        return [self.ejemplares[i] for i in sorted(self.ejemplares)]

    def _guardar(self) -> None:
        self._repositorio.guardar(list(self.ejemplares.values()), self.prestamos)


def _obligatorio(campo: str, valor: str) -> str:
    """Devuelve `valor` sin espacios al inicio y al final; si queda vacío, lanza CampoVacio."""
    limpio = valor.strip()
    if not limpio:
        raise CampoVacio(campo)
    return limpio
