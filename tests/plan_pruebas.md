# Plan de pruebas — Gestor de préstamos de libros (v1)
Estado: APROBADO (2026-11-24) · Actividad 6 · Fecha: 2026-11-24
Fuentes: `docs/02_requisitos.md`, `docs/03_especificacion_producto.md`, `docs/04_diseno_tecnico.md`, `tasks/plan_tareas.md` (APROBADOS)

## 1. Estrategia

| Tipo | Qué verifica | Nivel | Herramienta |
|------|--------------|-------|-------------|
| **U** Unitaria | Una clase o función aislada (modelo, repositorio, ayudas de consola) | Componente | `unittest` |
| **A** Aceptación | Un criterio de aceptación de una HU (HU-xxx.CAn) | Servicio o consola con E/S simulada | `unittest` |
| **F** Fallo | Rechazo de una entrada u operación inválida, o falla de un recurso; incluye comprobar que **los datos no cambian** | Servicio, repositorio o consola | `unittest` (+ `unittest.mock` para simular fallas) |
| **I** Integración | Varias capas juntas con el archivo real en una carpeta temporal | Aplicación completa | `unittest` + `tempfile` |
| **M** Manual | Lo que no conviene automatizar (usabilidad, uso sin red) | Aplicación completa | Persona del equipo; evidencia en `tests/evidencias.md` |

**Convenciones**
- Cada prueba automatizada se nombra con su ID: `test_TEST_017_registro_valido` (AGENT.md §7).
- Las pruebas de servicio usan un **repositorio falso en memoria**, que cuenta las llamadas a `guardar()` y puede simular una falla. Las de repositorio e integración usan `tempfile.TemporaryDirectory()`. Ninguna prueba toca `datos/`.
- Las pruebas de consola verifican **palabras clave** del mensaje (por ejemplo "ya está prestado", "DD/MM/AAAA"), no el texto exacto (QPR1).
- Toda prueba de tipo F comprueba que el estado (ejemplares, préstamos y llamadas a `guardar`) es igual antes y después.
- Ejecución: `python -m unittest discover -s tests -v` desde la raíz. La prueba de rendimiento solo corre con `RENDIMIENTO=1`.

## 2. Datos de prueba comunes

| Nombre | Contenido |
|--------|-----------|
| **HOY** | Reloj fijo: 24/11/2026 |
| **D0** | Catálogo vacío, sin préstamos |
| **D1** | E-01 "Cálculo I" / Stewart · E-02 "Cálculo I" / Stewart · E-03 "Física" / Serway. Préstamo **P1** activo: E-02 a 2024001 "Ana Pérez", prestado 20/11/2026, previsto 30/11/2026 |
| **D2** | D1 + préstamo **P2** devuelto: E-01 a 2024002 "Luis Núñez", prestado 01/11/2026, previsto 10/11/2026, devuelto 15/11/2026 |

## 3. Casos de prueba

Estado inicial de todas las pruebas: **Pendiente**. El resultado de cada ejecución se registra en `tests/evidencias.md`.

### TASK-001 — Estructura
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-001 | U | DEC-008 | Repositorio con `src/biblioteca/` | `import biblioteca` | Importa sin error; el comando de pruebas encuentra la prueba |

### TASK-002 — Modelo y excepciones
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-002 | U | RN-009, DEC-003 | — | `Prestamo` sin fecha de devolución; luego con fecha | `activo` es `True`; luego `False` |
| TEST-003 | U | RN-006 | Préstamo previsto 24/11/2026 | `dias_atraso(hoy)` con 20/11, 24/11 y 25/11 | 0, 0 y 1 |
| TEST-004 | U | Diseño §6 | — | Crear cada excepción con su dato | Conserva el dato (p. ej., `.identificador == "E-01"`). Las de negocio heredan de `ErrorBiblioteca`; `ErrorPersistencia` y `DatosCorruptos` no |

### TASK-003 — Repositorio: cargar y guardar
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-005 | U | RNF-001, RN-008 | Carpeta temporal | Guardar D2 con un estudiante "Ñuñez Álvarez" y volver a cargar | Los datos cargados son iguales a los guardados, incluido el préstamo devuelto |
| TEST-006 | U | CU-006 2a | Carpeta temporal sin archivo | `cargar()` | Listas vacías; no se crea ningún archivo |
| TEST-007 | U | DEC-005, DEC-012 | Ruta con subcarpeta inexistente | `guardar(D1)` | Se crea la carpeta y el archivo; no queda ningún `.tmp` |
| TEST-008 | F | RNF-005, DEC-005 | Archivo con D1 | `guardar(D2)` con `os.replace` simulado que falla | Lanza `ErrorPersistencia`; el archivo contiene exactamente D1 |
| TEST-009 | U | DEC-007, §4.3 | Carpeta temporal | `guardar(D1)` y leer el texto del archivo | `"version": 1`; fechas `"2026-11-20"`; "Pérez" escrito con tilde (no `é`) |

