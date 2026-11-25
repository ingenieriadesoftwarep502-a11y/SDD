"""Capa de presentación: menú de consola y entrada de datos (diseño §3, DEC-010, DEC-011).

Pide y valida el formato de los datos, gestiona "cancelar" y traduce las
excepciones a mensajes en español. No decide reglas de negocio: eso lo hace
`Biblioteca`.
"""
from __future__ import annotations

from datetime import date, datetime

from biblioteca.errores import (
    CampoVacio,
    DatosCorruptos,
    EjemplarDuplicado,
    EjemplarNoDisponible,
    EjemplarNoEncontrado,
    EjemplarNoPrestado,
    ErrorBiblioteca,
    ErrorPersistencia,
    FechaPrevistaInvalida,
)

PALABRA_CANCELAR = "cancelar"
FORMATO_FECHA = "%d/%m/%Y"  # DD/MM/AAAA (RNF-009)
AVISO_CANCELAR = "Escriba cancelar en cualquier momento para volver al menú."  # DEC-011

# Nombres de los campos tal como se muestran al bibliotecario.
_NOMBRES_DE_CAMPO = {
    "identificador": "identificador",
    "titulo": "título",
    "autor": "autor",
    "codigo": "código del estudiante",
    "nombre": "nombre del estudiante",
}


class _Cancelado(Exception):
    """El bibliotecario escribió "cancelar" mientras se le pedía un dato (RC-1)."""


def formatear_fecha(fecha: date) -> str:
    """Fecha en el formato de pantalla DD/MM/AAAA (RNF-009, DEC-007)."""
    return fecha.strftime(FORMATO_FECHA)


def mensaje_error(error: Exception) -> str:
    """Mensaje en español para cada excepción del diseño §6 (RNF-003, RNF-008)."""
    if isinstance(error, CampoVacio):
        campo = _NOMBRES_DE_CAMPO.get(error.campo, error.campo)
        return f"El campo «{campo}» es obligatorio."
    if isinstance(error, EjemplarDuplicado):
        return f"Ya existe un ejemplar con el identificador {error.identificador}."
    if isinstance(error, EjemplarNoEncontrado):
        return f"El ejemplar {error.identificador} no está registrado."
    if isinstance(error, EjemplarNoDisponible):
        return f"El ejemplar {error.identificador} ya está prestado."
    if isinstance(error, EjemplarNoPrestado):
        return f"El ejemplar {error.identificador} no tiene préstamo activo."
    if isinstance(error, FechaPrevistaInvalida):
        return (f"La fecha prevista ({formatear_fecha(error.fecha_prevista)}) no puede ser "
                f"anterior a la fecha del préstamo ({formatear_fecha(error.fecha_prestamo)}).")
    if isinstance(error, ErrorPersistencia):
        return f"No se pudo guardar la operación; los datos no cambiaron. Detalle: {error.detalle}"
    if isinstance(error, DatosCorruptos):
        return f"El archivo de datos está dañado y no se puede usar. Detalle: {error.detalle}"
    raise TypeError(f"Excepción sin mensaje definido: {type(error).__name__}")


