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
| 2026-11-25 | TASK-004 | `cargar()` valida el archivo y lanza `DatosCorruptos` sin modificarlo | src/biblioteca/repositorio.py, tests/test_repositorio_corrupto.py, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-004 | TEST-010 ampliado (control y caso no UTF-8); pendientes PD-1 (tildes) y PD-2 (BOM) registrados en el plan de tareas §6 | tests/test_repositorio_corrupto.py, tests/plan_pruebas.md, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-005 | `Biblioteca`: carga inicial, índices y `registrar_ejemplar` con reversión si falla el guardado | src/biblioteca/servicio.py, tests/test_servicio_ejemplares.py, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-006 | `registrar_prestamo` con validaciones RN-002…RN-005, RN-010 y reversión si falla el guardado | src/biblioteca/servicio.py, tests/test_servicio_prestamos.py, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-006 | TEST-027 (identificador vacío) y TEST-030 (orden de validación) ampliados por decisión del equipo | tests/test_servicio_prestamos.py, tests/plan_pruebas.md, tests/evidencias.md | |
| 2026-11-25 | TASK-007 | `registrar_devolucion` con validaciones RN-007, conservación del historial (RN-008) y reversión si falla el guardado; TEST-035 ampliado (identificador vacío) | src/biblioteca/servicio.py, tests/test_servicio_devoluciones.py, tests/plan_pruebas.md, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-008 | Consultas `listar_catalogo`, `consultar_ejemplar`, `listar_disponibles`, `listar_prestados` ordenadas por identificador; TEST-043 ampliado (identificador vacío) | src/biblioteca/servicio.py, tests/test_servicio_consultas.py, tests/plan_pruebas.md, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-009 | `listar_vencidos`: préstamos activos con fecha prevista anterior a hoy, de más a menos atraso y desempate por identificador; TEST-050 ampliado (empate) | src/biblioteca/servicio.py, tests/test_servicio_vencidos.py, tests/plan_pruebas.md, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-010 | `Consola`: menú 1–6, pedir texto y fecha DD/MM/AAAA, cancelar, mensajes de error en español; PD-1 asignado a TEST-079 | src/biblioteca/consola.py, tests/test_consola_base.py, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-011 | Flujo de consola CU-001 (registrar ejemplar): aviso de cancelar, identificador repetido se vuelve a pedir, confirmación | src/biblioteca/consola.py, tests/test_consola_cu001.py, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-012 | Flujo de consola CU-002 (consultar ejemplares): submenú 1–4 con catálogo, por identificador, disponibles y prestados | src/biblioteca/consola.py, tests/test_consola_cu002.py, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-012 | TEST-061 ampliado: opción inválida del submenú y aviso de cancelar una sola vez (decisión del equipo) | tests/test_consola_cu002.py, tests/plan_pruebas.md, tests/evidencias.md | |
| 2026-11-25 | TASK-013 | Flujo de consola CU-003 (registrar préstamo): verificación del ejemplar, fecha inválida o anterior se vuelve a pedir, sin confirmación | src/biblioteca/consola.py, tests/test_consola_cu003.py, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-013 | TEST-066 ampliado con el caso 4a (ejemplar inexistente) por decisión del equipo | tests/test_consola_cu003.py, tests/plan_pruebas.md, tests/evidencias.md | |
| 2026-11-25 | TASK-014 | Flujos de consola CU-004 (devolución) y CU-005 (vencidos); se elimina el método provisional `_no_disponible` | src/biblioteca/consola.py, tests/test_consola_cu004_cu005.py, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-014 | TEST-072 (caso 4a) y TEST-074 (sin aviso de cancelar) ampliados por decisión del equipo | tests/test_consola_cu004_cu005.py, tests/plan_pruebas.md, tests/evidencias.md | |
| 2026-11-25 | TASK-015 | `__main__.py`: `python -m biblioteca [RUTA]`, datos dañados o ilegibles → código 1, argumentos de más → código 2, cierre ordenado con Ctrl+C/EOF; PD-1 ampliado tras el recorrido de humo | src/biblioteca/__main__.py, tests/test_integracion.py, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-25 | TASK-015 | TEST-076 (permisos, argumentos de más) y TEST-077 (Ctrl+C, mensaje de cierre) ampliados por decisión del equipo; PD-1 se mantiene para TEST-079 | tests/test_integracion.py, tests/plan_pruebas.md, tests/evidencias.md | |
| 2026-11-25 | TASK-016 | TEST-081: rendimiento con 5.000 ejemplares y 20.000 préstamos; consultas < 0.002 s, carga 0.27 s, guardado 0.54 s | tests/test_rendimiento.py, tests/evidencias.md, tasks/plan_tareas.md | |
| 2026-11-26 | Cierre | README: Actividad 7 aprobada, Actividades 8 y 9 fuera del alcance; matriz de trazabilidad con componentes reales y estado final | README.md, docs/trazabilidad.md | |
