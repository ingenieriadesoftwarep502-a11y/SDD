# Plan de tareas — Gestor de préstamos de libros (v1)
Estado: APROBADO (2026-11-24) · Actividad 5 · Prompt 3.2 · Fecha: 2026-11-24
Fuente: `docs/04_diseno_tecnico.md` (APROBADO)

> **Pruebas asociadas:** los TEST-xxx se definen en la Actividad 6 y se asignan a cada tarea antes de implementarla.
> **Límites comunes a todas las tareas** (además de AGENT.md §5): no modificar `docs/`, `agent/` ni tareas ya cerradas; no agregar dependencias; no implementar comportamientos de otra tarea.

## 1. Orden y dependencias

| Orden | Tarea | Capa | Depende de | HU / requisito principal |
|-------|-------|------|------------|--------------------------|
| 1 | TASK-001 Estructura base y entorno de pruebas | — | — | DEC-001, DEC-008, DEC-012 |
| 2 | TASK-002 Modelo y excepciones | Datos | 001 | RES-002, RES-003, RN-006 |
| 3 | TASK-003 Repositorio: cargar y guardar | Datos | 002 | RNF-001, RNF-005, QP5 |
| 4 | TASK-004 Repositorio: detección de datos dañados | Datos | 003 | QP1 |
| 5 | TASK-005 Servicio: inicio y registro de ejemplares | Negocio | 003 | HU-001 |
| 6 | TASK-006 Servicio: registrar préstamo | Negocio | 005 | HU-004 |
| 7 | TASK-007 Servicio: registrar devolución | Negocio | 006 | HU-005 |
| 8 | TASK-008 Servicio: consultas de catálogo y estado | Negocio | 006 | HU-002, HU-003, HU-006, HU-007 |
| 9 | TASK-009 Servicio: préstamos vencidos | Negocio | 006 | HU-008 |
| 10 | TASK-010 Consola: menú y entrada de datos | Presentación | 002 | RC-1, RC-2, RNF-002/004 |
| 11 | TASK-011 Consola: registrar ejemplar (CU-001) | Presentación | 005, 010 | HU-001 |
| 12 | TASK-012 Consola: consultar ejemplares (CU-002) | Presentación | 008, 010 | HU-002, 003, 006, 007 |
| 13 | TASK-013 Consola: registrar préstamo (CU-003) | Presentación | 006, 010 | HU-004 |
| 14 | TASK-014 Consola: devolución y vencidos (CU-004, CU-005) | Presentación | 007, 009, 010 | HU-005, HU-008 |
| 15 | TASK-015 Punto de entrada e inicio/cierre (CU-006) | Arranque | 004, 011–014 | RNF-001, CU-006 |
| 16 | TASK-016 Verificación de rendimiento | Pruebas | 015 | RNF-006 |

TASK-010 solo depende del modelo y de las excepciones, así que puede hacerse en paralelo con TASK-005 a TASK-009.

---

## 2. Tareas

### TASK-001 — Estructura base y entorno de pruebas
- **Objetivo:** crear el paquete vacío y dejar funcionando el comando de pruebas.
- **Requisito asociado:** DEC-001, DEC-008, DEC-012
- **Resultado esperado:** `src/biblioteca/__init__.py`; `tests/__init__.py`, que agrega `src/` a `sys.path`; `tests/test_estructura.py`, con una prueba que importa el paquete; `datos/` agregado a `.gitignore`.
- **Criterio de aceptación:** `python -m unittest -v` se ejecuta desde la raíz y muestra 1 prueba OK.
- **Archivos permitidos:** los cuatro mencionados.
- **Fuera de límites:** no crear todavía `modelo.py`, `servicio.py`, `repositorio.py` ni `consola.py`.

