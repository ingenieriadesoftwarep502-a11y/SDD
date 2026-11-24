# Engineering Intent Document — Gestor de préstamos de libros
Estado: APROBADO (2026-11-24) · Actividad 1 · Prompts 2.1–2.4 · Fecha: 2026-11-24

> Las preguntas de clarificación (Anexo A) fueron respondidas por el equipo el 2026-11-24.

## 1. Nombre del proyecto
Gestor de préstamos de libros (versión 1).

## 2. Problema (Prompt 2.2)

| Elemento | Descripción |
|----------|-------------|
| **Usuario afectado** | El bibliotecario de una pequeña biblioteca universitaria, que presta libros a estudiantes. |
| **Dificultad actual** | El catálogo y los préstamos se llevan a mano en hojas de cálculo. Para saber si un ejemplar está disponible, quién lo tiene o si un préstamo está vencido, el bibliotecario tiene que buscar y comparar filas y fechas a mano. Nada impide anotar el mismo ejemplar como prestado a dos estudiantes. |
| **Consecuencia** | Se pierde tiempo en consultas rutinarias, puede haber datos inconsistentes (préstamos duplicados, devoluciones sin registrar) y los préstamos vencidos se detectan tarde o no se detectan. |
| **Mejora deseada** | Una aplicación de consola sencilla que registre el catálogo, los préstamos y las devoluciones, impida prestar un ejemplar que ya está prestado y muestre de inmediato qué ejemplares están disponibles, cuáles están prestados y cuáles están vencidos. |

## 3. Usuarios

| Usuario | Relación con el sistema |
|---------|-------------------------|
| Bibliotecario | Único usuario directo. Opera todas las funciones. |
| Estudiante | No usa el sistema. Solo aparece como dato del préstamo. |

## 4. Objetivos
- **OBJ-1:** Saber en cualquier momento el estado de cada ejemplar: disponible o prestado.
- **OBJ-2:** Identificar los préstamos vencidos sin revisar fechas a mano.
- **OBJ-3:** Evitar préstamos inconsistentes, como un ejemplar prestado a dos estudiantes a la vez.
- **OBJ-4:** Reemplazar la hoja de cálculo como registro de préstamos y devoluciones.

## 5. Capacidades esenciales
1. **Catálogo:** registrar ejemplares (identificador, título, autor) y consultarlos. Cada ejemplar físico tiene su propio identificador; puede haber varios ejemplares del mismo título.
2. **Préstamo:** registrar el préstamo de un ejemplar disponible a un estudiante, con fecha prevista de devolución.
3. **Devolución:** registrar la devolución de un ejemplar prestado, que vuelve a quedar disponible.
4. **Consultas de estado:** listar ejemplares disponibles, ejemplares prestados (con estudiante y fecha prevista) y préstamos vencidos.

## 6. Datos clave
| Entidad | Datos |
|---------|-------|
| Ejemplar | identificador único, título, autor, estado (disponible / prestado) |
| Préstamo | ejemplar, estudiante, fecha de préstamo, fecha prevista de devolución, fecha real de devolución |
| Estudiante | código de estudiante y nombre, ingresados al registrar el préstamo (P3) |

## 7. Fuera de alcance (versión 1)
- Autenticación, usuarios, roles o varios bibliotecarios trabajando a la vez.
- Interfaz gráfica, aplicación web o móvil.
- Integraciones externas: sistemas universitarios, correo, bases de datos remotas.
- Gestión de un registro de estudiantes (alta, baja, edición).
- Modificar o dar de baja ejemplares del catálogo (P2).
- Multas, sanciones, reservas, renovaciones de préstamos.
- Límite de préstamos activos por estudiante.
- Notificaciones o recordatorios de vencimiento.
- Reportes, estadísticas, exportación o importación de datos (incluida la migración de las hojas de cálculo actuales, ver P7).
- Búsqueda avanzada (por ejemplo, por palabras clave o filtros combinados).

## 8. Restricciones
| ID | Restricción |
|----|-------------|
| RES-001 | Un único actor: el bibliotecario. |
| RES-002 | Cada libro tiene identificador, título y autor. |
| RES-003 | Cada préstamo se asocia a un estudiante y a una fecha prevista de devolución. |
| RES-004 | Un ejemplar no puede prestarse a dos estudiantes al mismo tiempo. |
| RES-005 | Aplicación de consola. |
| RES-006 | Sin autenticación, interfaz gráfica ni integraciones externas. |
| RES-007 | Python o Java (decisión del equipo, PEND-001). |