### TASK-004 — Repositorio: datos dañados
Para todas: el archivo se prepara a mano, se ejecuta `cargar()`, se espera `DatosCorruptos` con un detalle no vacío y el archivo debe quedar **idéntico byte a byte**. Requisito: QP1, CU-006 2b.

| ID | Tipo | Contenido del archivo |
|----|------|-----------------------|
| TEST-010 | F | Texto que no es JSON (`{ejemplares: [`) |
| TEST-011 | F | `"version": 2` |
| TEST-012 | F | Ejemplar sin `autor`; y otro caso con `titulo` numérico |
| TEST-013 | F | Fecha prevista `"24/11/2026"` (no ISO) |
| TEST-014 | F | Dos ejemplares con identificador "E-01" |
| TEST-015 | F | Préstamo de "E-99", que no existe en el catálogo |
| TEST-016 | F | Dos préstamos activos de "E-02" |

### TASK-005 — Servicio: inicio y registro de ejemplares
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-017 | A | HU-001.CA1 | D0 | Registrar ("E-01", "Cálculo I", "Stewart") | El ejemplar existe y está disponible; `guardar` se llamó 1 vez |
| TEST-018 | F | HU-001.CA2, RN-001 | D1 | Registrar ("E-01", "Otro", "Otro") | `EjemplarDuplicado`; catálogo sin cambios; `guardar` no se llamó |
| TEST-019 | U | RN-001 (Q4) | D0 | Registrar "e-01" y "E-01" | Ambos se registran: son distintos |
| TEST-020 | U | RN-001 | D0 | Registrar " E-04 " y luego "E-04" | El primero queda como "E-04"; el segundo da `EjemplarDuplicado` |
| TEST-021 | F | HU-001.CA3, RN-010 | D0 | Por cada campo (identificador, título, autor): "" y "   " | `CampoVacio` con el nombre del campo; catálogo vacío |
| TEST-022 | A | HU-001.CA4 | D0 | Registrar E-01 y E-02 con el mismo título y autor | Dos ejemplares independientes |
| TEST-023 | F | RNF-005, RC-3 | D0; el repositorio falso falla al guardar | Registrar "E-01" | `ErrorPersistencia`; "E-01" no existe en memoria |
| TEST-024 | U | DEC-006 | Repositorio falso con D1 | Crear `Biblioteca` y registrar "E-03" | `EjemplarDuplicado`: los datos se cargaron al iniciar |

### TASK-006 — Servicio: registrar préstamo (HOY = 24/11/2026)
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-025 | A | HU-004.CA1, RN-004 | D1 | Prestar E-01 a ("2024003", "Marta Ríos"), previsto 01/12/2026 | Préstamo activo con fecha de préstamo 24/11/2026; E-01 prestado; `guardar` 1 vez |
| TEST-026 | F | HU-004.CA2, RN-002, CE-3 | D1 (E-02 prestado a 2024001) | Prestar E-02 a "2024003"; luego al mismo "2024001" | `EjemplarNoDisponible` en ambos; la cantidad de préstamos no cambia |
| TEST-027 | F | HU-004.CA3 | D1 | Prestar "E-99" | `EjemplarNoEncontrado` |
| TEST-028 | F | HU-004.CA4, RN-005 | D1 | Prestar E-01, previsto 23/11/2026 | `FechaPrevistaInvalida`; sin préstamo nuevo |
| TEST-029 | A | HU-004.CA5, RN-005 | D1 | Prestar E-01, previsto 24/11/2026 | Se acepta (caso límite) |
| TEST-030 | F | RN-010 | D1 | Código "" y, aparte, nombre "  " | `CampoVacio` con el campo; sin préstamo |
| TEST-031 | A | HU-004.CA7, RN-011 | D1 | Prestar E-01 y E-03 a "2024001" (que ya tiene E-02) | Ambos se aceptan; el estudiante tiene 3 préstamos activos |
| TEST-032 | F | RNF-005 | D1; el repositorio falla al guardar | Prestar E-01 | `ErrorPersistencia`; E-01 sigue disponible; sin préstamo nuevo |