class Consola:
    """Interfaz de consola del bibliotecario."""

    def __init__(self, biblioteca, entrada=input, salida=print):
        """`entrada` y `salida` se reemplazan en las pruebas (DEC-010)."""
        self._biblioteca = biblioteca
        self._entrada = entrada
        self._salida = salida
        # Opciones del menú principal (especificación §2). "6" es Salir.
        self._opciones = {
            "1": ("Registrar ejemplar", self._registrar_ejemplar),
            "2": ("Consultar ejemplares", self._consultar_ejemplares),
            "3": ("Registrar préstamo", self._no_disponible),
            "4": ("Registrar devolución", self._no_disponible),
            "5": ("Préstamos vencidos", self._no_disponible),
        }

    def ejecutar(self) -> None:
        """Muestra el menú principal hasta que el bibliotecario elige Salir."""
        while True:
            self._mostrar_menu()
            opcion = self._entrada("Elija una opción: ").strip()
            if opcion == "6":
                return
            if opcion in self._opciones:
                _, operacion = self._opciones[opcion]
                self.ejecutar_operacion(operacion)
            else:
                self._salida("Opción no válida. Escriba un número del 1 al 6.")

    def ejecutar_operacion(self, operacion) -> None:
        """Ejecuta una operación y vuelve al menú si se cancela o si falla (RC-1, RC-3)."""
        try:
            operacion()
        except _Cancelado:
            self._salida("Operación cancelada.")
        except (ErrorBiblioteca, ErrorPersistencia) as error:
            self._salida(mensaje_error(error))

    def pedir_texto(self, etiqueta: str) -> str:
        """Pide un texto obligatorio; lo vuelve a pedir mientras esté vacío (RC-2)."""
        while True:
            valor = self._pedir(etiqueta).strip()
            if valor:
                return valor
            self._salida(f"El dato «{etiqueta}» es obligatorio.")

    def pedir_fecha(self, etiqueta: str) -> date:
        """Pide una fecha DD/MM/AAAA existente; la vuelve a pedir si no es válida (RNF-009)."""
        while True:
            texto = self._pedir(f"{etiqueta} (DD/MM/AAAA)").strip()
            try:
                return datetime.strptime(texto, FORMATO_FECHA).date()
            except ValueError:
                self._salida(f"Fecha no válida: «{texto}». Use el formato DD/MM/AAAA, por ejemplo 24/11/2026.")

    def _pedir(self, etiqueta: str) -> str:
        """Lee un dato; si es "cancelar" (sin distinguir mayúsculas), interrumpe la operación."""
        valor = self._entrada(f"{etiqueta}: ")
        if valor.strip().lower() == PALABRA_CANCELAR:
            raise _Cancelado()
        return valor

    def _mostrar_menu(self) -> None:
        self._salida("")
        self._salida("=== Gestor de préstamos de libros ===")
        for numero, (titulo, _) in self._opciones.items():
            self._salida(f"{numero}. {titulo}")
        self._salida("6. Salir")

    def _registrar_ejemplar(self) -> None:
        """CU-001: identificador → título → autor; registra y confirma."""
        self._salida(AVISO_CANCELAR)
        while True:
            identificador = self.pedir_texto("Identificador")
            try:
                self._biblioteca.consultar_ejemplar(identificador)
            except EjemplarNoEncontrado:
                break
            self._salida(f"Identificador ya registrado: {identificador}.")  # CU-001 4b
        titulo = self.pedir_texto("Título")
        autor = self.pedir_texto("Autor")
        ejemplar = self._biblioteca.registrar_ejemplar(identificador, titulo, autor)
        self._salida(f"Ejemplar {ejemplar.identificador} registrado: «{ejemplar.titulo}», "
                     f"de {ejemplar.autor}.")

    def _consultar_ejemplares(self) -> None:
        """CU-002: submenú con cuatro consultas; muestra el resultado y vuelve al menú."""
        consultas = {
            "1": ("Catálogo completo", self._mostrar_catalogo),
            "2": ("Por identificador", self._mostrar_ejemplar),
            "3": ("Disponibles", self._mostrar_disponibles),
            "4": ("Prestados", self._mostrar_prestados),
        }
        self._salida(AVISO_CANCELAR)
        for numero, (titulo, _) in consultas.items():
            self._salida(f"{numero}. {titulo}")
        while True:
            opcion = self._pedir("Elija una consulta").strip()
            if opcion in consultas:
                break
            self._salida("Consulta no válida. Escriba un número del 1 al 4.")
        _, mostrar = consultas[opcion]
        mostrar()

    def _mostrar_catalogo(self) -> None:
        """HU-002: identificador, título, autor y estado de cada ejemplar."""
        catalogo = self._biblioteca.listar_catalogo()
        if not catalogo:
            self._salida("No hay ejemplares registrados.")
        for ejemplar, prestamo in catalogo:
            estado = "disponible" if prestamo is None else "prestado"
            self._salida(f"{ejemplar.identificador} | {ejemplar.titulo} | {ejemplar.autor} | {estado}")

    def _mostrar_ejemplar(self) -> None:
        """HU-003: un ejemplar; si está prestado, también estudiante y fecha prevista."""
        identificador = self.pedir_texto("Identificador")
        ejemplar, prestamo = self._biblioteca.consultar_ejemplar(identificador)
        if prestamo is None:
            estado = "disponible"
        else:
            estado = (f"prestado a {prestamo.codigo_estudiante} {prestamo.nombre_estudiante}, "
                      f"devolución prevista: {formatear_fecha(prestamo.fecha_prevista)}")
        self._salida(f"{ejemplar.identificador} | {ejemplar.titulo} | {ejemplar.autor} | {estado}")

    def _mostrar_disponibles(self) -> None:
        """HU-006: identificador, título y autor de los ejemplares disponibles."""
        disponibles = self._biblioteca.listar_disponibles()
        if not disponibles:
            self._salida("No hay ejemplares disponibles.")
        for ejemplar in disponibles:
            self._salida(f"{ejemplar.identificador} | {ejemplar.titulo} | {ejemplar.autor}")

    def _mostrar_prestados(self) -> None:
        """HU-007: identificador, título, estudiante, fecha de préstamo y fecha prevista."""
        prestados = self._biblioteca.listar_prestados()
        if not prestados:
            self._salida("No hay ejemplares prestados.")
        for ejemplar, prestamo in prestados:
            self._salida(
                f"{ejemplar.identificador} | {ejemplar.titulo} | "
                f"{prestamo.codigo_estudiante} {prestamo.nombre_estudiante} | "
                f"prestado el {formatear_fecha(prestamo.fecha_prestamo)} | "
                f"devolución prevista: {formatear_fecha(prestamo.fecha_prevista)}")

    def _no_disponible(self) -> None:
        self._salida("Opción no disponible todavía.")