## 9. Expectativas de calidad
- **Sencillez:** un bibliotecario sin formación técnica puede usar todas las funciones desde un menú de consola.
- **Integridad:** el sistema rechaza las operaciones inválidas con un mensaje claro y no deja datos inconsistentes.
- **Persistencia:** los datos se conservan al cerrar y volver a abrir la aplicación (P5).
- **Respuesta:** las consultas responden de inmediato con el volumen de una biblioteca pequeña (**SUPUESTO** no confirmado por la biblioteca: hasta unos pocos miles de ejemplares).

## 10. Riesgos
| ID | Riesgo | Mitigación |
|----|--------|------------|
| R-1 | Ambigüedad entre "libro" y "ejemplar". | Resuelta (P1): el identificador corresponde al ejemplar físico. |
| R-2 | El cálculo de vencidos depende de la fecha del equipo, que puede estar mal configurada. | Resolver P4. Mostrar la fecha usada en la consulta de vencidos. |
| R-3 | Pérdida o corrupción de datos si la persistencia falla. | Se trata en el diseño (Actividad 4). |
| R-4 | Ampliación del alcance: la IA o el equipo agregan funciones no pedidas (multas, reservas). | Respetar la sección 7 y AGENT.md §5. |
| R-5 | Los datos actuales en hojas de cálculo no se migran. | Aceptado (P7): los ejemplares se registran manualmente. |

## 11. Criterios de éxito
- **CE-1:** El bibliotecario puede saber si un ejemplar está disponible o prestado (y a quién) con una sola consulta.
- **CE-2:** El sistema lista todos los préstamos vencidos a la fecha, y solo esos.
- **CE-3:** El sistema rechaza todos los intentos de prestar un ejemplar ya prestado.
- **CE-4:** Una devolución registrada deja el ejemplar disponible de inmediato.
- **CE-5:** Después de cerrar y reabrir la aplicación, catálogo y préstamos siguen iguales.
- **CE-6:** Todo el flujo (registrar ejemplar → prestar → consultar → devolver) se hace sin usar la hoja de cálculo.

---

## Anexo A. Preguntas de clarificación (Prompt 2.1)

La IA propuso respuestas; el equipo las confirmó el 2026-11-24.

| # | Pregunta | Ámbito | Respuesta propuesta por la IA | Decisión del equipo |
|---|----------|--------|--------------------------------|---------------------|
| P1 | ¿El identificador corresponde a un título o a un ejemplar físico? ¿Puede haber varias copias del mismo libro? | Alcance / datos | Cada registro es un **ejemplar físico** con su propio identificador. Las copias del mismo título se registran por separado. | Ejemplar físico; puede haber varios del mismo título. |
| P2 | ¿Qué significa "administrar el catálogo": solo registrar y consultar, o también modificar y dar de baja? | Alcance | V1: **registrar y consultar**. Modificar y dar de baja quedan como pregunta abierta. | Solo registrar y consultar. Modificar y dar de baja quedan fuera de la v1. |
| P3 | ¿Qué datos se necesitan del estudiante? ¿Hay que mantener un registro de estudiantes? | Datos / alcance | Solo **código y nombre**, que se ingresan al prestar. No hay registro de estudiantes. | Código y nombre. |
| P4 | ¿Cuándo un préstamo está vencido? ¿Con qué fecha se compara? | Regla | Vencido = no devuelto y **fecha actual del sistema** posterior a la fecha prevista. | Fecha actual del sistema. |
| P5 | ¿Los datos deben conservarse entre ejecuciones? | Calidad | **Sí.** Si no, la aplicación no reemplaza a la hoja de cálculo. El mecanismo se decide en la Actividad 4. | Sí. |
| P6 | ¿La fecha prevista la ingresa el bibliotecario o hay un plazo fijo? | Regla | La **ingresa el bibliotecario**. No puede ser anterior a la fecha del préstamo. | La ingresa el bibliotecario. |
| P7 | ¿Hay que importar los datos de las hojas de cálculo actuales? | Alcance | **No** en la v1. Los ejemplares se registran manualmente. | No. |
| P8 | ¿Se conserva el historial de préstamos devueltos? | Datos | **Sí**, con la fecha real de devolución. No hace falta consultarlo en la v1. | Sí. |

## Anexo B. Dirección de software (Prompt 2.3)
- **Usuario principal:** bibliotecario (sección 3).
- **Capacidades principales:** catálogo, préstamo, devolución, consultas de estado (sección 5).
- **Datos clave:** ejemplar, préstamo, estudiante (sección 6).
- **Expectativas de calidad:** sencillez, integridad, persistencia, respuesta inmediata (sección 9).
- **Exclusiones de la v1:** sección 7.