### TASK-007 — Servicio: registrar devolución (HOY = 24/11/2026)
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-033 | A | HU-005.CA1, CE-4 | D1 | Devolver E-02 | P1 con fecha de devolución 24/11/2026; E-02 disponible; `guardar` 1 vez |
| TEST-034 | F | HU-005.CA2, RN-007 | D1 | Devolver E-01 (disponible) | `EjemplarNoPrestado`; sin cambios |
| TEST-035 | F | HU-005.CA3 | D1 | Devolver "E-99" | `EjemplarNoEncontrado` |
| TEST-036 | A | HU-005.CA4 | D1 con P1 previsto el 20/11/2026 (vencido) | Devolver E-02 | Se acepta igual que una devolución a tiempo |
| TEST-037 | A | HU-005.CA5, RN-008 | D1 | Devolver E-02 | La lista de préstamos sigue teniendo P1 (cerrado); la cantidad total no cambia |
| TEST-038 | A | RN-002, RN-007 | D1 | Devolver E-02 y luego prestarlo a "2024003" | El nuevo préstamo se acepta |
| TEST-039 | F | RNF-005 | D1; el repositorio falla al guardar | Devolver E-02 | `ErrorPersistencia`; P1 sigue activo; E-02 prestado |

### TASK-008 — Servicio: consultas
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-040 | A | HU-002.CA1, QP3 | D1 | `listar_catalogo()` | 3 ejemplares en orden E-01, E-02, E-03; solo E-02 tiene préstamo (P1) |
| TEST-041 | A | HU-002.CA2, HU-006.CA2, HU-007.CA2 | D0 | Las tres consultas de listado | Listas vacías |
| TEST-042 | A | HU-003.CA1, HU-003.CA2, CE-1 | D1 | Consultar E-01 y E-02 | E-01 sin préstamo; E-02 con P1 (2024001, Ana Pérez, 30/11/2026) |
| TEST-043 | F | HU-003.CA3 | D1 | Consultar "E-99" | `EjemplarNoEncontrado` |
| TEST-044 | A | HU-006.CA1 | D1 | `listar_disponibles()` | E-01, E-03 |
| TEST-045 | A | HU-007.CA1 | D1 | `listar_prestados()` | Solo E-02, con P1 |
| TEST-046 | U | Diseño §3.1 | D1 | Ejecutar las 4 consultas | `guardar` no se llamó; el estado no cambia |

### TASK-009 — Servicio: vencidos (HOY = 24/11/2026)
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-047 | A | HU-008.CA1, RN-006, CE-2 | Préstamos activos con fecha prevista 20/11, 24/11 y 30/11 | `listar_vencidos()` | Solo el del 20/11 |
| TEST-048 | A | HU-008.CA2 | D2 (P2 devuelto con atraso) + P1 a tiempo | `listar_vencidos()` | Lista vacía |
| TEST-049 | A | HU-008.CA4 | D1 | `listar_vencidos()` | `(24/11/2026, [])` |
| TEST-050 | U | QP3 | Activos con fecha prevista 20/11, 10/11 y 15/11 | `listar_vencidos()` | Orden: 10/11, 15/11, 20/11 (de más a menos atraso) |

### TASK-010 — Consola: base (E/S simulada)
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-051 | F | CU-006 3a, RNF-004 | Menú principal | "9", "abc", "" y luego Salir | Un mensaje de opción inválida por cada entrada; el menú se muestra de nuevo; no hay excepción |
| TEST-052 | U | CU-006 | Menú principal | Opción Salir | El bucle termina |
| TEST-053 | U | RC-2, RN-010 | Pedir texto obligatorio | "", "  ", "Hola" | Dos avisos de campo obligatorio; devuelve "Hola" |
| TEST-054 | F | RNF-009, HU-004.CA6 | Pedir fecha | "31/02/2026", "2026-11-24", "hola", "24/11/2026" | Tres rechazos que muestran "DD/MM/AAAA"; devuelve `date(2026, 11, 24)` |
| TEST-055 | U | RC-1, DEC-011 | Pedir un dato dentro de una operación | "cancelar"; aparte, "CANCELAR" | Vuelve al menú sin ejecutar la operación |
| TEST-056 | U | RNF-003, RNF-008 | — | Cada excepción del diseño §6 | Mensaje en español que incluye el dato (p. ej., "E-01") |

