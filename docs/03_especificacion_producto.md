# Especificación del producto — Gestor de préstamos de libros (v1)
Estado: APROBADO (2026-11-24) · Actividad 3 · Fecha: 2026-11-24
Fuentes: `docs/01_intencion.md` y `docs/02_requisitos.md` (APROBADOS)

> Los casos de uso describen qué hace el bibliotecario y qué responde el sistema, no cómo está construido.
> Las preguntas QP1–QP5 (sección 6) fueron respondidas por el equipo el 2026-11-24. QP4 fue rechazada.

## 1. Rol
| Rol | Descripción | Permisos |
|-----|-------------|----------|
| Bibliotecario | Único actor. Usa la aplicación en su computador. | Todas las operaciones (PER-001) |

## 2. Funcionalidades incluidas
El bibliotecario llega a cada funcionalidad desde el menú principal (RNF-002).

| Opción del menú | Caso de uso | HU / RNF |
|-----------------|-------------|----------|
| Registrar ejemplar | CU-001 | HU-001 |
| Consultar ejemplares (catálogo, por identificador, disponibles, prestados) | CU-002 | HU-002, HU-003, HU-006, HU-007 |
| Registrar préstamo | CU-003 | HU-004 |
| Registrar devolución | CU-004 | HU-005 |
| Préstamos vencidos | CU-005 | HU-008 |
| Salir | CU-006 | RNF-001 |

**Recorrido típico:** iniciar la aplicación → registrar ejemplares → prestar un ejemplar → consultar su estado → revisar vencidos → registrar la devolución → salir. Es el flujo de CE-6.

**Reglas comunes a todos los casos de uso**
- **RC-1:** En cualquier paso en que se pide un dato, el bibliotecario puede cancelar. El sistema vuelve al menú principal sin cambiar ningún dato (QP2).
- **RC-2:** Cuando un dato ingresado no es válido, el sistema muestra el motivo y vuelve a pedir ese mismo dato (RNF-003, RNF-004).
- **RC-3:** Si ocurre un error al guardar, el sistema lo informa y los datos quedan como antes de la operación (RNF-005).

---

## 3. Casos de uso

### CU-001 — Registrar ejemplar
- **Actor principal:** Bibliotecario
- **Objetivo:** agregar un ejemplar físico al catálogo.
- **Precondiciones:** la aplicación está iniciada (CU-006).
- **Postcondiciones (éxito):** el ejemplar está en el catálogo con estado *disponible* y queda guardado.
- **Postcondiciones (fallo o cancelación):** el catálogo no cambia.

**Flujo principal**
1. El bibliotecario elige "Registrar ejemplar".
2. El sistema solicita el identificador.
3. El bibliotecario ingresa el identificador.
4. El sistema verifica que no esté vacío y que no exista en el catálogo (RN-001).
5. El sistema solicita el título.
6. El bibliotecario ingresa el título.
7. El sistema solicita el autor.
8. El bibliotecario ingresa el autor.
9. El sistema registra el ejemplar como *disponible*, lo guarda y confirma el registro.
10. El sistema vuelve al menú principal.

**Flujos alternativos y excepciones**
- **4a.** Identificador vacío: el sistema informa que es obligatorio y vuelve al paso 2.
- **4b.** El identificador ya existe: el sistema informa que ya está registrado y vuelve al paso 2.
- **6a / 8a.** Título o autor vacío: el sistema informa qué campo falta y lo vuelve a pedir.
- **9a.** Error al guardar: se aplica RC-3.

**HU relacionadas:** HU-001 (CA1–CA4)

### CU-002 — Consultar ejemplares
- **Actor principal:** Bibliotecario
- **Objetivo:** conocer el estado de los ejemplares (disponible o prestado y a quién).
- **Precondiciones:** la aplicación está iniciada.
- **Postcondiciones:** no se modifica ningún dato.

**Flujo principal**
1. El bibliotecario elige "Consultar ejemplares".
2. El sistema ofrece cuatro consultas: catálogo completo, por identificador, disponibles y prestados.
3. El bibliotecario elige una consulta.
4. El sistema muestra el resultado:
   - **Catálogo completo:** identificador, título, autor y estado de cada ejemplar.
   - **Por identificador:** pide el identificador y muestra identificador, título, autor y estado. Si el ejemplar está prestado, muestra también el código y nombre del estudiante y la fecha prevista de devolución.
   - **Disponibles:** identificador, título y autor de los ejemplares *disponibles*.
   - **Prestados:** identificador, título, código y nombre del estudiante, fecha de préstamo y fecha prevista de cada ejemplar con préstamo activo.

   Los listados se ordenan por identificador (QP3).