### TASK-002 — Modelo y excepciones
- **Objetivo:** definir las entidades y la jerarquía de errores.
- **Requisito asociado:** RES-002, RES-003, RN-006, RN-008, DEC-003, DEC-007; diseño §4.1 y §6
- **Resultado esperado:** `modelo.py` con las dataclasses `Ejemplar` y `Prestamo`. `Prestamo` tiene la propiedad `activo` y el método `dias_atraso(hoy)`, que devuelve 0 si el préstamo no está vencido. `Ejemplar` **no tiene campo de estado**. `errores.py` con todas las excepciones del diseño §6, cada una con el dato que causó el error.
- **Criterio de aceptación:** las pruebas verifican que `activo` es verdadero sin fecha de devolución y falso con ella, y que `dias_atraso` da 0 el día de la fecha prevista y 1 el día siguiente.
- **Archivos permitidos:** `src/biblioteca/modelo.py`, `src/biblioteca/errores.py`, `tests/test_modelo.py`
- **Fuera de límites:** sin validaciones de negocio en el modelo; sin E/S.

### TASK-003 — Repositorio: cargar y guardar
- **Objetivo:** persistir ejemplares y préstamos en un archivo JSON.
- **Requisito asociado:** RNF-001, RNF-005, QP5, DEC-004, DEC-005, DEC-007; diseño §3.2 y §4.3
- **Resultado esperado:** `RepositorioJSON` con:
  - `cargar()`: si el archivo no existe, devuelve listas vacías.
  - `guardar()`: escritura atómica (`.tmp` → `fsync` → `os.replace`). Crea la carpeta si no existe. UTF-8 con `ensure_ascii=False`. Fechas en ISO.
- **Criterio de aceptación:**
  - Guardar y volver a cargar devuelve datos iguales, incluidos los préstamos devueltos y los nombres con tildes.
  - Con un archivo inexistente, `cargar()` devuelve listas vacías.
  - Después de guardar no queda ningún `.tmp`.
  - Si `os.replace` falla (simulado), el archivo anterior queda intacto y se lanza `ErrorPersistencia`.
- **Archivos permitidos:** `src/biblioteca/repositorio.py`, `tests/test_repositorio.py`
- **Fuera de límites:** sin validación de contenido dañado (TASK-004); sin reglas de negocio.

### TASK-004 — Repositorio: detección de datos dañados
- **Objetivo:** rechazar al cargar un archivo inválido, sin modificarlo.
- **Requisito asociado:** QP1, CU-006 2b; diseño §5 (validaciones del archivo)
- **Resultado esperado:** `cargar()` lanza `DatosCorruptos(detalle)` si:
  - el JSON es inválido;
  - la `version` es distinta de 1;
  - falta un campo o tiene un tipo incorrecto;
  - hay una fecha no ISO;
  - hay un identificador duplicado;
  - un préstamo apunta a un ejemplar inexistente;
  - un ejemplar tiene dos préstamos activos.
- **Criterio de aceptación:** una prueba por cada caso anterior. En todas, el contenido del archivo es idéntico antes y después de `cargar()`.
- **Archivos permitidos:** `src/biblioteca/repositorio.py`, `tests/test_repositorio_corrupto.py`
- **Fuera de límites:** no reparar ni sobrescribir el archivo; no cambiar `guardar()`.

### TASK-005 — Servicio: inicio y registro de ejemplares
- **Objetivo:** crear `Biblioteca`, con carga inicial, índices y la operación `registrar_ejemplar`.
- **Requisito asociado:** HU-001 (CA1–CA4), RN-001, RN-010, RNF-005, DEC-002, DEC-006, DEC-009
- **Resultado esperado:** `Biblioteca(repositorio, reloj)` carga los datos y construye `ejemplares` y `activos`. `registrar_ejemplar` aplica `strip()`, valida, agrega, guarda y, si guardar falla, revierte. Las pruebas usan un repositorio falso en memoria.
- **Criterio de aceptación:**
  - Registro válido → el ejemplar existe y queda guardado (CA1).
  - Identificador duplicado → `EjemplarDuplicado` sin cambios (CA2). "e-01" y "E-01" son distintos (Q4).
  - Campo vacío o solo espacios → `CampoVacio` indicando el campo (CA3).
  - Dos ejemplares con el mismo título → ambos existen (CA4).
  - Fallo al guardar → `ErrorPersistencia` y el ejemplar no queda en memoria.
