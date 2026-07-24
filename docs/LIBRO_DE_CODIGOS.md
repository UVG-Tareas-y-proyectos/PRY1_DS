# Libro de códigos

Proyecto 1 · Obtención y limpieza de datos

Establecimientos educativos de Guatemala · Nivel Diversificado

## Procedencia, versión y uso

- Curso: CC3084 Data Science, Universidad del Valle de Guatemala, semestre II de 2026.
- Integrantes: Ihan Marroquin (23108), Diego Patzan (23525) y Milton Polanco.
- Unidad de observación: código de servicio educativo autorizado de nivel Diversificado. Un centro físico puede tener varios códigos.
- Fuente de datos: https://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/.
- Consulta: 23 territorios; nivel 46/DIVERSIFICADO; todos los sectores, planes, modalidades y estados.
- Fecha de entrega: 23 de julio de 2026.
- Cobertura de la extracción: 12,043 registros, 17 campos de origen, 32 columnas finales. No es un censo de personas, alumnos o edificios.
- Catálogo territorial: dominio codmuni_i del servicio público INAB; procedencia, fecha y 340 municipios en data/catalogos/fuente.json y municipios.csv.
- Versión: 1.0.0; codificación UTF-8, separador coma y encabezado. Los textos entre comillas y las comas se escapan mediante el estándar CSV.
- Ausencia: campo vacío. Se recomienda keep_default_na=False al leer para distinguirlo de categorías expresas como SIN JORNADA.
- Identificadores: leer CODIGO, DISTRITO, TELEFONO, ZONA_CAPITAL y CODIGO_MUNICIPIO como texto; no convertirlos a números.

## Transformaciones, validación y decisiones

Las correcciones se detallan en reports/transformaciones_detalle.csv y se resumen por variable y regla en reports/registro_transformaciones.csv. Se modificaron 13,919 celdas y se conservaron todas las filas. No se imputaron teléfonos, directores, supervisores ni distritos.

Las 29 reglas automáticas de la entrega verifican tipos, códigos, unicidad, espacios, teléfono, distritos, categorías y coherencia territorial. Las ausencias documentadas son permitidas; un contrato de formato no certifica que un teléfono esté activo. El resultado está en reports/validacion.json.

Se identificaron 12,063 pares de posibles coincidencias con RapidFuzz dentro de municipio. Cada par tiene decisión y justificación. La semejanza no prueba que un código sea un duplicado; se conservan servicios legítimos y se señalan los casos que requieren revisión humana. No se eliminaron ni fusionaron registros.

## Reproducibilidad

La entrega incluye los 23 CSV crudos y el catálogo usado. Para reproducir los resultados sin acceder a la red: python -m src.pipeline, python -m src.documentacion y python -m src.pdf. El proceso verifica las sumas SHA-256 antes y después. Una descarga futura puede cambiar y se guarda en una carpeta diferente. Los comandos completos y las dependencias probadas están en README.md.

## Variables del conjunto de origen

### CODIGO

**Descripción:** Código único del servicio educativo autorizado. No identifica necesariamente un plantel físico único.

**Tipo de dato:** Identificador textual; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Dos dígitos de territorio, dos de municipio/zona, cuatro de servicio y sufijo 46: 00-00-0000-46. Único y no vacío.

**Valores observados:** 12043 valores no vacíos distintos. Ejemplos más frecuentes: 16-01-0137-46; 16-01-0138-46; 16-01-0139-46; 16-01-0140-46; 16-01-0141-46.

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Conservar ceros iniciales y guiones; normalizar solo espacios externos. No inventar ni renumerar códigos.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### DISTRITO

**Descripción:** Código de distrito o supervisión educativa informado por el MINEDUC.

**Tipo de dato:** Identificador textual opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** 00-000 o 00-00-0000; vacío si falta o está incompleto.

**Valores observados:** 1683 valores no vacíos distintos. Ejemplos más frecuentes: 01-403; 01-411; 05-033; 01-101; 01-409.

