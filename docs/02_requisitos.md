# Requisitos — Gestor de préstamos de libros (v1)
Estado: APROBADO (2026-11-24) · Actividad 2 · Prompt 3.1 · Fecha: 2026-11-24
Fuente: `docs/01_intencion.md` (APROBADO)

> No se eligen herramientas de implementación: lenguaje, almacenamiento y bibliotecas se deciden en la Actividad 4.
> Las preguntas Q1–Q5 (sección 7) fueron respondidas por el equipo el 2026-11-24.

**Términos usados**
- **Ejemplar:** copia física de un libro, con su propio identificador (P1).
- **Préstamo activo:** préstamo que aún no tiene devolución registrada.
- **Fecha actual:** fecha del sistema en el momento de la operación (P4).

---

## 1. Requisitos funcionales (historias de usuario)

### HU-001 — Registrar un ejemplar
Como bibliotecario, quiero registrar un ejemplar con su identificador, título y autor, para que forme parte del catálogo.
Origen: capacidad 1, OBJ-4 · Reglas: RN-001, RN-010

- **HU-001.CA1:** Dado un identificador que no existe en el catálogo, cuando registro un ejemplar con identificador, título y autor no vacíos, entonces el ejemplar queda en el catálogo con estado *disponible* y el sistema confirma el registro.
- **HU-001.CA2:** Dado que ya existe un ejemplar con el identificador "E-01", cuando intento registrar otro con "E-01", entonces el sistema rechaza el registro, informa que el identificador ya existe y el catálogo no cambia.
- **HU-001.CA3:** Cuando intento registrar un ejemplar con identificador, título o autor vacío (o solo espacios), entonces el sistema rechaza el registro, indica qué campo falta y el catálogo no cambia.
- **HU-001.CA4:** Dado un ejemplar "E-01" con título "Cálculo I", cuando registro "E-02" con el mismo título y autor, entonces ambos ejemplares quedan en el catálogo como registros independientes.

### HU-002 — Consultar el catálogo
Como bibliotecario, quiero ver todos los ejemplares registrados con su estado, para tener una vista general del catálogo.
Origen: capacidad 1, OBJ-1 · Reglas: RN-009

- **HU-002.CA1:** Dado un catálogo con ejemplares, cuando consulto el catálogo, entonces el sistema muestra cada ejemplar con identificador, título, autor y estado (*disponible* o *prestado*).
- **HU-002.CA2:** Dado un catálogo vacío, cuando consulto el catálogo, entonces el sistema informa que no hay ejemplares registrados.

### HU-003 — Consultar un ejemplar por identificador
Como bibliotecario, quiero consultar un ejemplar por su identificador, para saber al instante si está disponible o quién lo tiene.
Origen: capacidad 4, OBJ-1, CE-1 · Reglas: RN-009

- **HU-003.CA1:** Dado un ejemplar disponible, cuando lo consulto por su identificador, entonces el sistema muestra identificador, título, autor y estado *disponible*.
- **HU-003.CA2:** Dado un ejemplar prestado, cuando lo consulto, entonces el sistema muestra además el código y nombre del estudiante y la fecha prevista de devolución.
- **HU-003.CA3:** Cuando consulto un identificador que no existe, entonces el sistema informa que el ejemplar no está registrado.

### HU-004 — Registrar un préstamo
Como bibliotecario, quiero registrar el préstamo de un ejemplar a un estudiante con una fecha prevista de devolución, para saber quién tiene cada ejemplar y hasta cuándo.
Origen: capacidad 2, OBJ-3, CE-3 · Reglas: RN-002, RN-003, RN-004, RN-005, RN-010, RN-011

- **HU-004.CA1:** Dado un ejemplar disponible, cuando registro un préstamo con código y nombre del estudiante y una fecha prevista igual o posterior a la fecha actual, entonces se crea un préstamo activo con fecha de préstamo igual a la fecha actual, el ejemplar pasa a *prestado* y el sistema confirma la operación.
- **HU-004.CA2:** Dado un ejemplar *prestado*, cuando intento prestarlo a cualquier estudiante (el mismo u otro), entonces el sistema rechaza la operación, informa que el ejemplar ya está prestado y no se crea ningún préstamo.
- **HU-004.CA3:** Cuando intento prestar un identificador que no existe, entonces el sistema rechaza la operación e informa que el ejemplar no está registrado.
- **HU-004.CA4:** Dada una fecha actual 24/11/2026, cuando registro un préstamo con fecha prevista 23/11/2026, entonces el sistema rechaza la operación e informa que la fecha prevista no puede ser anterior a la fecha del préstamo.
- **HU-004.CA5:** Dada una fecha actual 24/11/2026, cuando registro un préstamo con fecha prevista 24/11/2026, entonces el préstamo se acepta.
- **HU-004.CA6:** Cuando ingreso un código o nombre de estudiante vacío, o una fecha con formato no válido o inexistente (p. ej., 31/02/2026), entonces el sistema rechaza la operación, indica el dato incorrecto y no se crea ningún préstamo.
- **HU-004.CA7:** Dado un estudiante con un préstamo activo, cuando le presto otro ejemplar disponible, entonces el préstamo se acepta (RN-011).

