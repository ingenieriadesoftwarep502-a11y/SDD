# Evidencia de ejecución de pruebas
<!-- ## fecha · TASK-xxx
Comando:
Resultado: N pasan / N fallan
Salida relevante: -->

## 2026-11-24 · TASK-001 — Estructura base y entorno de pruebas
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.

**Ejecución 1: antes de crear el paquete (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: 0 pasan / 1 falla (error)
- Salida relevante: `ModuleNotFoundError: No module named 'biblioteca'` → `FAILED (errors=1)`

**Ejecución 2: después de crear el paquete**
- Comando: `python -m unittest -v`
- Resultado: 1 pasa / 0 fallan
- Salida relevante: `test_TEST_001_importa_paquete_desde_src ... ok` → `Ran 1 test` → `OK`

**Ejecución 3: regresión después de eliminar `src/.gitkeep`**
- Comando: `python -m unittest -v`
- Resultado: 1 pasa / 0 fallan

| Prueba | Resultado |
|--------|-----------|
| TEST-001 | Pasa |

## 2026-11-25 · TASK-002 — Modelo y excepciones
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.

**Ejecución 1: con las pruebas escritas y sin el código (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: 1 pasa (TEST-001) / 1 error
- Salida relevante: `ModuleNotFoundError: No module named 'biblioteca.errores'` → `FAILED (errors=1)`

**Ejecución 2: después de implementar `modelo.py` y `errores.py` (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 4 pasan / 0 fallan
- Salida relevante: `Ran 4 tests` → `OK`

| Prueba | Resultado |
|--------|-----------|
| TEST-001 (regresión) | Pasa |
| TEST-002 | Pasa |
| TEST-003 | Pasa |
| TEST-004 | Pasa |

**Ejecución 3: después de quitar de TEST-003 el caso no previsto en el plan (decisión del equipo, opción A)**
- Comando: `python -m unittest -v`
- Resultado: 4 pasan / 0 fallan
- Nota: el comportamiento "préstamo devuelto → 0 días de atraso" se verificará en TEST-048 (TASK-009).

## 2026-11-25 · TASK-003 — Repositorio: cargar y guardar
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.
Decisiones del equipo antes de implementar: cualquier `OSError` al guardar → `ErrorPersistencia`; borrar el `.tmp` si falla; JSON con sangría de 2 espacios; en TEST-005 se agrega un préstamo P3 activo de E-03 a "Ñuñez Álvarez".

**Ejecución 1: con las pruebas escritas y sin el código (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: 4 pasan (regresión) / 1 error
- Salida relevante: `ModuleNotFoundError: No module named 'biblioteca.repositorio'` → `FAILED (errors=1)`

**Ejecución 2: después de implementar `repositorio.py` (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 9 pasan / 0 fallan
- Salida relevante: `Ran 9 tests` → `OK`

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-004 (regresión) | Pasan |
| TEST-005 | Pasa |
| TEST-006 | Pasa |
| TEST-007 | Pasa |
| TEST-008 | Pasa |
| TEST-009 | Pasa |

**Ejecución 3: TEST-008 ampliado (no queda `.tmp` si guardar falla), por decisión del equipo**
- Comando: `python -m unittest -v`
- Resultado: 9 pasan / 0 fallan
- Control: con el borrado del `.tmp` desactivado (simulado con `mock`, sin modificar el código), TEST-008 falla con `AssertionError: Lists differ: [...biblioteca.json.tmp] != []`. La comprobación detecta el defecto.

## 2026-11-25 · TASK-004 — Repositorio: detección de datos dañados
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.
Decisiones del equipo antes de implementar: un archivo que no es UTF-8 → `DatosCorruptos` (los errores del sistema al leer se propagan como `OSError`); los campos extra se ignoran; no se validan textos vacíos ni la coherencia entre fechas.

**Ejecución 1: con las pruebas escritas y sin la validación (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: TEST-001 a TEST-009 pasan; TEST-010 a TEST-016 fallan (`failures=5, errors=3`).

**Ejecución 2: después de implementar la validación (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 16 pasan / 0 fallan
- Control adicional: `guardar()` es idéntico al del commit anterior (límite de la tarea).

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-009 (regresión) | Pasan |
| TEST-010 a TEST-016 | Pasan |

**Ejecución 3: TEST-010 ampliado (control del contenido base y caso no UTF-8), por decisión del equipo**
- Comando: `python -m unittest -v`
- Resultado: 16 pasan / 0 fallan
- Control: el contenido del caso Latin-1 produce `UnicodeDecodeError` al decodificarlo como UTF-8 (byte 68), así que el caso prueba la detección de codificación y no la de JSON.

## 2026-11-25 · TASK-005 — Servicio: inicio y registro de ejemplares
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.

**Ejecución 1: con las pruebas escritas y sin el código (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: TEST-001 a TEST-016 pasan; 1 error (`No module named 'biblioteca.servicio'`).

**Ejecución 2: después de implementar `servicio.py` (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 24 pasan / 0 fallan

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-016 (regresión) | Pasan |
| TEST-017 a TEST-024 | Pasan |

## 2026-11-25 · TASK-006 — Servicio: registrar préstamo
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.
Decisiones del equipo antes de implementar: validar en el orden de CU-003 (ejemplar → código → nombre → fecha); identificador vacío → `CampoVacio`; código y nombre se guardan sin espacios al inicio y al final.

**Ejecución 1: con las pruebas escritas y sin el método (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: TEST-001 a TEST-024 pasan; TEST-025 a TEST-032 dan error (el método no existe).

**Ejecución 2: después de implementar `registrar_prestamo` (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 32 pasan / 0 fallan
- Control adicional: `registrar_ejemplar` es idéntico al del commit anterior (límite de la tarea).

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-024 (regresión) | Pasan |
| TEST-025 a TEST-032 | Pasan |

**Ejecución 3: TEST-027 y TEST-030 ampliados (identificador vacío y orden de validación), por decisión del equipo**
- Comando: `python -m unittest -v`
- Resultado: 32 pasan / 0 fallan
- Control: en una copia temporal del código con el orden alterado (código y nombre antes que el ejemplar), TEST-030 falla en 2 subcasos. El caso de orden detecta el defecto. El código del proyecto no se modificó.

## 2026-11-25 · TASK-007 — Servicio: registrar devolución
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.
Decisión del equipo antes de implementar: identificador vacío → `CampoVacio`, con el caso agregado a TEST-035.

**Ejecución 1: con las pruebas escritas y sin el método (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: TEST-001 a TEST-032 pasan; TEST-033 a TEST-039 dan error (el método no existe).

**Ejecución 2: después de implementar `registrar_devolucion` (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 39 pasan / 0 fallan
- Control adicional: `registrar_ejemplar` y `registrar_prestamo` son idénticos a los del commit anterior (límite de la tarea).

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-032 (regresión) | Pasan |
| TEST-033 a TEST-039 | Pasan |

## 2026-11-25 · TASK-008 — Servicio: consultas de catálogo y estado
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.
Decisiones del equipo antes de implementar: orden por identificador como texto simple; identificador vacío en la consulta → `CampoVacio`, con el caso agregado a TEST-043.
Datos: D1 cargado con los ejemplares en orden inverso, para que las pruebas de orden detecten la falta de ordenamiento.

**Ejecución 1: con las pruebas escritas y sin los métodos (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: TEST-001 a TEST-039 pasan; TEST-040 a TEST-046 dan error (los métodos no existen).

**Ejecución 2: después de implementar las cuatro consultas (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 46 pasan / 0 fallan
- Control adicional 1: `registrar_ejemplar`, `registrar_prestamo` y `registrar_devolucion` son idénticos a los del commit anterior (límite de la tarea).
- Control adicional 2: en una copia temporal sin ordenamiento, TEST-040 y TEST-044 fallan. Las pruebas de orden detectan el defecto.

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-039 (regresión) | Pasan |
| TEST-040 a TEST-046 | Pasan |

## 2026-11-25 · TASK-009 — Servicio: préstamos vencidos
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.
Decisión del equipo antes de implementar: a igual atraso, se ordena por identificador; caso de empate agregado a TEST-050.

**Ejecución 1: con las pruebas escritas y sin el método (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: TEST-001 a TEST-046 pasan; TEST-047 a TEST-050 dan error (el método no existe).

**Ejecución 2: después de implementar `listar_vencidos` (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 50 pasan / 0 fallan
- Control adicional 1: los siete métodos anteriores del servicio son idénticos a los del commit anterior (límite de la tarea).
- Control adicional 2: en copias temporales, TEST-050 falla sin ordenamiento y falla sin desempate por identificador. La prueba detecta ambos defectos.

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-046 (regresión) | Pasan |
| TEST-047 a TEST-050 | Pasan |

## 2026-11-25 · TASK-010 — Consola: menú y entrada de datos
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.
Decisiones del equipo antes de implementar: menú del 1 al 6 (6 = Salir); Ctrl+C y fin de entrada se manejan en TASK-015; al cancelar se muestra "Operación cancelada."; PD-1 se verifica en TEST-079.

**Ejecución 1: con las pruebas escritas y sin el código (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: TEST-001 a TEST-050 pasan; 1 error (`No module named 'biblioteca.consola'`).

**Ejecución 2: después de implementar `consola.py` (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 56 pasan / 0 fallan

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-050 (regresión) | Pasan |
| TEST-051 a TEST-056 | Pasan |

## 2026-11-25 · TASK-011 — Consola: registrar ejemplar (CU-001)
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.
Implementación explicada antes de aplicarla: el identificador repetido se detecta con `consultar_ejemplar` (método existente) para volver a pedirlo antes del título (CU-001 4b), sin modificar `servicio.py`.

**Ejecución 1: con las pruebas escritas y sin el flujo (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: TEST-001 a TEST-056 pasan; TEST-057 a TEST-060 fallan (`failures=3, errors=1`): la opción 1 aún mostraba "no disponible".

**Ejecución 2: después de implementar el flujo (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 60 pasan / 0 fallan
- Control adicional: `servicio.py` sin cambios (límite de la tarea).

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-056 (regresión) | Pasan |
| TEST-057 a TEST-060 | Pasan |

## 2026-11-25 · TASK-012 — Consola: consultar ejemplares (CU-002)
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.
Decisiones del equipo antes de implementar: submenú 1–4 (opción inválida se vuelve a pedir); cada ejemplar en una línea con separadores "|".

**Ejecución 1: con las pruebas escritas y sin el flujo (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: TEST-001 a TEST-060 pasan; TEST-061 a TEST-064 fallan (`failures=4`): la opción 2 aún mostraba "no disponible".

**Ejecución 2: después de implementar el flujo (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 64 pasan / 0 fallan
- Control adicional: `servicio.py` y el flujo de CU-001 sin cambios (límite de la tarea).

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-060 (regresión) | Pasan |
| TEST-061 a TEST-064 | Pasan |

**Ejecución 3: TEST-061 ampliado (opción inválida del submenú y aviso de cancelar una sola vez), por decisión del equipo**
- Comando: `python -m unittest -v`
- Resultado: 64 pasan / 0 fallan
- Control: en copias temporales, TEST-061 falla si la opción inválida vuelve al menú en lugar de pedirse de nuevo, y falla si el aviso de cancelar se muestra dos veces. El código del proyecto no se modificó.

## 2026-11-25 · TASK-013 — Consola: registrar préstamo (CU-003)
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.
Implementación explicada antes de aplicarla: el ejemplar se verifica con `consultar_ejemplar` antes de pedir el código (CU-003 4a/4b); si `registrar_prestamo` responde `FechaPrevistaInvalida`, se vuelve a pedir solo la fecha (11b). Sin confirmación (QP4) y sin modificar `servicio.py`.

**Ejecución 1: con las pruebas escritas y sin el flujo (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: TEST-001 a TEST-064 pasan; TEST-065 a TEST-070 fallan (`failures=6`): la opción 3 aún mostraba "no disponible".

**Ejecución 2: después de implementar el flujo (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 70 pasan / 0 fallan
- Control adicional 1: `servicio.py` y los demás métodos de la consola sin cambios (límite de la tarea).
- Control adicional 2: en una copia temporal con una confirmación agregada antes de registrar, TEST-070 falla. La prueba protege la decisión QP4.

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-064 (regresión) | Pasan |
| TEST-065 a TEST-070 | Pasan |

**Ejecución 3: TEST-066 ampliado con el caso 4a (ejemplar inexistente), por decisión del equipo**
- Comando: `python -m unittest -v`
- Resultado: 70 pasan / 0 fallan
- Control: en una copia temporal donde el caso 4a vuelve al menú en lugar de pedir de nuevo el identificador, TEST-066 falla. El código del proyecto no se modificó.

## 2026-11-25 · TASK-014 — Consola: devolución y vencidos (CU-004, CU-005)
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.
Decisión del equipo antes de implementar: "Préstamos vencidos" no muestra el aviso de cancelar (no pide datos).

**Ejecución 1: con las pruebas escritas y sin los flujos (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: TEST-001 a TEST-070 pasan; TEST-071 a TEST-074 fallan (`failures=4`): las opciones 4 y 5 aún mostraban "no disponible".

**Ejecución 2: después de implementar los flujos (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 74 pasan / 0 fallan
- Control adicional: `servicio.py` y los demás métodos de la consola sin cambios (límite de la tarea). Se eliminó el método provisional `_no_disponible`, que quedó sin uso.

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-070 (regresión) | Pasan |
| TEST-071 a TEST-074 | Pasan |

**Ejecución 3: TEST-072 (caso 4a) y TEST-074 (sin aviso de cancelar) ampliados, por decisión del equipo**
- Comando: `python -m unittest -v`
- Resultado: 74 pasan / 0 fallan
- Control: en copias temporales, TEST-072 falla si el caso 4a vuelve al menú en lugar de pedir de nuevo el identificador, y TEST-074 falla si "Préstamos vencidos" muestra el aviso de cancelar. El código del proyecto no se modificó.

## 2026-11-25 · TASK-015 — Punto de entrada e inicio/cierre (CU-006)
Entorno: Windows 11, Python 3.14.7. Ejecutado desde la raíz del repositorio.
Decisiones del equipo antes de implementar: error del sistema al leer → mensaje y código 1; al cerrar con Ctrl+C o fin de entrada → "Aplicación cerrada."; más de un argumento → uso y código 2; recorrido de humo real en lugar de la ejecución manual (TEST-079/080 quedan para la Actividad 8).

**Ejecución 1: con las pruebas escritas y sin el código (debe fallar)**
- Comando: `python -m unittest -v`
- Resultado: TEST-001 a TEST-074 pasan; 1 error (`No module named 'biblioteca.__main__'`).

**Ejecución 2: después de implementar `__main__.py` (suite completa)**
- Comando: `python -m unittest -v`
- Resultado: 78 pasan / 0 fallan
- Control adicional: ningún otro módulo de `src/` cambió (límite de la tarea).

| Prueba | Resultado |
|--------|-----------|
| TEST-001 a TEST-074 (regresión) | Pasan |
| TEST-075 a TEST-078 | Pasan |
| TEST-079, TEST-080 (manuales) | Pendientes: Actividad 8 (QPR2) |

**Recorrido de humo real (`python -m biblioteca RUTA` como proceso, entrada por tubería, carpeta temporal)**
- Flujo CE-6: registrar E-01 y E-02 → prestar E-01 → consultar prestados → vencidos ("No hay préstamos vencidos al 25/11/2026") → devolver E-01 → catálogo (ambos disponibles) → salir. Código de salida 0.
- Reinicio: E-01 aparece "disponible" con sus datos (persistencia, CE-5). Código 0.
- Archivo dañado: mensaje con el detalle y la ruta; código 1.
- Argumentos de más: "Uso: python -m biblioteca [RUTA]"; código 2.
- Fin de entrada en el menú: "Aplicación cerrada."; código 0.
- `datos/` del repositorio no se creó ni se modificó.
- **Hallazgo (PD-1):** con tubería, `sys.stdin` y `sys.stdout` usan `cp1252`. Los textos propios se ven con `�` y los textos con tildes ingresados se guardan dañados (p. ej., "Física" → `'F�\xadsica'`). Registrado en el plan de tareas §6 (PD-1). No se corrigió: queda para TEST-079 según la decisión del equipo.

**Ejecución 3: TEST-076 (permisos, argumentos de más) y TEST-077 (Ctrl+C, mensaje de cierre) ampliados, por decisión del equipo**
- Comando: `python -m unittest -v`
- Resultado: 78 pasan / 0 fallan
- Control: en copias temporales, cada caso nuevo falla con su defecto: sin manejo de permisos (TEST-076), sin control de argumentos (TEST-076), sin mensaje de cierre (TEST-077) y sin atrapar Ctrl+C (TEST-077). En este último, la primera versión de la prueba dejaba escapar la interrupción y detenía la suite; se ajustó para que falle con un mensaje claro. El código del proyecto no se modificó.
- PD-1 queda para TEST-079 (decisión del equipo).

## 2026-11-25 · TASK-016 — Verificación de rendimiento (RNF-006)
Equipo (QPR3): Intel Core i5-1135G7 @ 2.40 GHz (4 núcleos, 8 hilos), 15.8 GB de RAM, disco SSD; Windows 11, Python 3.14.7.
Decisión del equipo antes de implementar: el límite de 1 s se exige a las consultas; la carga y el guardado se miden y se registran sin límite.
Nota: esta tarea no agrega código a la aplicación, así que no tiene una ejecución previa que falle.

**Suite normal (sin RENDIMIENTO)**
- Comando: `python -m unittest -v`
- Resultado: 79 pruebas; 78 pasan, 1 omitida (TEST-081), 0 fallan.

**TEST-081 con `RENDIMIENTO=1`**
- Comando (PowerShell): `$env:RENDIMIENTO="1"; python -m unittest tests.test_rendimiento -v`
- Datos: 5.000 ejemplares y 20.000 préstamos (1.000 activos, 200 vencidos); archivo de 5.80 MB.
- Resultado: 1 pasa / 0 fallan (1.4 s en total, incluida la generación de datos).

| Medición | Tiempo | Límite | Resultado |
|----------|--------|--------|-----------|
| Carga inicial | 0.273 s | sin límite (se registra) | — |
| `listar_catalogo` | 0.0013 s | 1 s | Cumple |
| `listar_disponibles` | 0.0007 s | 1 s | Cumple |
| `listar_prestados` | 0.0007 s | 1 s | Cumple |
| `listar_vencidos` | 0.0004 s | 1 s | Cumple |
| `consultar_ejemplar` | < 0.0001 s | 1 s | Cumple |
| `registrar_prestamo` con guardado | 0.536 s | sin límite (se registra) | — |

Observaciones:
- El archivo ocupa 5.80 MB, más que los ~4 MB estimados en DEC-004, por la sangría de 2 espacios decidida en TASK-003. No afecta el cumplimiento.
- Con el volumen máximo, cada operación que guarda (registrar, prestar, devolver) tarda alrededor de medio segundo, porque reescribe el archivo completo con `fsync` (DEC-005). No hay requisito para este tiempo.