**Ausencias:** 734 campos vacíos de 12,043 registros (6.09%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Mantener ambos formatos; retirar espacios externos, convertir marcadores e incompletos en vacío y conservar DISTRITO_ORIGINAL y ESTADO_DISTRITO.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### DEPARTAMENTO

**Descripción:** Departamento territorial del establecimiento según catálogo oficial.

**Tipo de dato:** Categórica nominal; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** 22 departamentos del catálogo municipios.csv.

**Valores observados:** 22 valores no vacíos distintos. Ejemplos más frecuentes: GUATEMALA; SAN MARCOS; ESCUINTLA; HUEHUETENANGO; QUETZALTENANGO.

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Normalizar acentos/espacios por catálogo. CIUDAD CAPITAL se integra en GUATEMALA, con origen y zona conservados.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### MUNICIPIO

**Descripción:** Municipio territorial validado por código. Las zonas de capital se almacenan por separado.

**Tipo de dato:** Categórica nominal; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Nombres oficiales de los 340 municipios; el nombre puede repetirse en varios departamentos, por lo que se usa CODIGO_MUNICIPIO.

**Valores observados:** 334 valores no vacíos distintos. Ejemplos más frecuentes: GUATEMALA; MIXCO; VILLA NUEVA; QUETZALTENANGO; RETALHULEU.

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Validar código, nombre y departamento con INAB; aceptar solo equivalencias explícitas. No aplicar unificación difusa.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### ESTABLECIMIENTO

**Descripción:** Nombre del centro educativo asociado al código de servicio.

**Tipo de dato:** Texto nominal opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Texto de longitud variable o vacío; nombres iguales pueden representar servicios o sedes diferentes.

**Valores observados:** 6207 valores no vacíos distintos. Ejemplos más frecuentes: INSTITUTO NACIONAL DE EDUCACION DIVERSIFICADA; INSTITUTO NACIONAL DE EDUCACIÓN DIVERSIFICADA; INED INSTITUTO NACIONAL DE EDUCACIÓN DIVERSIFICADA; CENTRO DE EDUCACIÓN EXTRAESCOLAR -CEEX-; INSTITUTO DIVERSIFICADO POR COOPERATIVA.

**Ausencias:** 5 campos vacíos de 12,043 registros (0.04%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Unicode NFC, espacios uniformes y mayúsculas. Mantener tildes existentes, siglas y puntuación con significado; no fusionar nombres automáticamente.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### DIRECCION

**Descripción:** Dirección física del establecimiento informada en la fuente.

**Tipo de dato:** Texto opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Texto o vacío; números de casa, guiones y referencias son significativos.

**Valores observados:** 7245 valores no vacíos distintos. Ejemplos más frecuentes: CABECERA MUNICIPAL; BARRIO EL CENTRO; ZONA 1; BARRIO SAN SEBASTIAN; BARRIO EL PORVENIR.

**Ausencias:** 83 campos vacíos de 12,043 registros (0.69%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Convertir marcadores explícitos en vacío; retirar caracteres invisibles y espacios repetidos; expandir AV./AVDA./AVEN. y uniformar KM. sin modificar números.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### TELEFONO

**Descripción:** Uno o más teléfonos completos extraídos de la cadena de contacto original.

**Tipo de dato:** Identificador textual opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Ocho dígitos por número; varios separados por punto y coma; vacío cuando no existe ningún número completo verificable por formato.

**Valores observados:** 6601 valores no vacíos distintos. Ejemplos más frecuentes: 22067425; 22093200; 79480009; 77602663; 45353648.

**Ausencias:** 1,079 campos vacíos de 12,043 registros (8.96%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Unir grupos 4+4 y retirar prefijo explícito +502/(502); separar números completos sin completar rangos, teléfonos antiguos o dígitos faltantes. Mantener original, estado y notas.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### SUPERVISOR

**Descripción:** Nombre de la persona responsable de supervisión educativa.

**Tipo de dato:** Texto nominal opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Texto o vacío. No se interpreta como una identidad personal verificada.

**Valores observados:** 1281 valores no vacíos distintos. Ejemplos más frecuentes: CARLOS HUMBERTO GONZALEZ DE LEON; CARLOS HUMBERTO GONZÁLEZ DE LEÓN; ELENA ELIZABETH SUCHITE GARNICA DE QUINTANILLA; AMADO SALOMON FLORES PEREZ; JUAN ENRIQUE MARTINEZ SOLANO.

**Ausencias:** 667 campos vacíos de 12,043 registros (5.54%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Normalizar Unicode, espacios y mayúsculas; marcadores de ausencia a vacío; conservar tildes, partículas y apellidos compuestos.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### DIRECTOR

**Descripción:** Nombre de la persona registrada como directora o director.

**Tipo de dato:** Texto nominal opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Texto o vacío; no imputar nombres faltantes.

**Valores observados:** 5829 valores no vacíos distintos. Ejemplos más frecuentes: ----; THELMA ONDINA VASQUEZ; -----; JORGE GRANADOS GUZMÁN; MARIA DEL ROSARIO LOPEZ ESCOBAR DE PAZ.

**Ausencias:** 1,847 campos vacíos de 12,043 registros (15.34%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Mismo tratamiento que SUPERVISOR. Se conserva el valor original para revisar marcadores y escritura.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### NIVEL

**Descripción:** Nivel educativo autorizado del servicio.

**Tipo de dato:** Categórica constante; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** DIVERSIFICADO.

**Valores observados:** DIVERSIFICADO

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Normalizar texto y comprobar que todas las filas correspondan al nivel 46.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### SECTOR

**Descripción:** Tipo de gestión del servicio educativo.

**Tipo de dato:** Categórica nominal; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Dominio explícito en categorias.json, clave SECTOR.

**Valores observados:** PRIVADO; OFICIAL; COOPERATIVA; MUNICIPAL

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Uniformar escritura contra catálogo; conservar oficial, privado, municipal y cooperativa como categorías distintas.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### AREA

**Descripción:** Clasificación urbana/rural del establecimiento.

**Tipo de dato:** Categórica nominal; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** URBANA, RURAL o SIN ESPECIFICAR.

**Valores observados:** URBANA; RURAL; SIN ESPECIFICAR

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Uniformar escritura. SIN ESPECIFICAR permanece como categoría informada y no se reemplaza por ausencia.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### STATUS

**Descripción:** Estado administrativo del código de servicio.

**Tipo de dato:** Categórica nominal; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Dominio explícito en categorias.json, clave STATUS.

**Valores observados:** ABIERTA; CERRADA TEMPORALMENTE; CERRADA DEFINITIVAMENTE; TEMPORAL TITULOS; TEMPORAL NOMBRAMIENTO

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Conservar cierres temporales, definitivos y estados temporales. No filtrar a establecimientos abiertos.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### MODALIDAD

**Descripción:** Modalidad lingüística autorizada del servicio.

**Tipo de dato:** Categórica nominal; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** MONOLINGUE o BILINGUE.

**Valores observados:** MONOLINGUE; BILINGUE

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Normalizar texto contra catálogo sin inferir idioma específico.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### JORNADA

**Descripción:** Jornada en la que está autorizado el servicio educativo.

**Tipo de dato:** Categórica nominal; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Dominio explícito en categorias.json, clave JORNADA.

**Valores observados:** DOBLE; VESPERTINA; MATUTINA; SIN JORNADA; NOCTURNA; INTERMEDIA; COMPLETA

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Uniformar escritura; SIN JORNADA se conserva separada de la ausencia. No fusionar jornadas.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### PLAN

**Descripción:** Plan o frecuencia de atención educativa autorizada.

**Tipo de dato:** Categórica nominal; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Dominio explícito en categorias.json, clave PLAN.

**Valores observados:** DIARIO(REGULAR); FIN DE SEMANA; SEMIPRESENCIAL (FIN DE SEMANA); SEMIPRESENCIAL (UN DÍA A LA SEMANA); A DISTANCIA; SEMIPRESENCIAL; VIRTUAL A DISTANCIA; SEMIPRESENCIAL (DOS DÍAS A LA SEMANA); SABATINO; DOMINICAL; MIXTO; IRREGULAR; INTERCALADO

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Mantener planes diarios, de fin de semana, virtuales y semipresenciales diferenciados. Normalización por equivalencia de acentos/caso/espacios.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### DEPARTAMENTAL

**Descripción:** Dirección departamental administrativa responsable del servicio.

**Tipo de dato:** Categórica nominal; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Regiones autorizadas en categorias.json, clave DEPARTAMENTAL; puede incluir Guatemala Norte/Sur/Oriente/Occidente o Quiché Norte.

**Valores observados:** 26 valores no vacíos distintos. Ejemplos más frecuentes: GUATEMALA NORTE; GUATEMALA OCCIDENTE; GUATEMALA SUR; SAN MARCOS; ESCUINTLA.

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Normalizar por catálogo; validar correspondencia con departamento territorial, sin confundir región administrativa con departamento.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

## Variables de trazabilidad y control

### DISTRITO_ORIGINAL

**Descripción:** Valor exacto de DISTRITO antes de la limpieza.

**Tipo de dato:** Texto original opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Contenido original sin normalización; admite espacios, marcadores y formatos inconsistentes de la fuente.

**Valores observados:** 1686 valores no vacíos distintos. Ejemplos más frecuentes: 01-403; 01-411; 05-033; 01-101; 01-.

**Ausencias:** 664 campos vacíos de 12,043 registros (5.51%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Copia previa a toda transformación. Permite auditar cada decisión; no se incluye en contratos de formato del dato limpio.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Variable preservada del dato de origen.

### DEPARTAMENTO_ORIGINAL

**Descripción:** Valor exacto de DEPARTAMENTO antes de la limpieza.

**Tipo de dato:** Texto original opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Contenido original sin normalización; admite espacios, marcadores y formatos inconsistentes de la fuente.

**Valores observados:** 23 valores no vacíos distintos. Ejemplos más frecuentes: CIUDAD CAPITAL; GUATEMALA; SAN MARCOS; ESCUINTLA; HUEHUETENANGO.

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Copia previa a toda transformación. Permite auditar cada decisión; no se incluye en contratos de formato del dato limpio.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Variable preservada del dato de origen.

### MUNICIPIO_ORIGINAL

**Descripción:** Valor exacto de MUNICIPIO antes de la limpieza.

**Tipo de dato:** Texto original opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Contenido original sin normalización; admite espacios, marcadores y formatos inconsistentes de la fuente.

**Valores observados:** 354 valores no vacíos distintos. Ejemplos más frecuentes: ZONA 1; MIXCO; VILLA NUEVA; QUETZALTENANGO; ZONA 7.

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Copia previa a toda transformación. Permite auditar cada decisión; no se incluye en contratos de formato del dato limpio.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Variable preservada del dato de origen.

### ESTABLECIMIENTO_ORIGINAL

**Descripción:** Valor exacto de ESTABLECIMIENTO antes de la limpieza.

**Tipo de dato:** Texto original opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Contenido original sin normalización; admite espacios, marcadores y formatos inconsistentes de la fuente.

**Valores observados:** 6505 valores no vacíos distintos. Ejemplos más frecuentes: INSTITUTO NACIONAL DE EDUCACION DIVERSIFICADA; INSTITUTO NACIONAL DE EDUCACIÓN DIVERSIFICADA; INED  INSTITUTO NACIONAL DE EDUCACIÓN DIVERSIFICADA; CENTRO DE EDUCACIÓN EXTRAESCOLAR -CEEX-; INSTITUTO DIVERSIFICADO POR COOPERATIVA.

**Ausencias:** 5 campos vacíos de 12,043 registros (0.04%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Copia previa a toda transformación. Permite auditar cada decisión; no se incluye en contratos de formato del dato limpio.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Variable preservada del dato de origen.

### DIRECCION_ORIGINAL

**Descripción:** Valor exacto de DIRECCION antes de la limpieza.

**Tipo de dato:** Texto original opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Contenido original sin normalización; admite espacios, marcadores y formatos inconsistentes de la fuente.

**Valores observados:** 7377 valores no vacíos distintos. Ejemplos más frecuentes: CABECERA MUNICIPAL; BARRIO EL CENTRO; ZONA 1; BARRIO SAN SEBASTIAN; BARRIO EL PORVENIR.

**Ausencias:** 75 campos vacíos de 12,043 registros (0.62%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Copia previa a toda transformación. Permite auditar cada decisión; no se incluye en contratos de formato del dato limpio.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Variable preservada del dato de origen.

### TELEFONO_ORIGINAL

**Descripción:** Valor exacto de TELEFONO antes de la limpieza.

**Tipo de dato:** Texto original opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Contenido original sin normalización; admite espacios, marcadores y formatos inconsistentes de la fuente.

**Valores observados:** 6704 valores no vacíos distintos. Ejemplos más frecuentes: 22067425; 22093200; 79480009; 77602663; 45353648.

**Ausencias:** 973 campos vacíos de 12,043 registros (8.08%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Copia previa a toda transformación. Permite auditar cada decisión; no se incluye en contratos de formato del dato limpio.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Variable preservada del dato de origen.

### SUPERVISOR_ORIGINAL

**Descripción:** Valor exacto de SUPERVISOR antes de la limpieza.

**Tipo de dato:** Texto original opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Contenido original sin normalización; admite espacios, marcadores y formatos inconsistentes de la fuente.

**Valores observados:** 1287 valores no vacíos distintos. Ejemplos más frecuentes:  ; CARLOS HUMBERTO GONZALEZ DE LEON; CARLOS HUMBERTO GONZÁLEZ DE LEÓN; ELENA ELIZABETH SUCHITE GARNICA DE QUINTANILLA; JUAN ENRIQUE MARTINEZ SOLANO.

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Copia previa a toda transformación. Permite auditar cada decisión; no se incluye en contratos de formato del dato limpio.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Variable preservada del dato de origen.

### DIRECTOR_ORIGINAL

**Descripción:** Valor exacto de DIRECTOR antes de la limpieza.

**Tipo de dato:** Texto original opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Contenido original sin normalización; admite espacios, marcadores y formatos inconsistentes de la fuente.

**Valores observados:** 5885 valores no vacíos distintos. Ejemplos más frecuentes: ---; --; ----; THELMA ONDINA VASQUEZ; SIN DATO.

**Ausencias:** 1,576 campos vacíos de 12,043 registros (13.09%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Copia previa a toda transformación. Permite auditar cada decisión; no se incluye en contratos de formato del dato limpio.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Variable preservada del dato de origen.

### ESTADO_DISTRITO

**Descripción:** Resultado de la comprobación del distrito.

**Tipo de dato:** Categórica nominal; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** VALIDO, AUSENTE, INCOMPLETO o INVALIDO.

**Valores observados:** VALIDO; AUSENTE; INCOMPLETO

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Derivado del patrón observado antes de vaciar códigos incompletos. Permite separar ausencia real de formatos incompletos.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### TELEFONO_LIMPIO

**Descripción:** Alias explícito del campo TELEFONO después de la limpieza.

**Tipo de dato:** Identificador textual opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Igual a TELEFONO en todas las filas.

**Valores observados:** 6601 valores no vacíos distintos. Ejemplos más frecuentes: 22067425; 22093200; 79480009; 77602663; 45353648.

**Ausencias:** 1,079 campos vacíos de 12,043 registros (8.96%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Copia del resultado del analizador; facilita distinguir el valor limpio de TELEFONO_ORIGINAL.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### ESTADO_TELEFONO

**Descripción:** Estado de la extracción del contacto.

**Tipo de dato:** Categórica nominal; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** VALIDO, MULTIPLE, PARCIAL, INVALIDO o AUSENTE.

**Valores observados:** VALIDO; AUSENTE; MULTIPLE; INVALIDO; PARCIAL

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** VALIDO: un número sin resto; MULTIPLE: varios sin resto; PARCIAL: números válidos más fragmentos/notas; INVALIDO: dato presente sin un número completo; AUSENTE: vacío/marcador.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### TELEFONO_NOTAS

**Descripción:** Fragmentos no interpretados, notas o cadena inválida del contacto.

**Tipo de dato:** Texto opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Texto o vacío; nunca se convierte automáticamente en otro número.

**Valores observados:** 110 valores no vacíos distintos. Ejemplos más frecuentes: 2325732, 2320075, 2307014; 00000000; 4431414, 3109992; 8392658; 73.

**Ausencias:** 11,916 campos vacíos de 12,043 registros (98.95%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Se guarda el resto del analizador o la cadena inválida para revisión. Las notas y extensiones pueden activar PARCIAL.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### ZONA_CAPITAL

**Descripción:** Zona urbana de la Ciudad Capital separada del municipio.

**Tipo de dato:** Identificador textual opcional; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Dígitos de zona cuando el territorio original es CIUDAD CAPITAL; vacío en los demás casos.

**Valores observados:** 22 valores no vacíos distintos. Ejemplos más frecuentes: 1; 7; 12; 18; 2.

**Ausencias:** 9,875 campos vacíos de 12,043 registros (82.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Se extrae ZONA n y se comprueba contra el segundo segmento del código MINEDUC. No es un municipio independiente.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### CODIGO_MUNICIPIO

**Descripción:** Código territorial municipal de cuatro dígitos.

**Tipo de dato:** Identificador textual; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** Código existente en municipios.csv. 0101 para las zonas de Ciudad Capital.

**Valores observados:** 338 valores no vacíos distintos. Ejemplos más frecuentes: 0101; 0108; 0115; 0901; 1101.

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Se deriva del prefijo del servicio y se valida contra catálogo; en capital se utiliza explícitamente Guatemala 0101.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.

### ESTADO_GEOGRAFIA

**Descripción:** Resultado de las comprobaciones territoriales.

**Tipo de dato:** Categórica nominal; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** VALIDO o REVISAR; la entrega requiere todos VALIDO.

**Valores observados:** VALIDO

**Ausencias:** 0 campos vacíos de 12,043 registros (0.00%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** Comprueba código, equivalencias de nombre, departamento y zona. No corrige por semejanza de cadenas.

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.
