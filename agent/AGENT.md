# AGENT.md — Instrucciones para el asistente de IA

> Versión: 1.0 · Estado: APROBADO (2026-11-24) · Revisado con el Prompt 4.3 a partir de `agent/AGENT_v0_original.md`.
> Este archivo solo lo modifica el equipo. El asistente no puede editarlo.

## 1. Proyecto

**Gestor de préstamos de libros.** Una pequeña biblioteca universitaria lleva el préstamo de libros
a estudiantes en hojas de cálculo. Por eso cuesta saber qué ejemplares están disponibles, cuáles
están prestados y qué préstamos están vencidos. El objetivo es una aplicación sencilla para
administrar el catálogo y registrar préstamos y devoluciones.

## 2. Condiciones iniciales (no negociables en la versión 1)

| ID | Condición |
|----|-----------|
| RES-001 | Un único actor: el bibliotecario. |
| RES-002 | Cada libro tiene identificador, título y autor. |
| RES-003 | Cada préstamo se asocia a un estudiante y a una fecha prevista de devolución. |
| RES-004 | Un ejemplar no puede estar prestado a dos estudiantes al mismo tiempo. |
| RES-005 | La versión 1 es una aplicación de consola. |
| RES-006 | Sin autenticación, sin interfaz gráfica y sin integraciones externas (red, API, base de datos remota, correo). |
| RES-007 | Lenguaje: Python o Java. **Pendiente: lo decide el equipo** (ver §8). |

Los requisitos detallados se escriben en `docs/` durante el taller. Si este archivo y `docs/`
se contradicen, manda la versión aprobada de `docs/`. Avisa de la contradicción.

## 3. Fuente de verdad y orden de lectura

Antes de responder, lee solo los artefactos que te indique la solicitud, en este orden de autoridad:

1. `docs/02_requisitos.md` (HU, RNF, RN, RES aprobados)
2. `docs/03_especificacion_producto.md` (CU)
3. `docs/04_diseno_tecnico.md` (DEC)
4. `tasks/plan_tareas.md` (TASK)
5. `tests/plan_pruebas.md` (TEST)

Un artefacto con estado `BORRADOR` no autoriza a implementar. Solo cuentan los que estén marcados como `APROBADO`.

## 4. Trabajo por fases

- Trabaja **solo en la fase y la tarea que nombre la solicitud** (p. ej., "Actividad 2" o "TASK-003").
  Si la solicitud no nombra ninguna, pregunta antes de empezar.
- No escribas código en `src/` hasta que requisitos, diseño, tarea y plan de pruebas estén `APROBADO`.
- Una solicitud = una tarea. Al terminar, detente y entrega el reporte de §7. No empieces la tarea siguiente.
- Nunca construyas la aplicación completa en una sola respuesta, aunque se te pida.

## 5. Límites de modificación

**Permitido:** crear o editar únicamente los archivos que liste la tarea en su campo
"Archivos permitidos". Si la tarea no lista archivos, propón la lista y espera confirmación.

**Prohibido sin aprobación explícita y previa:**
- Editar, renombrar, mover o borrar archivos fuera de esa lista, incluido código que "convendría limpiar".
- Modificar `agent/`, los documentos `APROBADO` de `docs/` o tareas y pruebas ya cerradas.
- Añadir funcionalidades no pedidas. Ejemplos: multas, reservas, renovaciones, usuarios, roles,
  reportes, exportar, GUI, web, notificaciones o un límite de préstamos por estudiante.
- Añadir dependencias o bibliotecas externas. Usa solo la biblioteca estándar del lenguaje,
  salvo el framework de pruebas que apruebe el equipo.
- Cambiar la arquitectura, el modelo de datos o el formato de persistencia definidos en el diseño.
- Ejecutar comandos destructivos (`rm -rf`, `git reset --hard`, `git push --force`, borrar datos).
- Hacer `git commit` o `git push`. El equipo hace los commits.
- Acceder a la red o usar datos personales reales. Usa estudiantes y libros ficticios.

## 6. Cuándo detenerse y preguntar

Detente y pregunta, en vez de suponer, cuando una decisión afecte a:
- **Alcance:** algo no está en la HU o el CU, o hay dos interpretaciones razonables.
- **Datos:** persistencia (memoria o archivo), formato de identificadores, formato de fechas,
  cómo se determina la "fecha actual" para calcular vencidos.
- **Reglas de negocio:** qué pasa con un libro inexistente, una devolución duplicada o una fecha pasada.
- **Arquitectura:** nuevas capas, clases o módulos que no estén en el diseño.
- **Seguridad o integridad:** pérdida o sobrescritura de datos.

Formula preguntas cerradas y numeradas, con opciones. Si la duda es menor y no bloquea, márcala
como **SUPUESTO** en el reporte en lugar de decidir en silencio.

## 7. Expectativas de pruebas

- Toda implementación debe vincularse a por lo menos un TEST de `tests/plan_pruebas.md`.
- Las pruebas automatizadas van en `tests/` y se nombran con el ID: `test_TEST_004_...` o `Test004...`.
- Cada regla de negocio necesita un caso válido y un caso de fallo. Ejemplo para RES-004:
  prestar un ejemplar ya prestado debe ser rechazado.
- **Ejecuta las pruebas y copia la salida real.** No digas que "pasan" si no las ejecutaste.
  Si no puedes ejecutarlas, escríbelo.
- No modifiques, borres ni desactives una prueba existente para que algo "pase". Si crees que
  una prueba es incorrecta, repórtalo y espera decisión.
- Además de las pruebas nuevas, ejecuta todas las existentes (regresión).

## 8. Decisiones pendientes del equipo

| ID | Decisión | Estado |
|----|----------|--------|
| PEND-001 | Lenguaje: Python o Java | Abierta |
| PEND-002 | Framework de pruebas (p. ej., `unittest`/`pytest` o JUnit) | Abierta |
| PEND-003 | Persistencia de la versión 1 (en memoria o archivo local) | Abierta, se decide en la Actividad 4 |

Mientras una decisión siga abierta, no la tomes por tu cuenta.

## 9. Estilo de respuesta

- Idioma: español. Lenguaje simple. Explica el *porqué* de cada cambio importante.
- Usa siempre los IDs definidos en `README.md` (HU, CU, TASK, TEST, etc.).
- Muestra los cambios como diff o como archivo completo. Nunca uses "…resto igual…".

### Formato obligatorio del reporte

```
## Resumen
(qué se hizo, en 2–4 líneas)

## Archivos afectados
- ruta — creado | modificado — motivo

## Trazabilidad
- TASK-xxx → HU-xxx / RN-xxx → TEST-xxx

## Pruebas
- Comando ejecutado:
- Resultado real (salida resumida): N pasan / N fallan

## Supuestos y riesgos
- SUPUESTO: ...
- RIESGO: ...

## Preguntas abiertas
1. ...

## Fuera de alcance (detectado pero no hecho)
- ...
```
