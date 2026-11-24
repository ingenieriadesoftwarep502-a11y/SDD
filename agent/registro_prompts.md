# Registro de prompts usados

## ACT-0 · Prompt 4.4 — Generate a workspace plan
Fecha: 2026-11-24
Contexto entregado: idea del proyecto, enunciado del taller.
Resultado: estructura de carpetas, plantillas y convenciones de ID (ver README.md).
Ajustes del equipo:

## ACT-0 · Prompt 4.3 — Improve an agent instruction file
Fecha: 2026-11-24
Entrada: agent/AGENT_v0_original.md
Resultado: agent/AGENT.md v1.0
Ajustes del equipo:

## ACT-1 · Prompts 2.1, 2.2, 2.3, 2.4 — Clarificación, problema, dirección e intención
Fecha: 2026-11-24
Contexto entregado: idea del proyecto y condiciones iniciales del taller. En 2.3 y 2.4 el equipo respondió "hazlo".
Resultado: docs/01_intencion.md (EN REVISIÓN). Las preguntas de 2.1 y las respuestas propuestas están en el Anexo A.
Ajustes del equipo: se confirmaron las 8 respuestas propuestas (P1–P8). P2 deja fuera de la v1 modificar y dar de baja ejemplares. Documento APROBADO el 2026-11-24.

## ACT-2 · Prompt 3.1 — Draft requirements from intent
Fecha: 2026-11-24
Contexto entregado: docs/01_intencion.md (APROBADO). Instrucción adicional del taller: requisitos funcionales como HU con criterios verificables; RNF, RN, permisos y restricciones como declaraciones separadas.
Resultado: docs/02_requisitos.md (EN REVISIÓN): 8 HU, 9 RNF, 12 RN, 2 PER, 8 RES, 5 preguntas abiertas.
Ajustes del equipo: se confirmaron las 5 respuestas propuestas (Q1–Q5). Documento APROBADO el 2026-11-24.

## ACT-3 · Identificación de casos de uso (sin prompt específico del libro)
Fecha: 2026-11-24
Contexto entregado: docs/01_intencion.md y docs/02_requisitos.md (APROBADOS), plantilla de CU del taller.
Resultado: docs/03_especificacion_producto.md (EN REVISIÓN): 6 CU, matriz HU↔CU, exclusiones, 5 preguntas abiertas.
Ajustes del equipo: se aceptaron QP1, QP2, QP3 y QP5. Se rechazó QP4 (confirmación antes de guardar préstamo y devolución) porque agregaba comportamiento no definido en los requisitos. Documento APROBADO el 2026-11-24.

## ACT-4 · Propuesta de diseño técnico (sin prompt específico del libro)
Fecha: 2026-11-24
Contexto entregado: docs/02_requisitos.md y docs/03_especificacion_producto.md (APROBADOS); el equipo eligió Python.
Resultado: docs/04_diseno_tecnico.md (EN REVISIÓN): 3 capas, modelo de datos, validaciones, manejo de errores, DEC-001…DEC-012, 5 preguntas abiertas.
Ajustes del equipo: se aceptaron QD1, QD2, QD4 y QD5. En QD3 el equipo pidió alternativas; se evaluaron cinco (B–E) y se mantuvo `cancelar`, indicado una sola vez por operación en lugar de en cada pregunta. Documento APROBADO el 2026-11-24.

## ACT-5 · Prompt 3.2 — Turn a spec into tasks
Fecha: 2026-11-24
Contexto entregado: docs/04_diseno_tecnico.md (APROBADO).
Resultado: tasks/plan_tareas.md (EN REVISIÓN): 16 tareas ordenadas con dependencias, archivos permitidos y límites; 3 preguntas abiertas.
Ajustes del equipo: se aceptaron QT1, QT2 y QT3. QT2 se concretó: la prueba de rendimiento se omite salvo con RENDIMIENTO=1. Documento APROBADO el 2026-11-24.

## ACT-6 · Derivación de pruebas (sin prompt específico del libro)
Fecha: 2026-11-24
Contexto entregado: requisitos, especificación del producto, diseño técnico y plan de tareas (APROBADOS).
Resultado: tests/plan_pruebas.md (EN REVISIÓN): 81 pruebas (U/A/F/I/M), datos de prueba comunes, cobertura por CA/RN/RNF/CE, asignación a tareas; 3 preguntas abiertas.
Ajustes del equipo: se aceptaron QPR1 y QPR3. QPR2 se modificó: las pruebas manuales las puede ejecutar cualquier persona, no necesariamente alguien que no implementó la consola. Documento APROBADO el 2026-11-24.