### HU-005 — Registrar una devolución
Como bibliotecario, quiero registrar la devolución de un ejemplar, para que vuelva a quedar disponible.
Origen: capacidad 3, OBJ-1, CE-4 · Reglas: RN-007, RN-008

- **HU-005.CA1:** Dado un ejemplar con un préstamo activo, cuando registro su devolución, entonces el préstamo se cierra con fecha real de devolución igual a la fecha actual, el ejemplar pasa a *disponible* y el sistema confirma la operación.
- **HU-005.CA2:** Dado un ejemplar *disponible*, cuando intento registrar su devolución, entonces el sistema rechaza la operación, informa que el ejemplar no está prestado y no cambia ningún dato.
- **HU-005.CA3:** Cuando intento devolver un identificador que no existe, entonces el sistema rechaza la operación e informa que el ejemplar no está registrado.
- **HU-005.CA4:** Dado un préstamo vencido, cuando registro su devolución, entonces la devolución se acepta igual que una a tiempo.
- **HU-005.CA5:** Dada una devolución registrada, entonces el préstamo cerrado se sigue conservando con todos sus datos (RN-008).

### HU-006 — Listar ejemplares disponibles
Como bibliotecario, quiero ver la lista de ejemplares disponibles, para saber qué puedo prestar.
Origen: capacidad 4, OBJ-1 · Reglas: RN-009

- **HU-006.CA1:** Dados ejemplares disponibles y prestados, cuando consulto los disponibles, entonces el sistema muestra solo los disponibles, con identificador, título y autor.
- **HU-006.CA2:** Si no hay ejemplares disponibles, el sistema lo informa.

### HU-007 — Listar ejemplares prestados
Como bibliotecario, quiero ver la lista de ejemplares prestados, para saber quién tiene cada uno y cuándo debe devolverlo.
Origen: capacidad 4, OBJ-1 · Reglas: RN-009

- **HU-007.CA1:** Dados ejemplares disponibles y prestados, cuando consulto los prestados, entonces el sistema muestra solo los que tienen préstamo activo, con identificador, título, código y nombre del estudiante, fecha de préstamo y fecha prevista de devolución.
- **HU-007.CA2:** Si no hay ejemplares prestados, el sistema lo informa.

### HU-008 — Listar préstamos vencidos
Como bibliotecario, quiero ver los préstamos vencidos, para contactar a los estudiantes que no devolvieron a tiempo.
Origen: capacidad 4, OBJ-2, CE-2 · Reglas: RN-006

- **HU-008.CA1:** Dada una fecha actual 24/11/2026 y préstamos activos con fecha prevista 20/11/2026, 24/11/2026 y 30/11/2026, cuando consulto los vencidos, entonces el sistema muestra solo el de 20/11/2026.
- **HU-008.CA2:** Un préstamo devuelto nunca aparece como vencido, aunque se haya devuelto después de la fecha prevista.
- **HU-008.CA3:** El listado muestra, por préstamo, identificador y título del ejemplar, código y nombre del estudiante, fecha prevista y días de atraso. También indica la fecha actual usada para el cálculo (riesgo R-2).
- **HU-008.CA4:** Si no hay préstamos vencidos, el sistema lo informa.

---

## 2. Requisitos no funcionales

| ID | Requisito | Cómo se verifica |
|----|-----------|------------------|
| RNF-001 | **Persistencia:** el catálogo y los préstamos (activos y devueltos) se conservan al cerrar y volver a abrir la aplicación. | Registrar datos, cerrar, reabrir y comprobar que todo sigue igual (CE-5). |
| RNF-002 | **Usabilidad:** todas las funciones se usan desde un menú de consola, sin conocer comandos ni editar archivos. | Un usuario sin formación técnica completa el flujo registrar → prestar → consultar → devolver solo con el menú (CE-6). |
| RNF-003 | **Mensajes:** cada operación informa si tuvo éxito o, si se rechazó, el motivo concreto. | Cada criterio de rechazo de la sección 1 muestra un mensaje que identifica la causa. |
| RNF-004 | **Robustez:** una entrada inválida (texto en lugar de opción, fecha mal escrita, campo vacío) no cierra la aplicación; se vuelve a pedir el dato o se vuelve al menú. | Ingresar entradas inválidas en cada campo y comprobar que la aplicación sigue funcionando. |
| RNF-005 | **Integridad:** una operación rechazada no modifica ningún dato. Si ocurre un error durante una operación, los datos quedan como antes de ella. | Comparar el estado antes y después de cada rechazo. |
| RNF-006 | **Rendimiento (Q3):** con 5.000 ejemplares y 20.000 préstamos, cada consulta responde en menos de 1 segundo en un computador de oficina. | Prueba con datos generados. |
| RNF-007 | **Operación local:** la aplicación funciona en el computador del bibliotecario sin conexión a la red. | Ejecutar con la red desactivada. |
| RNF-008 | **Idioma:** menús y mensajes en español. | Inspección. |
| RNF-009 | **Formato de fecha (Q2):** las fechas se ingresan y muestran en un único formato, DD/MM/AAAA, que se indica al pedir el dato. | Inspección y HU-004.CA6. |

