# Diseño técnico — Gestor de préstamos de libros (v1)
Estado: APROBADO (2026-11-24) · Actividad 4 · Fecha: 2026-11-24
Fuentes: `docs/02_requisitos.md` y `docs/03_especificacion_producto.md` (APROBADOS)

> Las preguntas QD1–QD5 (sección 8) fueron respondidas por el equipo el 2026-11-24.

## 1. Visión general

Aplicación de consola en **Python** con tres capas. Solo usa la biblioteca estándar.

```
           ┌─────────────────────────────┐
 usuario → │ consola.py  (menú, entradas, │   Capa de presentación
           │ formato DD/MM/AAAA, mensajes)│   CU-001…CU-006, RNF-002/003/004/008/009
           └──────────────┬──────────────┘
                          │ llama operaciones / recibe resultados o excepciones
           ┌──────────────▼──────────────┐
           │ servicio.py (Biblioteca)     │   Capa de negocio
           │ reglas RN-001…RN-012          │   (no lee teclado ni archivos)
           └──────┬───────────────┬──────┘
                  │ usa           │ usa
       ┌──────────▼───┐   ┌───────▼────────────┐
       │ modelo.py    │   │ repositorio.py      │  Capa de datos
       │ errores.py   │   │ (archivo JSON local)│  RNF-001, RNF-005, QP1, QP5
       └──────────────┘   └─────────────────────┘
```

**Por qué tres capas:** la lógica de negocio se puede probar sin consola ni archivos, y cada capa se implementa como una tarea pequeña (Actividad 5). Para el tamaño del proyecto no hace falta más.

## 2. Estructura de archivos

```
src/biblioteca/
  __init__.py
  __main__.py      # punto de entrada: python -m biblioteca
  modelo.py        # Ejemplar, Prestamo
  errores.py       # jerarquía de excepciones
  servicio.py      # Biblioteca: operaciones y reglas de negocio
  repositorio.py   # RepositorioJSON: cargar / guardar
  consola.py       # Consola: menú e interacción
tests/
  __init__.py      # agrega src/ a sys.path (DEC-008)
  test_*.py        # una prueba por TEST-xxx
datos/             # archivo de datos en tiempo de ejecución (no se versiona)
```

## 3. Componentes y responsabilidades

| Componente | Responsabilidad | No hace | Requisitos |
|------------|-----------------|---------|------------|
| `modelo.Ejemplar` | Datos de un ejemplar: `identificador`, `titulo`, `autor`. | No guarda su estado (DEC-003). | RES-002 |
| `modelo.Prestamo` | Datos de un préstamo: `identificador_ejemplar`, `codigo_estudiante`, `nombre_estudiante`, `fecha_prestamo`, `fecha_prevista`, `fecha_devolucion` (o `None`). Propiedad `activo` (sin fecha de devolución) y método `dias_atraso(hoy)`. | No valida reglas de negocio. | RES-003, RN-006, RN-008 |
| `servicio.Biblioteca` | Ejecuta las operaciones, aplica RN-001…RN-012, calcula estados y listados, y pide al repositorio que guarde después de cada operación que modifica datos. | No lee el teclado, no imprime, no conoce el formato del archivo. | HU-001…HU-008 |
| `repositorio.RepositorioJSON` | Carga y guarda el estado completo en un archivo JSON, con escritura atómica. Valida la estructura del archivo al cargar. | No aplica reglas de negocio. | RNF-001, RNF-005, QP1, QP5 |
| `consola.Consola` | Muestra el menú, pide y valida el formato de las entradas (texto vacío, fechas DD/MM/AAAA, opciones del menú), gestiona "cancelar", traduce las excepciones a mensajes y formatea los listados. | No decide reglas de negocio. | CU-001…CU-006, RC-1, RC-2, RNF-002/003/004/008/009 |
| `__main__` | Construye repositorio, servicio y consola; carga los datos y arranca el menú. Si los datos están dañados, muestra el error y termina con código 1. | — | CU-006 |

### 3.1 Interfaz del servicio

