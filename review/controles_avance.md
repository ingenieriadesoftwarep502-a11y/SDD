# Controles de avance (stage gates)
No se avanza a la fase siguiente hasta marcar todos los puntos de la fase actual.

## Actividad 0
- [x] Existen las carpetas docs, tasks, tests, src, review, agent y ops
- [x] Git inicializado y primer commit realizado
- [x] agent/AGENT.md revisado y aprobado por el equipo
- [x] Convenciones de ID acordadas (README.md)
- [x] Decididos lenguaje y framework de pruebas (PEND-001, PEND-002) — cerrado en la Actividad 4

## Actividad 1
- [x] Problema, usuarios, objetivos, exclusiones, restricciones y criterios de éxito definidos
- [x] Rechazadas las funcionalidades extra que sugirió la IA
- [x] ¿Dos desarrolladores lo interpretarían igual?

## Actividad 2
- [x] Cada HU tiene ID y criterios de aceptación verificables (Dado/Cuando/Entonces)
- [x] RNF, RN, permisos y restricciones separados y con ID
- [x] Sin decisiones técnicas (lenguaje, almacenamiento) en los requisitos
- [x] Sin duplicaciones ni contradicciones con docs/01_intencion.md
- [x] Preguntas abiertas Q1–Q5 respondidas

## Actividad 3
- [x] Cada CU tiene ID, actor, objetivo, pre/postcondiciones, flujo numerado, alternativos y HU relacionadas
- [x] Todas las HU aprobadas están cubiertas por al menos un CU
- [x] Cubiertas las situaciones excepcionales (inexistente, ya prestado, no prestado, fecha inválida, error al guardar)
- [x] Los CU no agregan funciones fuera del alcance de la v1
- [x] Funcionalidades excluidas listadas
- [x] Preguntas QP1–QP5 respondidas

## Actividad 4
- [x] Componentes con responsabilidades claras, conectados a requisitos
- [x] Modelo de datos cubre RES-002, RES-003 y RN-008
- [x] Validaciones y manejo de errores cubren todas las excepciones de los CU
- [x] Cada decisión (DEC) tiene alternativas y justificación
- [x] El diseño no agrega funcionalidades fuera del alcance
- [x] Preguntas QD1–QD5 respondidas (cierra PEND-002 y PEND-003)

## Actividad 5
- [x] Cada tarea tiene ID, objetivo, requisito, resultado esperado, criterio de aceptación y límites
- [x] Todas las HU y los RNF verificables están cubiertos por alguna tarea
- [x] Dependencias y orden revisados (no hay tareas que usen algo aún no construido)
- [x] Cada tarea se puede revisar por separado
- [x] Preguntas QT1–QT3 respondidas
