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
