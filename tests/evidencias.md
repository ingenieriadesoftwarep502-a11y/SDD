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