- **Archivos permitidos:** `src/biblioteca/servicio.py`, `tests/test_servicio_ejemplares.py`
- **Fuera de límites:** solo `__init__` y `registrar_ejemplar`; nada de préstamos ni consultas; no usar `RepositorioJSON` en estas pruebas.

### TASK-006 — Servicio: registrar préstamo
- **Objetivo:** implementar `registrar_prestamo`.
- **Requisito asociado:** HU-004 (CA1–CA5, CA7), RN-002, RN-003, RN-004, RN-005, RN-010, RN-011
- **Resultado esperado:** el método valida los campos, que el ejemplar exista y esté disponible, y que la fecha prevista sea igual o posterior a hoy. Crea el préstamo con `fecha_prestamo = reloj()`, actualiza `activos`, guarda y revierte si guardar falla.
- **Criterio de aceptación** (con reloj fijo en 24/11/2026):
  - Préstamo válido → préstamo activo con fecha 24/11/2026 (CA1).
  - Ejemplar prestado → `EjemplarNoDisponible`, sin préstamo nuevo (CA2).
  - Ejemplar inexistente → `EjemplarNoEncontrado` (CA3).
  - Fecha prevista 23/11 → `FechaPrevistaInvalida` (CA4); fecha 24/11 → se acepta (CA5).
  - Código o nombre vacío → `CampoVacio`.
  - Mismo estudiante con dos préstamos → se aceptan (CA7).
  - Fallo al guardar → se revierte.
- **Archivos permitidos:** `src/biblioteca/servicio.py` (solo el método nuevo), `tests/test_servicio_prestamos.py`
- **Fuera de límites:** no modificar `registrar_ejemplar`; no validar el formato de texto de la fecha (eso es de la consola, HU-004.CA6); no agregar límite por estudiante.

### TASK-007 — Servicio: registrar devolución
- **Objetivo:** implementar `registrar_devolucion`.
- **Requisito asociado:** HU-005 (CA1–CA5), RN-007, RN-008
- **Resultado esperado:** el método exige un préstamo activo. Asigna `fecha_devolucion = reloj()`, lo quita de `activos`, guarda y revierte si guardar falla. El préstamo se conserva en `prestamos`.
- **Criterio de aceptación:**
  - Devolución válida → fecha real = hoy y ejemplar disponible (CA1).
  - Ejemplar disponible → `EjemplarNoPrestado` (CA2).
  - Ejemplar inexistente → `EjemplarNoEncontrado` (CA3).
  - Préstamo vencido → se acepta (CA4).
  - El préstamo cerrado sigue en el historial (CA5).
  - Después de devolver, el ejemplar se puede volver a prestar.
- **Archivos permitidos:** `src/biblioteca/servicio.py` (solo el método nuevo), `tests/test_servicio_devoluciones.py`
- **Fuera de límites:** no borrar préstamos; no agregar multas ni cálculos de atraso al devolver.

### TASK-008 — Servicio: consultas de catálogo y estado
- **Objetivo:** implementar `listar_catalogo`, `consultar_ejemplar`, `listar_disponibles` y `listar_prestados`.
- **Requisito asociado:** HU-002, HU-003, HU-006, HU-007, RN-009, QP3
- **Resultado esperado:** los cuatro métodos devuelven los datos según el diseño §3.1, ordenados por identificador, y no modifican el estado.
- **Criterio de aceptación** (con 3 ejemplares, 1 prestado):
  - El catálogo muestra los 3 con el préstamo correcto.
  - Disponibles devuelve 2 y prestados devuelve 1, con los datos del estudiante.
  - La consulta por identificador funciona para un ejemplar disponible, uno prestado y uno inexistente (`EjemplarNoEncontrado`).
  - Con el catálogo vacío, las listas salen vacías.
  - No se llama a `guardar()`.
- **Archivos permitidos:** `src/biblioteca/servicio.py` (solo los métodos nuevos), `tests/test_servicio_consultas.py`
- **Fuera de límites:** sin búsqueda por título, autor ni estudiante; sin historial.

