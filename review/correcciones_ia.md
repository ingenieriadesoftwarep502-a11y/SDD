# Propuestas de la IA corregidas o rechazadas
Insumo para el punto 9 del informe final.

| Fecha | Actividad | Prompt | Qué propuso la IA | Problema (incorrecta / incompleta / fuera de alcance) | Cómo lo detectamos | Corrección aplicada |
|-------|-----------|--------|-------------------|------|------|------|
| 2026-11-24 | 3 | Identificación de casos de uso | Pedir confirmación al bibliotecario antes de guardar un préstamo o una devolución (QP4) | Fuera de alcance: agregaba un comportamiento que no estaba en las HU aprobadas | Revisión del equipo de las preguntas abiertas | Se rechazó; se eliminaron los pasos de confirmación de CU-003 y CU-004 |
| 2026-11-24 | 6 | Derivación de pruebas | Exigir que las pruebas manuales las ejecute una persona que no implementó la consola (QPR2) | Restricción innecesaria para el contexto del taller | Revisión del equipo de las preguntas abiertas | Se modificó: cualquier persona puede ejecutarlas |
| 2026-11-24 | 7 (TASK-001) | Diseño técnico, DEC-008 | Comando de pruebas `python -m unittest discover -s tests -v` | Incorrecto: con `-s tests` unittest no ejecuta `tests/__init__.py`, así que `src/` no queda en el path | La IA verificó el supuesto antes de implementar TASK-001 | El equipo eligió `python -m unittest -v`; se corrigió en DEC-008, TASK-001 y el plan de pruebas §1 |