```python
class Biblioteca:
    def __init__(self, repositorio, reloj=date.today): ...
    def registrar_ejemplar(self, identificador, titulo, autor) -> Ejemplar          # HU-001
    def listar_catalogo(self) -> list[tuple[Ejemplar, Prestamo | None]]            # HU-002
    def consultar_ejemplar(self, identificador) -> tuple[Ejemplar, Prestamo | None] # HU-003
    def registrar_prestamo(self, identificador, codigo, nombre, fecha_prevista: date) -> Prestamo  # HU-004
    def registrar_devolucion(self, identificador) -> Prestamo                       # HU-005
    def listar_disponibles(self) -> list[Ejemplar]                                  # HU-006
    def listar_prestados(self) -> list[tuple[Ejemplar, Prestamo]]                   # HU-007
    def listar_vencidos(self) -> tuple[date, list[tuple[Ejemplar, Prestamo]]]       # HU-008 (devuelve la fecha usada)
```

El estado de un ejemplar se deduce de que tenga o no un préstamo activo: los listados devuelven el ejemplar junto con su préstamo activo, o `None` si no tiene.

### 3.2 Interfaz del repositorio

```python
class RepositorioJSON:
    def __init__(self, ruta: Path): ...
    def cargar(self) -> tuple[list[Ejemplar], list[Prestamo]]   # archivo inexistente → listas vacías (CU-006 2a)
    def guardar(self, ejemplares, prestamos) -> None             # escritura atómica (DEC-005)
```

## 4. Modelo de datos

### 4.1 Entidades

| Entidad | Campo | Tipo | Regla |
|---------|-------|------|-------|
| Ejemplar | identificador | `str` | Obligatorio, sin espacios al inicio ni al final, único y distingue mayúsculas (RN-001, Q4). |
| | titulo | `str` | Obligatorio (RN-010). |
| | autor | `str` | Obligatorio (RN-010). |
| Prestamo | identificador_ejemplar | `str` | Debe existir en el catálogo. |
| | codigo_estudiante | `str` | Obligatorio; no se valida contra un registro (RN-012). |
| | nombre_estudiante | `str` | Obligatorio. |
| | fecha_prestamo | `date` | La asigna el sistema: hoy (RN-004). |
| | fecha_prevista | `date` | Igual o posterior a `fecha_prestamo` (RN-005). |
| | fecha_devolucion | `date \| None` | `None` si el préstamo está activo; hoy al devolver (RN-007). |

**Relación:** un ejemplar tiene 0..N préstamos (historial, RN-008) y **como máximo uno activo** (RN-002).

### 4.2 Estructura en memoria (DEC-006)
- `ejemplares: dict[str, Ejemplar]`: búsqueda por identificador en tiempo constante. Se guarda en orden de inserción y se ordena al listar (QP3).
- `prestamos: list[Prestamo]`: todos los préstamos, en orden cronológico.
- `activos: dict[str, Prestamo]`: préstamo activo por identificador de ejemplar. Es un índice que se reconstruye al cargar y garantiza RN-002 y RN-009 en tiempo constante.

### 4.3 Formato del archivo (`datos/biblioteca.json`)

```json
{
  "version": 1,
  "ejemplares": [
    {"identificador": "E-01", "titulo": "Cálculo I", "autor": "Stewart"}
  ],
  "prestamos": [
    {"identificador_ejemplar": "E-01", "codigo_estudiante": "2024001",
     "nombre_estudiante": "Ana Pérez", "fecha_prestamo": "2026-11-24",
     "fecha_prevista": "2026-12-01", "fecha_devolucion": null}
  ]
}
```
Las fechas se guardan en ISO (AAAA-MM-DD) y se muestran en DD/MM/AAAA (DEC-007). El archivo se escribe en UTF-8 con `ensure_ascii=False`, para que los nombres con tildes sigan siendo legibles.

## 5. Reglas de validación

| Regla | Dónde se valida | Error si falla |
|-------|-----------------|----------------|
| Campo obligatorio no vacío tras `strip()` (RN-010) | Servicio (y la consola vuelve a pedir el dato) | `CampoVacio(campo)` |
| Identificador único (RN-001) | Servicio | `EjemplarDuplicado` |
| Ejemplar existe (HU-003/004/005) | Servicio | `EjemplarNoEncontrado` |
| Ejemplar disponible al prestar (RN-002, RN-003) | Servicio, con el índice `activos` | `EjemplarNoDisponible` |
| Ejemplar con préstamo activo al devolver (RN-007) | Servicio | `EjemplarNoPrestado` |
| Fecha con formato DD/MM/AAAA y existente (RNF-009) | Consola, con `datetime.strptime(texto, "%d/%m/%Y")` | La consola muestra el formato esperado y vuelve a pedir el dato |
| Fecha prevista ≥ hoy (RN-005) | Servicio | `FechaPrevistaInvalida` |
| Opción de menú válida (CU-006 3a) | Consola | La consola informa y vuelve a mostrar el menú |
| Estructura del archivo de datos (QP1) | Repositorio, al cargar | `DatosCorruptos(detalle)` |