### TASK-009 — Servicio: préstamos vencidos
- **Objetivo:** implementar `listar_vencidos`.
- **Requisito asociado:** HU-008 (CA1, CA2, CA4), RN-006, QP3, DEC-009
- **Resultado esperado:** el método devuelve `(fecha_usada, lista)` con los préstamos activos cuya fecha prevista es anterior a hoy, ordenados de más a menos días de atraso.
- **Criterio de aceptación:**
  - Con hoy 24/11/2026 y fechas previstas 20/11, 24/11 y 30/11, solo aparece la de 20/11 (CA1).
  - Un préstamo devuelto tarde no aparece (CA2).
  - Sin vencidos → lista vacía y fecha usada correcta (CA4).
  - El orden es por días de atraso.
- **Archivos permitidos:** `src/biblioteca/servicio.py` (solo el método nuevo), `tests/test_servicio_vencidos.py`
- **Fuera de límites:** sin notificaciones ni filtros extra.

### TASK-010 — Consola: menú y entrada de datos
- **Objetivo:** crear la base de la interfaz de consola.
- **Requisito asociado:** RC-1, RC-2, RC-3, RNF-002, RNF-003, RNF-004, RNF-008, RNF-009, CU-006 3a, DEC-010, DEC-011
- **Resultado esperado:** clase `Consola(biblioteca, entrada, salida)` con:
  - Bucle de menú principal con 6 opciones, incluida "Salir".
  - Ayudas para pedir un texto obligatorio (vuelve a pedirlo si viene vacío), pedir una fecha DD/MM/AAAA (vuelve a pedirla si no es válida) y detectar `cancelar` sin distinguir mayúsculas.
  - Traducción de cada excepción del diseño §6 a un mensaje en español.
  - Las opciones del menú, todavía sin implementar, muestran "no disponible".
- **Criterio de aceptación** (con entrada simulada):
  - Una opción inválida muestra un mensaje y vuelve a mostrar el menú.
  - "Salir" termina el bucle.
  - Un texto vacío se vuelve a pedir.
  - "31/02/2026" y "2026-11-24" se rechazan y se vuelven a pedir; "24/11/2026" se acepta.
  - "CANCELAR" vuelve al menú.
- **Archivos permitidos:** `src/biblioteca/consola.py`, `tests/test_consola_base.py`
- **Fuera de límites:** sin reglas de negocio en la consola; no implementar todavía los flujos de los CU.

### TASK-011 — Consola: registrar ejemplar (CU-001)
- **Objetivo:** conectar la opción del menú con `registrar_ejemplar`.
- **Requisito asociado:** CU-001, HU-001
- **Resultado esperado:** el flujo de CU-001 completo: aviso de "cancelar" al inicio, identificador → título → autor. Con un identificador duplicado se vuelve a pedir el identificador (4b). Muestra la confirmación.
- **Criterio de aceptación** (con entrada simulada y servicio real con repositorio falso): registro válido; identificador duplicado y luego uno válido; campo vacío y luego uno válido; cancelar a mitad sin cambios.
- **Archivos permitidos:** `src/biblioteca/consola.py` (solo este flujo), `tests/test_consola_cu001.py`
- **Fuera de límites:** no modificar `servicio.py`.

### TASK-012 — Consola: consultar ejemplares (CU-002)
- **Objetivo:** mostrar las cuatro consultas.
- **Requisito asociado:** CU-002, HU-002, HU-003, HU-006, HU-007
- **Resultado esperado:** un submenú con catálogo, por identificador, disponibles y prestados, con los campos de cada consulta según CU-002 y las fechas en DD/MM/AAAA. Si la consulta no tiene resultados, muestra un mensaje.
- **Criterio de aceptación:** la salida contiene los campos exigidos por HU-002.CA1, HU-003.CA1–CA3, HU-006.CA1–CA2 y HU-007.CA1–CA2.
- **Archivos permitidos:** `src/biblioteca/consola.py` (solo este flujo), `tests/test_consola_cu002.py`
- **Fuera de límites:** no modificar `servicio.py`; sin paginación ni filtros extra.