5. El sistema vuelve al menú principal.

**Flujos alternativos y excepciones**
- **4a.** El catálogo o el listado elegido no tiene elementos: el sistema informa que no hay ejemplares en esa categoría.
- **4b.** El identificador consultado no existe: el sistema informa que el ejemplar no está registrado.

**HU relacionadas:** HU-002, HU-003, HU-006, HU-007

### CU-003 — Registrar préstamo
- **Actor principal:** Bibliotecario
- **Objetivo:** prestar un ejemplar disponible a un estudiante, con fecha prevista de devolución.
- **Precondiciones:** la aplicación está iniciada y el ejemplar está registrado.
- **Postcondiciones (éxito):** existe un préstamo activo con fecha de préstamo igual a hoy. El ejemplar está *prestado* y los datos quedan guardados.
- **Postcondiciones (fallo o cancelación):** no se crea ningún préstamo y el ejemplar conserva su estado.

**Flujo principal**
1. El bibliotecario elige "Registrar préstamo".
2. El sistema solicita el identificador del ejemplar.
3. El bibliotecario ingresa el identificador.
4. El sistema verifica que el ejemplar existe y está *disponible* (RN-002, RN-003) y muestra su título y autor.
5. El sistema solicita el código del estudiante.
6. El bibliotecario ingresa el código.
7. El sistema solicita el nombre del estudiante.
8. El bibliotecario ingresa el nombre.
9. El sistema solicita la fecha prevista de devolución en formato DD/MM/AAAA (RNF-009).
10. El bibliotecario ingresa la fecha.
11. El sistema verifica que la fecha es válida y que no es anterior a hoy (RN-005).
12. El sistema registra el préstamo activo con fecha de préstamo igual a hoy (RN-004), marca el ejemplar como *prestado*, guarda y confirma la operación.

**Flujos alternativos y excepciones**
- **4a.** El ejemplar no existe: el sistema informa que no está registrado y vuelve al paso 2.
- **4b.** El ejemplar ya está prestado: el sistema informa que no está disponible y vuelve al paso 2.
- **6a / 8a.** Código o nombre vacío: el sistema informa qué campo falta y lo vuelve a pedir.
- **11a.** Formato no válido o fecha inexistente (p. ej., 31/02/2026): el sistema muestra el formato esperado y vuelve al paso 9.
- **11b.** La fecha es anterior a hoy: el sistema informa que la fecha prevista no puede ser anterior a la fecha del préstamo y vuelve al paso 9.
- **12a.** Error al guardar: se aplica RC-3.

**HU relacionadas:** HU-004 (CA1–CA7)

### CU-004 — Registrar devolución
- **Actor principal:** Bibliotecario
- **Objetivo:** cerrar el préstamo activo de un ejemplar para que vuelva a estar disponible.
- **Precondiciones:** la aplicación está iniciada.
- **Postcondiciones (éxito):** el préstamo queda cerrado con fecha real de devolución igual a hoy y se conserva en el historial (RN-008). El ejemplar está *disponible* y los datos quedan guardados.
- **Postcondiciones (fallo o cancelación):** no cambia ningún dato.

**Flujo principal**
1. El bibliotecario elige "Registrar devolución".
2. El sistema solicita el identificador del ejemplar.
3. El bibliotecario ingresa el identificador.
4. El sistema verifica que el ejemplar existe y tiene un préstamo activo (RN-007).
5. El sistema cierra el préstamo con fecha real de devolución igual a hoy, marca el ejemplar como *disponible*, guarda y confirma la operación. El préstamo se cierra igual aunque esté vencido (HU-005.CA4).

**Flujos alternativos y excepciones**
- **4a.** El ejemplar no existe: el sistema informa que no está registrado y vuelve al paso 2.
- **4b.** El ejemplar no está prestado: el sistema informa que no tiene préstamo activo y vuelve al paso 2.
- **5a.** Error al guardar: se aplica RC-3.

**HU relacionadas:** HU-005 (CA1–CA5)

