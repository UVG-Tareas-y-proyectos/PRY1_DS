# Informe de calidad de los datos

## Alcance y procedencia

Versión 1.0.0. Fuente: buscador oficial MINEDUC, nivel DIVERSIFICADO y resto de filtros TODOS. Se consolidan 12,043 registros en 17 variables de origen, procedentes de 23 CSV. El manifiesto data/raw/manifest.json contiene los datos de procedencia, filtros y sumas SHA-256.

## Comparación en las mismas 17 variables

| Métrica | Antes | Después |
| --- | --- | --- |
| Registros | 12043 | 12043 |
| Variables | 17 | 17 |
| Celdas | 204731 | 204731 |
| Vacios | 3293 | 4415 |
| Faltantes con marcadores | 4239 | 4415 |
| Porcentaje faltantes con marcadores | 2.0705 | 2.1565 |
| Variables con faltantes | 6 | 6 |
| Variables con vacios | 5 | 6 |
| Porcentaje vacios | 1.6085 | 2.1565 |
| Duplicados exactos | 0 | 0 |
| Codigos unicos | 12043 | 12043 |
| Variables con formato inconsistente | 5 | 0 |
| Telefonos fuera formato | 247 | 0 |
| Codigos fuera formato | 0 | 0 |
| Distritos incompletos | 70 | 0 |
| Municipios distintos | 354 | 334 |
| Tipos incorrectos | 0 | 0 |

El CSV final tiene 32 columnas: 17 campos de origen y 15 columnas de trazabilidad, validación y ubicación. La tabla anterior usa las mismas 17 columnas antes y después para evitar atribuir a la limpieza los vacíos añadidos por campos derivados opcionales.

Los valores faltantes pueden aumentar al convertir marcadores y teléfonos o distritos incompletos en campos vacíos. Esto hace explícita la ausencia, sin inventar información. Las columnas originales y el registro por celda permiten recuperar cada valor.

## Registro de transformaciones

| Variable | Regla y justificación | Registros | Celdas |
| --- | --- | --- | --- |
| DEPARTAMENTO | Catálogo territorial oficial; capital pertenece a Guatemala. | 4232 | 4232 |
| DIRECCION | Normalizar espacios y abreviaturas inequívocas sin alterar números. | 968 | 968 |
| DIRECTOR | Unicode NFC, espacios, mayúsculas y marcadores explícitos de ausencia; sin imputar datos. | 1423 | 1423 |
| DISTRITO | No completar códigos; mantener formatos válidos y marcar incompletos. | 70 | 70 |
| ESTABLECIMIENTO | Unicode NFC, espacios, mayúsculas y marcadores explícitos de ausencia; sin imputar datos. | 1182 | 1182 |
| MUNICIPIO | Catálogo por código y equivalencias documentadas; separar zona capital. | 5025 | 5025 |
| SUPERVISOR | Unicode NFC, espacios, mayúsculas y marcadores explícitos de ausencia; sin imputar datos. | 769 | 769 |
| TELEFONO | Separar números válidos de ocho dígitos; conservar original y pendientes. | 250 | 250 |

Se modificaron 13,919 celdas en 8,025 servicios. Los conteos de celdas no equivalen a personas ni establecimientos físicos. El detalle incluye código, variable, valor anterior, valor posterior y justificación.

## Duplicados exactos y parciales

Duplicados exactos después: 0. Se identificaron 12,063 pares candidatos mediante token_sort_ratio de RapidFuzz dentro de municipio: umbral 97, o 90 con dirección/teléfono coincidente. Se conservan todos los códigos. Diferencias de jornada o plan justifican servicios distintos; los demás pares se conservan para revisión humana. No se afirma haber realizado una revisión manual inexistente. Consulte reports/duplicados_parciales.csv para la decisión y justificación de cada par.

No se eliminaron ni fusionaron filas. La fuente MINEDUC explica que un centro puede tener múltiples códigos según nivel, plan o jornada. Los nombres similares no prueban duplicación.

## Validación y limitaciones

Resultado: APROBADO; 29/29 reglas aprobadas. El registro ejecutable está en reports/validacion.json.

Persisten ausencias reales de la fuente y contactos incompletos: 192 registros requieren revisión de teléfono, distrito o geografía. Se documentan sin imputación en reports/casos_para_revision.csv. Un teléfono con ocho dígitos tiene formato válido; no demuestra que esté activo ni que pertenezca al establecimiento. Se respetan los dos formatos de distrito porque no se dispone de un catálogo público que justifique su unificación. El catálogo INAB comprueba municipio y departamento; DEPARTAMENTAL se valida con las regiones administrativas observadas en el MINEDUC y su correspondencia territorial.

La reproducibilidad local usa los CSV y catálogos versionados. Una nueva consulta a la web puede cambiar y debe guardarse en otra carpeta. Los datos de procedencia están en los manifiestos.
