# Registro de cambios

| Fecha | Actividad / ID | Cambio | Artefactos afectados | Commit |
|-------|----------------|--------|----------------------|--------|
| 2026-11-24 | ACT-0 | Estructura inicial y AGENT.md revisado | README.md, agent/, docs/, tasks/, tests/, review/, ops/ | |
| 2026-11-24 | ACT-0 | Actividad 0 aprobada | README.md, agent/AGENT.md, review/controles_avance.md | |
| 2026-11-24 | ACT-1 | Borrador del Engineering Intent Document | docs/01_intencion.md, agent/registro_prompts.md | |
| 2026-11-24 | ACT-1 | Decisiones P1–P8 incorporadas; intención APROBADA | docs/01_intencion.md, README.md, review/controles_avance.md | |
| 2026-11-24 | ACT-2 | Borrador de requisitos | docs/02_requisitos.md, docs/trazabilidad.md, README.md | |
| 2026-11-24 | ACT-2 | Decisiones Q1–Q5 incorporadas; requisitos APROBADOS | docs/02_requisitos.md, docs/trazabilidad.md, README.md, review/controles_avance.md | |
| 2026-11-24 | ACT-3 | Borrador de especificación del producto | docs/03_especificacion_producto.md, docs/trazabilidad.md, README.md | |
| 2026-11-24 | ACT-3 | QP4 rechazada (pasos de confirmación eliminados de CU-003 y CU-004); especificación del producto APROBADA | docs/03_especificacion_producto.md, docs/trazabilidad.md, README.md, review/controles_avance.md, review/correcciones_ia.md | |
| 2026-11-24 | ACT-4 | Borrador de diseño técnico; PEND-001 decidida (Python) | docs/04_diseno_tecnico.md, docs/trazabilidad.md, agent/AGENT.md, README.md | |
| 2026-11-24 | ACT-4 | QD1–QD5 resueltas; PEND-002 y PEND-003 cerradas; diseño técnico APROBADO | docs/04_diseno_tecnico.md, agent/AGENT.md, docs/trazabilidad.md, README.md, review/controles_avance.md | |
| 2026-11-24 | ACT-5 | Borrador del plan de tareas | tasks/plan_tareas.md, docs/trazabilidad.md, README.md | |
| 2026-11-24 | ACT-5 | QT1–QT3 resueltas; plan de tareas APROBADO | tasks/plan_tareas.md, docs/trazabilidad.md, README.md, review/controles_avance.md | |
| 2026-11-24 | ACT-6 | Borrador del plan de pruebas | tests/plan_pruebas.md, docs/trazabilidad.md, README.md | |
| 2026-11-24 | ACT-6 | QPR1–QPR3 resueltas (QPR2 modificada); plan de pruebas APROBADO | tests/plan_pruebas.md, docs/trazabilidad.md, README.md, review/controles_avance.md, review/correcciones_ia.md | |
| 2026-11-24 | TASK-001 | Paquete `biblioteca` y entorno de pruebas; comando de pruebas corregido a `python -m unittest -v`; regla de cierre obligatorio por tarea; `src/.gitkeep` eliminado | src/biblioteca/__init__.py, tests/__init__.py, tests/test_estructura.py, .gitignore, src/.gitkeep (eliminado), docs/04_diseno_tecnico.md, tasks/plan_tareas.md, tests/plan_pruebas.md, tests/evidencias.md, review/correcciones_ia.md | |
| 2026-11-25 | TASK-002 | Entidades `Ejemplar` y `Prestamo`; jerarquía de excepciones | src/biblioteca/modelo.py, src/biblioteca/errores.py, tests/test_modelo.py, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-002 | Se quitó de TEST-003 un caso no previsto en el plan de pruebas (opción A del equipo) | tests/test_modelo.py, tests/evidencias.md | |
| 2026-11-25 | TASK-003 | `RepositorioJSON`: cargar y guardar con escritura atómica | src/biblioteca/repositorio.py, tests/test_repositorio.py, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-003 | TEST-008 ampliado: no debe quedar `.tmp` si guardar falla (decisión del equipo) | tests/test_repositorio.py, tests/plan_pruebas.md, tests/evidencias.md | |