### TASK-011 — Consola: CU-001
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-057 | A | CU-001, HU-001.CA1, DEC-011 | D0 | Opción registrar: "E-01", "Cálculo I", "Stewart" | Ejemplar registrado; mensaje de confirmación; el aviso de "cancelar" aparece una sola vez |
| TEST-058 | F | CU-001 4b, HU-001.CA2 | D1 | "E-01", luego "E-04", título, autor | Mensaje "ya registrado"; vuelve a pedir el identificador; registra E-04 |
| TEST-059 | F | CU-001 6a, HU-001.CA3 | D0 | "E-01", "", "Cálculo I", "Stewart" | Aviso de título obligatorio; registra al reintentar |
| TEST-060 | F | RC-1 | D0 | "E-01", "Cálculo I", "cancelar" | Vuelve al menú; el catálogo sigue vacío |

### TASK-012 — Consola: CU-002
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-061 | A | HU-002.CA1, CA2 | D1; luego D0 | Consulta de catálogo | Con D1: los 3 identificadores, títulos, autores y "disponible"/"prestado". Con D0: mensaje de catálogo vacío |
| TEST-062 | A | HU-003.CA1, CA2 | D1 | Consultar "E-01" y "E-02" | E-01 "disponible"; E-02 "prestado", "2024001", "Ana Pérez", "30/11/2026" |
| TEST-063 | F | HU-003.CA3 | D1 | Consultar "E-99" | Mensaje "no está registrado" |
| TEST-064 | A | HU-006.CA1–2, HU-007.CA1–2 | D1; luego D0 | Consultas de disponibles y prestados | D1: disponibles E-01 y E-03; prestados E-02 con estudiante y fechas DD/MM/AAAA. D0: mensajes de lista vacía |

### TASK-013 — Consola: CU-003 (HOY = 24/11/2026)
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-065 | A | CU-003, HU-004.CA1 | D1 | "E-01", "2024003", "Marta Ríos", "01/12/2026" | Muestra "Cálculo I" y "Stewart" después del identificador; préstamo creado; confirmación |
| TEST-066 | F | CU-003 4b, HU-004.CA2 | D1 | "E-02", luego "E-01", … | Mensaje "ya está prestado"; vuelve a pedir el identificador |
| TEST-067 | F | CU-003 11a, HU-004.CA6 | D1 | …, "31/02/2026", "01/12/2026" | Muestra "DD/MM/AAAA" y vuelve a pedir la fecha; préstamo creado |
| TEST-068 | F | CU-003 11b, HU-004.CA4 | D1 | …, "23/11/2026", "24/11/2026" | Mensaje de fecha anterior y vuelve a pedirla; préstamo creado |
| TEST-069 | F | RC-1 | D1 | "E-01", "2024003", "Marta Ríos", "cancelar" | Sin préstamo; E-01 disponible |
| TEST-070 | U | QP4 (rechazada) | D1 | Exactamente las 4 entradas de TEST-065, seguidas de Salir | El préstamo se crea sin pedir ninguna entrada adicional (no hay confirmación) |

### TASK-014 — Consola: CU-004 y CU-005 (HOY = 24/11/2026)
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-071 | A | CU-004, HU-005.CA1 | D1 | Devolver "E-02" | Confirmación; E-02 disponible |
| TEST-072 | F | CU-004 4b, HU-005.CA2 | D1 | Devolver "E-01" | Mensaje "no tiene préstamo activo" |
| TEST-073 | A | CU-005, HU-008.CA3 | P1 con fecha prevista 20/11/2026 | Opción vencidos | Muestra "24/11/2026" (fecha usada), "E-02", "Cálculo I", "2024001", "Ana Pérez", "20/11/2026" y "4" días |
| TEST-074 | A | HU-008.CA4 | D1 | Opción vencidos | Mensaje "no hay préstamos vencidos" y la fecha usada |

### TASK-015 — Integración e inicio/cierre
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-075 | I | RNF-001, CE-5 | Carpeta temporal vacía | Ejecución 1: registrar E-01, prestarlo y salir. Ejecución 2: consultar E-01 | En la ejecución 2, E-01 aparece prestado con los datos del estudiante |
| TEST-076 | I | QP1, CU-006 2b | Archivo con JSON inválido | Iniciar la aplicación con esa ruta | Código de salida 1; mensaje con la ruta; archivo idéntico |
| TEST-077 | I | RNF-004 | Carpeta temporal | Entrada que termina (EOF) en mitad del menú | Termina sin traza de error |
| TEST-078 | I | CU-006 2a | Carpeta temporal sin archivo | Iniciar, consultar el catálogo, salir | Mensaje de catálogo vacío; sin error |
| TEST-079 | M | CE-6, RNF-002, RNF-008 | Aplicación ejecutada desde la raíz, sin datos | Cualquier persona (QPR2) recorre: registrar 2 ejemplares → prestar → consultar → vencidos → devolver → salir | Completa el flujo solo con el menú; todos los textos están en español |
| TEST-080 | M | RNF-007 | Red desactivada | Repetir TEST-079 | Funciona igual |

