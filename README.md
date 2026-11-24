# Gestor de préstamos de libros — Taller SDD

Aplicación de consola para que el bibliotecario de una biblioteca universitaria administre el catálogo
y registre préstamos y devoluciones. Se desarrolla con Spec-Driven Development asistido por IA.

## Estructura

| Carpeta | Contenido | Actividad |
|---------|-----------|-----------|
| `docs/` | Intención, requisitos, especificación de producto, diseño técnico, trazabilidad | 1–4 |
| `tasks/` | Plan de tareas de implementación | 5 |
| `tests/` | Plan de pruebas y pruebas automatizadas | 6–7 |
| `src/` | Código fuente | 7 |
| `review/` | Revisiones, controles de avance, registro de cambios, correcciones a la IA | todas |
| `agent/` | `AGENT.md` y registro de prompts usados | todas |
| `ops/` | Guía de ejecución y solicitudes de cambio | 8–9 |

## Convenciones de identificadores

Usa tres dígitos y no reutilices un ID, aunque el elemento se elimine (se marca `RETIRADO`).

| Prefijo | Artefacto | Archivo | Ejemplo |
|---------|-----------|---------|---------|
| `HU-` | Historia de usuario | `docs/02_requisitos.md` | HU-001 |
| `RNF-` | Requisito no funcional | `docs/02_requisitos.md` | RNF-001 |
| `RN-` | Regla de negocio | `docs/02_requisitos.md` | RN-001 |
| `RES-` | Restricción | `docs/02_requisitos.md` | RES-001 |
| `PER-` | Permiso | `docs/02_requisitos.md` | PER-001 |
| `CU-` | Caso de uso | `docs/03_especificacion_producto.md` | CU-001 |
| `DEC-` | Decisión de diseño | `docs/04_diseno_tecnico.md` | DEC-001 |
| `TASK-` | Tarea | `tasks/plan_tareas.md` | TASK-001 |
| `TEST-` | Prueba | `tests/plan_pruebas.md` | TEST-001 |
| `CR-` | Solicitud de cambio | `ops/solicitudes_cambio.md` | CR-001 |

Los criterios de aceptación se numeran dentro de su HU: `HU-001.CA1`, `HU-001.CA2`.

**Estados de un artefacto:** `BORRADOR` → `EN REVISIÓN` → `APROBADO`. Solo un artefacto `APROBADO`
permite pasar a la fase siguiente.

**Commits:** `[ACT-n] descripción` o `[TASK-xxx] descripción`. Ejemplo: `[ACT-0] Estructura inicial del repositorio`.

## Estado de las fases

| Actividad | Artefacto | Estado |
|-----------|-----------|--------|
| 0. Espacio de trabajo | estructura, `agent/AGENT.md` | APROBADO |
| 1. Intención | `docs/01_intencion.md` | APROBADO |
| 2. Requisitos | `docs/02_requisitos.md` | APROBADO |
| 3. Especificación de producto | `docs/03_especificacion_producto.md` | APROBADO |
| 4. Diseño técnico | `docs/04_diseno_tecnico.md` | Pendiente |
| 5. Tareas | `tasks/plan_tareas.md` | Pendiente |
| 6. Pruebas | `tests/plan_pruebas.md` | Pendiente |
| 7. Implementación | `src/`, `tests/` | Pendiente |
| 8. Revisión | `review/revision_final.md`, `ops/guia_ejecucion.md` | Pendiente |
| 9. Mantenimiento | `ops/solicitudes_cambio.md` | Pendiente |