### TASK-013 — Consola: registrar préstamo (CU-003)
- **Objetivo:** conectar la opción del menú con `registrar_prestamo`.
- **Requisito asociado:** CU-003, HU-004 (incluida CA6)
- **Resultado esperado:** el flujo de CU-003: identificador (se muestran título y autor) → código → nombre → fecha prevista. Atiende las excepciones 4a, 4b, 6a/8a, 11a y 11b del CU, volviendo al paso que corresponde. **No se pide confirmación** (QP4 rechazada).
- **Criterio de aceptación:**
  - Préstamo válido.
  - Ejemplar prestado → mensaje y se vuelve a pedir el identificador.
  - Fecha "31/02/2026" → se vuelve a pedir la fecha.
  - Fecha anterior a hoy → mensaje y se vuelve a pedir la fecha.
  - Cancelar en cualquier paso → sin préstamo.
- **Archivos permitidos:** `src/biblioteca/consola.py` (solo este flujo), `tests/test_consola_cu003.py`
- **Fuera de límites:** no modificar `servicio.py`; no agregar confirmación.

### TASK-014 — Consola: devolución y vencidos (CU-004, CU-005)
- **Objetivo:** conectar las opciones del menú con `registrar_devolucion` y `listar_vencidos`.
- **Requisito asociado:** CU-004, CU-005, HU-005, HU-008 (incluida CA3)
- **Resultado esperado:**
  - Devolución: identificador → cierre del préstamo y confirmación; atiende 4a y 4b.
  - Vencidos: muestra la fecha usada y, por cada préstamo, identificador, título, código, nombre, fecha prevista y días de atraso; si no hay vencidos, lo informa.
- **Criterio de aceptación:**
  - Devolución válida; devolución de un ejemplar no prestado (mensaje).
  - El listado de vencidos contiene la fecha usada y los campos de HU-008.CA3.
  - Mensaje cuando no hay vencidos.
- **Archivos permitidos:** `src/biblioteca/consola.py` (solo estos flujos), `tests/test_consola_cu004_cu005.py`
- **Fuera de límites:** no modificar `servicio.py`; no agregar confirmación.

### TASK-015 — Punto de entrada e inicio/cierre (CU-006)
- **Objetivo:** permitir ejecutar la aplicación con `python -m biblioteca [RUTA]`.
- **Requisito asociado:** CU-006, RNF-001, RNF-004, QP1, DEC-012; CE-5, CE-6
- **Resultado esperado:** `__main__.py` arma el repositorio con la ruta (por defecto `datos/biblioteca.json`), el servicio y la consola.
  - Con `DatosCorruptos`, muestra el detalle y sale con código 1 sin escribir.
  - Con Ctrl+C o fin de entrada, termina de forma ordenada.
- **Criterio de aceptación:**
  - Prueba de integración en una carpeta temporal: registrar, prestar, salir; luego reiniciar y comprobar que los datos siguen (CE-5).
  - Un archivo dañado produce el código 1 y el archivo queda sin cambios.
  - Ejecución manual desde la raíz del repositorio, para que los datos queden en `datos/` (DEC-012). En PowerShell: `$env:PYTHONPATH="src"; python -m biblioteca`. Se recorre el flujo completo de CE-6.
- **Archivos permitidos:** `src/biblioteca/__main__.py`, `tests/test_integracion.py`
- **Fuera de límites:** no modificar otros módulos. Si hace falta, reportar y crear una tarea nueva.

### TASK-016 — Verificación de rendimiento
- **Objetivo:** comprobar RNF-006.
- **Requisito asociado:** RNF-006, DEC-006
- **Resultado esperado:** una prueba que genera 5.000 ejemplares y 20.000 préstamos en una carpeta temporal y mide la carga, cada listado y una operación con guardado. Por ser lenta, se omite (`unittest.skipUnless`) salvo que se defina la variable de entorno `RENDIMIENTO=1` (QT2). En PowerShell: `$env:RENDIMIENTO="1"; python -m unittest tests.test_rendimiento -v`.
- **Criterio de aceptación:** cada consulta tarda menos de 1 s. Los tiempos medidos quedan en `tests/evidencias.md`.
- **Archivos permitidos:** `tests/test_rendimiento.py`, `tests/evidencias.md`
- **Fuera de límites:** **no optimizar código en esta tarea.** Si falla, se reporta y se crea una tarea nueva.

