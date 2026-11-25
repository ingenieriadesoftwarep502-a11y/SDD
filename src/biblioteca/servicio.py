"""Capa de negocio: operaciones de la biblioteca y reglas RN-001…RN-012 (diseño §3.1).

No lee el teclado, no imprime y no conoce el formato del archivo de datos.
"""
from __future__ import annotations

from datetime import date

from biblioteca.errores import CampoVacio, EjemplarDuplicado
from biblioteca.modelo import Ejemplar


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

    def _guardar(self) -> None:
        self._repositorio.guardar(list(self.ejemplares.values()), self.prestamos)


def _obligatorio(campo: str, valor: str) -> str:
    """Devuelve `valor` sin espacios al inicio y al final; si queda vacío, lanza CampoVacio."""
    limpio = valor.strip()
    if not limpio:
        raise CampoVacio(campo)
    return limpio