## 3. Reglas de negocio

| ID | Regla |
|----|-------|
| RN-001 | El identificador de un ejemplar es único en el catálogo. Se compara exactamente como se escribió, sin los espacios al inicio y al final (Q4). |
| RN-002 | Un ejemplar tiene como máximo un préstamo activo a la vez (RES-004). |
| RN-003 | Solo se puede prestar un ejemplar registrado y *disponible*. |
| RN-004 | La fecha de préstamo es la fecha actual del sistema; el bibliotecario no la ingresa (Q1). |
| RN-005 | La fecha prevista de devolución la ingresa el bibliotecario (P6) y no puede ser anterior a la fecha de préstamo. |
| RN-006 | Un préstamo está **vencido** si está activo y la fecha actual es posterior a la fecha prevista de devolución. El día de la fecha prevista no está vencido. |
| RN-007 | Solo se puede registrar la devolución de un ejemplar con préstamo activo. La fecha real de devolución es la fecha actual. |
| RN-008 | Los préstamos devueltos no se borran: se conservan con su fecha real de devolución (P8). |
| RN-009 | El estado de un ejemplar es *prestado* si tiene un préstamo activo; en otro caso es *disponible*. |
| RN-010 | Son obligatorios: identificador, título y autor del ejemplar; código y nombre del estudiante y fecha prevista del préstamo. |
| RN-011 | En la v1 no hay límite de préstamos activos por estudiante. |
| RN-012 | El código del estudiante no se valida contra ningún registro (P3). El sistema no comprueba que un mismo código tenga siempre el mismo nombre (Q5). |

## 4. Permisos

| ID | Permiso |
|----|---------|
| PER-001 | El bibliotecario puede ejecutar todas las operaciones del sistema. |
| PER-002 | No hay otros usuarios ni roles. El acceso a la aplicación se controla con el acceso al computador, fuera del sistema. Es una consecuencia aceptada de RES-006. |

## 5. Restricciones

| ID | Restricción |
|----|-------------|
| RES-001 | Un único actor: el bibliotecario. |
| RES-002 | Cada ejemplar tiene identificador, título y autor. |
| RES-003 | Cada préstamo se asocia a un estudiante y a una fecha prevista de devolución. |
| RES-004 | Un ejemplar no puede prestarse a dos estudiantes al mismo tiempo (se implementa como RN-002). |
| RES-005 | Aplicación de consola. |
| RES-006 | Sin autenticación, interfaz gráfica ni integraciones externas. |
| RES-007 | Python o Java (PEND-001, se decide en la Actividad 4). |
| RES-008 | En la v1 no se pueden modificar ni dar de baja ejemplares (P2). |

## 6. Exclusiones
Son las de la sección 7 de `docs/01_intencion.md`. No se repiten aquí para evitar duplicación.

## 7. Preguntas de clarificación (resueltas)

| # | Pregunta | Propuesta de la IA | Afecta a | Decisión del equipo |
|---|----------|--------------------|----------|---------------------|
| Q1 | ¿La fecha del préstamo es siempre la de hoy, o se pueden registrar préstamos hechos en días anteriores? | Siempre hoy | RN-004, HU-004.CA1 | Siempre hoy. |
| Q2 | ¿Qué formato de fecha se usa? | DD/MM/AAAA | RNF-009 | DD/MM/AAAA. |
| Q3 | ¿Qué volumen hay que soportar? | 5.000 ejemplares y 20.000 préstamos | RNF-006 | Sí: 5.000 ejemplares y 20.000 préstamos. |
| Q4 | ¿"e-01" y "E-01" son el mismo identificador? | No: se distinguen mayúsculas y minúsculas | RN-001 | No: se distinguen mayúsculas y minúsculas. |
| Q5 | Si un mismo código de estudiante aparece con nombres distintos, ¿el sistema debe avisar? | No en la v1 | RN-012 | No se avisa en la v1. |
