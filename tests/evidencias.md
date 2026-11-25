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