### CU-005 — Consultar préstamos vencidos
- **Actor principal:** Bibliotecario
- **Objetivo:** identificar los préstamos no devueltos a tiempo.
- **Precondiciones:** la aplicación está iniciada.
- **Postcondiciones:** no se modifica ningún dato.

**Flujo principal**
1. El bibliotecario elige "Préstamos vencidos".
2. El sistema toma la fecha actual y selecciona los préstamos activos cuya fecha prevista es anterior a ella (RN-006).
3. El sistema muestra la fecha usada para el cálculo y, por cada préstamo vencido: identificador y título del ejemplar, código y nombre del estudiante, fecha prevista y días de atraso. Primero aparecen los préstamos con más días de atraso (QP3).
4. El sistema vuelve al menú principal.

**Flujos alternativos y excepciones**
- **3a.** No hay préstamos vencidos: el sistema lo informa junto con la fecha usada.

**HU relacionadas:** HU-008 (CA1–CA4)

### CU-006 — Iniciar y cerrar la aplicación
- **Actor principal:** Bibliotecario
- **Objetivo:** empezar a trabajar con los datos guardados y terminar sin perderlos.
- **Precondiciones:** ninguna.
- **Postcondiciones:** al salir, todas las operaciones completadas quedan guardadas.

**Flujo principal**
1. El bibliotecario inicia la aplicación.
2. El sistema carga el catálogo y los préstamos guardados (RNF-001).
3. El sistema muestra el menú principal.
4. El bibliotecario usa las funcionalidades (CU-001 a CU-005).
5. El bibliotecario elige "Salir".
6. El sistema termina. Cada operación completada ya quedó guardada en el momento en que se completó (QP5).

**Flujos alternativos y excepciones**
- **2a.** No hay datos guardados (primer uso): el sistema inicia con el catálogo vacío.
- **2b.** Los datos guardados no se pueden leer (archivo dañado o modificado a mano): el sistema informa el problema y termina sin sobrescribir ni borrar esos datos (QP1).
- **3a.** El bibliotecario ingresa una opción que no existe: el sistema lo informa y vuelve a mostrar el menú (RNF-004).

**Requisitos relacionados:** RNF-001, RNF-002, RNF-004, RNF-005 (sin HU propia)

---

## 4. Matriz HU ↔ CU
| HU | CU |
|----|----|
| HU-001 | CU-001 |
| HU-002 | CU-002 |
| HU-003 | CU-002 |
| HU-004 | CU-003 |
| HU-005 | CU-004 |
| HU-006 | CU-002 |
| HU-007 | CU-002 |
| HU-008 | CU-005 |
| (RNF-001) | CU-006 |

## 5. Funcionalidades excluidas de la v1
Además de las exclusiones de `docs/01_intencion.md` (sección 7):
- Modificar o dar de baja ejemplares (RES-008).
- **Corregir o anular un préstamo o una devolución registrados por error.** Consecuencia: si se presta un ejemplar al estudiante equivocado, solo se puede registrar la devolución y volver a prestarlo. El préstamo erróneo queda en el historial.
- Consultar el historial de préstamos devueltos. Se conserva (RN-008), pero no se muestra en la v1.
- Buscar por título, autor o estudiante.
- Ver los préstamos de un estudiante.

## 6. Preguntas de clarificación (resueltas)
| # | Pregunta | Propuesta de la IA | Afecta a | Decisión del equipo |
|---|----------|--------------------|----------|---------------------|
| QP1 | Si los datos guardados no se pueden leer al iniciar, ¿qué hace el sistema? | Informa el problema y termina sin tocar los datos | CU-006 (2b) | Aceptada. |
| QP2 | ¿El bibliotecario puede cancelar una operación a mitad del ingreso de datos? | Sí, en cualquier paso, sin cambios | RC-1 | Aceptada. |
| QP3 | ¿En qué orden se muestran los listados? | Por identificador; los vencidos, de más a menos atraso | CU-002, CU-005 | Aceptada. |
| QP4 | ¿Se pide confirmación antes de guardar un préstamo o una devolución? | Sí, para evitar errores, ya que no se pueden corregir (sección 5) | CU-003, CU-004 | **Rechazada:** no se pide confirmación. Se mantiene el comportamiento de HU-004 y HU-005. |
| QP5 | ¿Cada operación completada se guarda en ese momento o al salir? | En ese momento, para no perderla si la consola se cierra de golpe | CU-006, RNF-001 | Aceptada. |