### TASK-016 — Rendimiento
| ID | Tipo | Requisito | Condiciones iniciales | Entradas | Resultado esperado |
|----|------|-----------|-----------------------|----------|--------------------|
| TEST-081 | I | RNF-006 | `RENDIMIENTO=1`; 5.000 ejemplares y 20.000 préstamos generados (1.000 activos, 200 vencidos) | Cargar; cada listado; consultar por identificador; registrar un préstamo con guardado | Cada consulta tarda menos de 1 s; se registran los tiempos en `tests/evidencias.md` |

---

## 4. Cobertura

### 4.1 Criterios de aceptación → pruebas
| HU | CA → TEST |
|----|-----------|
| HU-001 | CA1 → 017, 057 · CA2 → 018, 058 · CA3 → 021, 059 · CA4 → 022 |
| HU-002 | CA1 → 040, 061 · CA2 → 041, 061 |
| HU-003 | CA1 → 042, 062 · CA2 → 042, 062 · CA3 → 043, 063 |
| HU-004 | CA1 → 025, 065 · CA2 → 026, 066 · CA3 → 027 · CA4 → 028, 068 · CA5 → 029 · CA6 → 054, 067 · CA7 → 031 |
| HU-005 | CA1 → 033, 071 · CA2 → 034, 072 · CA3 → 035 · CA4 → 036 · CA5 → 037 |
| HU-006 | CA1 → 044, 064 · CA2 → 041, 064 |
| HU-007 | CA1 → 045, 064 · CA2 → 041, 064 |
| HU-008 | CA1 → 047 · CA2 → 048 · CA3 → 073 · CA4 → 049, 074 |

### 4.2 Reglas, requisitos no funcionales y criterios de éxito
| Requisito | Pruebas |
|-----------|---------|
| RN-001 | 018, 019, 020 |
| RN-002 / RES-004 | 026, 038 |
| RN-003 | 026, 027 |
| RN-004 | 025 |
| RN-005 | 028, 029 |
| RN-006 | 003, 047, 050 |
| RN-007 | 033, 034 |
| RN-008 | 005, 037 |
| RN-009 | 002, 040, 042 |
| RN-010 | 021, 030, 053 |
| RN-011 | 031 |
| RN-012 | 031 (mismo código, sin validación contra un registro) |
| RNF-001 | 005, 075 |
| RNF-002 | 079 |
| RNF-003 | 056 y todas las F de consola |
| RNF-004 | 051, 077 |
| RNF-005 | 008, 023, 032, 039 |
| RNF-006 | 081 |
| RNF-007 | 080 |
| RNF-008 | 056, 079 |
| RNF-009 | 054, 067 |
| QP1 | 010–016, 076 |
| RC-1 | 055, 060, 069 |
| CE-1 … CE-6 | 042 · 047 · 026 · 033 · 075 · 079 |

### 4.3 Asignación a tareas
| Tarea | Pruebas | | Tarea | Pruebas |
|-------|---------|-|-------|---------|
| TASK-001 | 001 | | TASK-009 | 047–050 |
| TASK-002 | 002–004 | | TASK-010 | 051–056 |
| TASK-003 | 005–009 | | TASK-011 | 057–060 |
| TASK-004 | 010–016 | | TASK-012 | 061–064 |
| TASK-005 | 017–024 | | TASK-013 | 065–070 |
| TASK-006 | 025–032 | | TASK-014 | 071–074 |
| TASK-007 | 033–039 | | TASK-015 | 075–080 |
| TASK-008 | 040–046 | | TASK-016 | 081 |

**Totales:** 81 pruebas: 78 automatizadas y 2 manuales, más la de rendimiento (TEST-081), que es automatizada pero opcional.

## 5. Preguntas de clarificación (resueltas)

| # | Pregunta | Propuesta de la IA | Decisión del equipo |
|---|----------|--------------------|---------------------|
| QPR1 | ¿Las pruebas de consola comparan el texto exacto de los mensajes o palabras clave? | Palabras clave: así las pruebas no fallan por cambios de redacción | Aceptada. |
| QPR2 | ¿Quién ejecuta las pruebas manuales TEST-079 y TEST-080, y cuándo? | Una persona del equipo que no implementó la consola, en la Actividad 8 | **Modificada:** cualquier persona puede ejecutarlas (no necesariamente alguien que no implementó la consola), en la Actividad 8. |
| QPR3 | En TEST-081, ¿en qué equipo se mide el rendimiento? | En el computador del equipo; se anotan sus características en la evidencia | Aceptada. |