**Validaciones del archivo al cargar:**
- JSON válido y `version == 1`.
- Cada registro tiene todos sus campos, con tipos correctos y fechas ISO válidas.
- No hay identificadores duplicados.
- Todo préstamo apunta a un ejemplar existente.
- Ningún ejemplar tiene más de un préstamo activo.

## 6. Manejo de errores

Las excepciones están en `errores.py`:

```
ErrorBiblioteca                 (base: errores de negocio que se informan al usuario)
├── CampoVacio(campo)
├── EjemplarDuplicado(identificador)
├── EjemplarNoEncontrado(identificador)
├── EjemplarNoDisponible(identificador)
├── EjemplarNoPrestado(identificador)
└── FechaPrevistaInvalida(fecha_prevista, fecha_prestamo)
ErrorPersistencia(detalle)      (fallo al escribir el archivo)
DatosCorruptos(detalle)         (archivo ilegible al iniciar)
```

| Situación | Comportamiento | Requisito |
|-----------|----------------|-----------|
| `ErrorBiblioteca` | La consola muestra un mensaje en español con la causa y vuelve a pedir el dato o vuelve al menú, según el CU. | RNF-003, RC-2 |
| `ErrorPersistencia` | El servicio **deshace el cambio en memoria** antes de propagar el error. La consola informa que no se guardó la operación. | RNF-005, RC-3 |
| `DatosCorruptos` | `__main__` muestra el detalle y la ruta del archivo y termina con código 1 **sin escribir el archivo**. | QP1, CU-006 2b |
| Entrada no válida (menú o fecha) | La consola la maneja sin excepciones de negocio. | RNF-004 |
| Ctrl+C / fin de entrada (`KeyboardInterrupt`, `EOFError`) | La consola termina de forma ordenada. Los datos ya están guardados (QP5). | RNF-004 |
| Cualquier otra excepción | No se captura en silencio: es un defecto y debe aparecer en las pruebas. | — |

**Secuencia de una operación que modifica datos** (registrar ejemplar, préstamo o devolución):
1. Validar todas las reglas. Si alguna falla, se lanza el error y no se modifica nada.
2. Aplicar el cambio en memoria.
3. `repositorio.guardar(...)`. Si falla, revertir el paso 2 y lanzar `ErrorPersistencia`.
4. Devolver el resultado.

## 7. Decisiones de diseño