---

## 3. Reglas de ejecución (para la Actividad 7)
1. Se implementa **una tarea por solicitud**, en el orden de la sección 1 (AGENT.md §4).
2. En cada tarea, primero se escriben las pruebas asociadas y después el código.
3. Una tarea pasa a **Hecha** cuando cumple su criterio de aceptación, y a **Verificada** cuando el equipo revisó el código y se ejecutó toda la suite (regresión).
4. Si una tarea necesita tocar un archivo fuera de "Archivos permitidos", se detiene y se reporta.
5. **Cierre obligatorio de cada tarea** (decidido por el equipo en TASK-001). Antes de pedir la aprobación, en la misma solicitud:
   - registrar en `tests/evidencias.md` los comandos ejecutados y su resultado real (incluida la ejecución que falla antes del código);
   - actualizar el estado de la tarea en la sección 4;
   - agregar la fila de la tarea en `review/registro_cambios.md`;
   - eliminar los archivos que la tarea deja sin uso (p. ej., marcadores `.gitkeep`) y reportarlo.
   Estos archivos de cierre se pueden modificar aunque no figuren en "Archivos permitidos". **Una tarea sin este cierre no se puede aprobar.**

## 4. Estado

| Tarea | Estado |
|-------|--------|
| TASK-001 | Verificada (2026-11-25) |
| TASK-002 | Verificada (2026-11-25) |
| TASK-003 | Verificada (2026-11-25) |
| TASK-004 | Verificada (2026-11-25) |
| TASK-005 | Verificada (2026-11-25) |
| TASK-006 | Verificada (2026-11-25) |
| TASK-007 | Verificada (2026-11-25) |
| TASK-008 | Verificada (2026-11-25) |
| TASK-009 | Verificada (2026-11-25) |
| TASK-010 | Verificada (2026-11-25) |
| TASK-011 | Verificada (2026-11-25) |
| TASK-012 | Verificada (2026-11-25) |
| TASK-013 | Verificada (2026-11-25) |
| TASK-014 | Verificada (2026-11-25) |
| TASK-015 … TASK-016 | Pendiente |

## 5. Preguntas de clarificación (resueltas)

| # | Pregunta | Propuesta de la IA | Decisión del equipo |
|---|----------|--------------------|---------------------|
| QT1 | ¿Las pruebas automatizadas se escriben dentro de cada tarea (antes del código) o en tareas aparte? | Dentro de cada tarea, primero las pruebas | Aceptada. |
| QT2 | ¿TASK-016 (rendimiento) se incluye como prueba automatizada o se verifica a mano en la Actividad 8? | Prueba automatizada, ejecutada aparte por ser lenta | Aceptada. |
| QT3 | ¿Les parece bien la granularidad (16 tareas) o prefieren unir las de consola (011–014) en dos? | Mantener 16: cada una se revisa en pocos minutos | Aceptada. |

## 6. Pendientes detectados (para una tarea posterior)
Decisiones del equipo: se registran aquí y se asignan a una tarea cuando sea oportuno.

| # | Detectado en | Pendiente | Estado |
|---|--------------|-----------|--------|
| PD-1 | TASK-002 | Las tildes pueden verse mal (`�`) en la consola de Windows; revisar al implementar la consola (RNF-008). | Se verificará en TEST-079, en la consola real (decisión del equipo en TASK-010). Si falla, se corrige en una tarea nueva. |
| PD-2 | TASK-004 | Un archivo de datos con marca BOM al inicio (editado con algunos editores) se rechaza como dañado. | Pendiente ("en otra tarea más oportuna") |
