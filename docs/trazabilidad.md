# Matriz de trazabilidad
Estado final al cierre de la Actividad 7 (2026-11-26). Los números de TEST son los de `tests/plan_pruebas.md`.

| HU / RN / RNF | CU | DEC | TASK | TEST | Componente (src/biblioteca) | Estado |
|---------------|----|-----|------|------|-----------------------------|--------|
| HU-001 | CU-001 | DEC-002, DEC-003, DEC-006 | TASK-005, TASK-011 | 017–024, 057–060 | `servicio.Biblioteca.registrar_ejemplar`; `consola.Consola._registrar_ejemplar` | Implementado y verificado |
| HU-002 | CU-002 | DEC-003, DEC-006 | TASK-008, TASK-012 | 040, 041, 061 | `servicio.Biblioteca.listar_catalogo`; `consola.Consola._mostrar_catalogo` | Implementado y verificado |
| HU-003 | CU-002 | DEC-003, DEC-006 | TASK-008, TASK-012 | 042, 043, 062, 063 | `servicio.Biblioteca.consultar_ejemplar`; `consola.Consola._mostrar_ejemplar` | Implementado y verificado |
| HU-004 | CU-003 | DEC-003, DEC-006, DEC-007, DEC-009 | TASK-006, TASK-013 | 025–032, 054, 065–070 | `servicio.Biblioteca.registrar_prestamo`; `consola.Consola._registrar_prestamo` | Implementado y verificado |
| HU-005 | CU-004 | DEC-003, DEC-009 | TASK-007, TASK-014 | 033–039, 071, 072 | `servicio.Biblioteca.registrar_devolucion`; `consola.Consola._registrar_devolucion` | Implementado y verificado |
| HU-006 | CU-002 | DEC-003, DEC-006 | TASK-008, TASK-012 | 041, 044, 064 | `servicio.Biblioteca.listar_disponibles`; `consola.Consola._mostrar_disponibles` | Implementado y verificado |
| HU-007 | CU-002 | DEC-003, DEC-006 | TASK-008, TASK-012 | 041, 045, 064 | `servicio.Biblioteca.listar_prestados`; `consola.Consola._mostrar_prestados` | Implementado y verificado |
| HU-008 | CU-005 | DEC-007, DEC-009 | TASK-009, TASK-014 | 047–050, 073, 074 | `servicio.Biblioteca.listar_vencidos`; `modelo.Prestamo.dias_atraso`; `consola.Consola._mostrar_vencidos` | Implementado y verificado |
| RNF-001 | CU-006 | DEC-004, DEC-005, DEC-012 | TASK-003, TASK-015 | 005, 075 | `repositorio.RepositorioJSON`; `__main__.main` | Implementado y verificado |
| RNF-005 | RC-3 | DEC-002, DEC-005 | TASK-003, TASK-005–007 | 008, 023, 032, 039 | `repositorio.RepositorioJSON.guardar`; reversión en `servicio.Biblioteca` | Implementado y verificado |
| RNF-006 | — | DEC-006 | TASK-016 | 081 | índices de `servicio.Biblioteca` | Verificado con `RENDIMIENTO=1` (consultas < 0.002 s; ver `tests/evidencias.md`) |
| RNF-009 | CU-003 | DEC-007 | TASK-010, TASK-013 | 054, 067 | `consola.Consola.pedir_fecha`; `consola.formatear_fecha` | Implementado y verificado |
| QP1 (datos dañados) | CU-006 | DEC-005 | TASK-004, TASK-015 | 010–016, 076 | `repositorio.RepositorioJSON.cargar`; `__main__.main` | Implementado y verificado |
| RC-1 (cancelar) | todos | DEC-011 | TASK-010–014 | 055, 060, 069 | `consola.Consola` (`cancelar` en `pedir_texto` / `pedir_fecha`) | Implementado y verificado |

**Verificado** significa: pruebas automatizadas ejecutadas y aprobadas (78 pasan; TEST-081 se ejecuta aparte con `RENDIMIENTO=1`). La evidencia de cada tarea está en `tests/evidencias.md`.
La cobertura detallada por criterio de aceptación está en `tests/plan_pruebas.md` §4.

**Fuera de la entrega (Actividad 8, no realizada):**
- TEST-079 y TEST-080 (manuales: flujo CE-6 por una persona, RNF-002, RNF-007, RNF-008) no se ejecutaron. Solo se hizo un recorrido de humo automatizado del flujo CE-6 en TASK-015.
- PD-1 sigue abierto: con entrada por tubería en Windows (`cp1252`), los textos con tildes se guardan dañados. Ver `tasks/plan_tareas.md` §6.