| ID | Decisión | Alternativas consideradas | Justificación | Requisitos |
|----|----------|---------------------------|---------------|------------|
| DEC-001 | **Python ≥ 3.10**, solo biblioteca estándar. | Java | Decisión del equipo (PEND-001). Con la biblioteca estándar no hay que instalar nada y se cumplen AGENT.md §5 y RNF-007. 3.10 permite `X \| None` en las anotaciones (QD5). | RES-007, RNF-007 |
| DEC-002 | Arquitectura de tres capas: consola, servicio, repositorio. | Un solo módulo; arquitectura hexagonal completa | Permite probar las reglas sin consola ni archivos, sin sobrediseñar. | RNF-005, plan de pruebas |
| DEC-003 | El estado del ejemplar **no se almacena**: se deduce de que tenga un préstamo activo. | Guardar un campo `estado` | Evita que el estado y los préstamos se contradigan. | RN-009, RN-002 |
| DEC-004 | **Persistencia en un archivo JSON** local (QD2). | SQLite (`sqlite3` también está en la biblioteca estándar); CSV | Legible, sencillo de probar e inspeccionar. Con 5.000 ejemplares y 20.000 préstamos el archivo ocupa unos 4 MB y se guarda en milisegundos. SQLite daría transacciones nativas, pero agrega SQL y esquema que el proyecto no necesita. | RNF-001, RNF-006 |
| DEC-005 | **Escritura atómica:** se escribe `biblioteca.json.tmp`, se hace `flush` + `os.fsync` y luego `os.replace` sobre el archivo real. Se guarda después de cada operación. | Escribir directo sobre el archivo; guardar al salir | Si la aplicación se cierra a mitad de una escritura, queda el archivo anterior completo y nunca uno a medias. | RNF-005, QP5 |
| DEC-006 | Índices en memoria (`dict` por identificador y por préstamo activo). | Recorrer listas | Cumple RNF-006 holgadamente. | RNF-006 |
| DEC-007 | Fechas internas como `datetime.date` y en ISO en el archivo. Se muestran en DD/MM/AAAA. | Guardar en DD/MM/AAAA | ISO es inequívoco y se ordena como texto. El formato de pantalla se aísla en la consola. | RNF-009 |
| DEC-008 | **Pruebas con `unittest`** (QD1). Se ejecutan con `python -m unittest discover -s tests -v` desde la raíz; `tests/__init__.py` agrega `src/` al path. | `pytest` | No requiere instalar nada (AGENT.md §5). Las pruebas son simples y no necesitan funciones de pytest. | PEND-002 |
| DEC-009 | **Reloj inyectable:** el servicio recibe `reloj` (por defecto `date.today`). | Llamar a `date.today()` directamente | Las pruebas fijan la fecha (p. ej., 24/11/2026) y verifican RN-004, RN-005 y RN-006 de forma determinista. | RN-004, RN-006, HU-008.CA1 |
| DEC-010 | **E/S inyectable en la consola:** recibe las funciones `entrada` (por defecto `input`) y `salida` (por defecto `print`). | Usar `input`/`print` directamente | Permite pruebas de integración de los CU completos simulando lo que escribe el bibliotecario. | CU-001…CU-006 |
| DEC-011 | **Cancelar:** escribir `cancelar` (sin distinguir mayúsculas) en cualquier dato pedido vuelve al menú sin cambios. La consola lo indica **una sola vez al iniciar cada operación** (p. ej., "Escriba cancelar en cualquier momento para volver al menú"), no en cada pregunta (QD3). | B: símbolo `*` (poco intuitivo; habría que recordarlo en cada pregunta); C: línea vacía (contradice HU-001.CA3 y HU-004.CA6); D: Ctrl+C (poco conocido por el usuario y reservado para cerrar); E: preguntar tras un error (no cumple RC-1); tecla Esc (no se detecta con `input()`) | Es la opción más clara para un usuario sin formación técnica (RNF-002) y no modifica requisitos aprobados. Consecuencia: no se puede usar `cancelar` como identificador, código ni nombre. | RC-1, RNF-002 |
| DEC-012 | **Archivo de datos:** por defecto `datos/biblioteca.json`, relativo a la carpeta desde donde se ejecuta. Se puede indicar otra ruta como argumento: `python -m biblioteca RUTA` (QD4). | Ruta fija | Las pruebas usan carpetas temporales y nunca tocan los datos reales. `datos/` se agrega a `.gitignore`. | RNF-001 |

## 8. Preguntas de clarificación (resueltas)

| # | Pregunta | Propuesta de la IA | Afecta a | Decisión del equipo |
|---|----------|--------------------|----------|---------------------|
| QD1 | ¿Framework de pruebas? | `unittest` (no requiere instalar nada) | DEC-008, PEND-002 | Aceptada: `unittest`. |
| QD2 | ¿Persistencia en JSON o SQLite? | JSON con escritura atómica | DEC-004, DEC-005, PEND-003 | Aceptada: JSON. |
| QD3 | ¿Cómo cancela el bibliotecario una operación? | Escribiendo `cancelar` | DEC-011 | Aceptada: `cancelar`, indicado una vez por operación. Se evaluaron las alternativas B–E (ver DEC-011). |
| QD4 | ¿Dónde se guarda el archivo de datos? | `datos/biblioteca.json`, con la opción de pasar otra ruta como argumento | DEC-012 | Aceptada. |
| QD5 | ¿Versión mínima de Python? | 3.10 (en el equipo está instalada la 3.14) | DEC-001 | Aceptada: 3.10. |
