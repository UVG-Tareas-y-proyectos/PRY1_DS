# Lectura del diagnóstico inicial

El diagnóstico se ejecuta antes de limpiar, leyendo todas las columnas como texto para conservar ceros iniciales y teléfonos. No modifica los CSV territoriales. Cada archivo crudo se comprueba contra su manifiesto SHA-256 y su total de filas.

## Tablas reproducibles

- `perfil_variables.csv`: tipo leído y semántico, vacíos, faltantes incluyendo marcadores, porcentaje, valores únicos, espacios externos/múltiples, caracteres invisibles y variantes por escritura.
- `resumen.json`: filas, columnas, celdas, ausencias y porcentajes, duplicados exactos, códigos únicos, formatos de teléfono/código/distrito y número de municipios observados.
- `categorias_observadas.csv`: todos los valores y frecuencias de las diez variables categóricas.
- `valores_fuera_catalogo.csv`: nombres o categorías que requieren equivalencia, incluidas zonas de Ciudad Capital.
- `por_territorio.csv`: verificación de cobertura de las 23 consultas.
- `duplicados_iniciales.json`: exactos, códigos repetidos y coincidencias de nombre-dirección-teléfono tras normalización básica.
- `codigos_repetidos.csv` y `duplicados_exactos.csv`: filas completas cuando existan casos.

## Interpretación

Un campo vacío y un marcador como SIN DATO se cuentan por separado; el total de faltantes los combina. Una fila puede presentar más de un problema y no debe sumarse entre tablas como si se tratara de registros distintos. Los valores únicos incluyen el vacío cuando se indica expresamente.

El número de nombres municipales observados puede superar o diferir de la cantidad de municipios: capital se desglosa por zonas, un mismo nombre puede aparecer en varios departamentos y la fuente puede usar variantes. La validación debe considerar conjuntamente código y departamento.

Los códigos de distrito de dos formatos distintos no se marcan como errores solo por su longitud. Los códigos parciales sí requieren revisión. Un teléfono con varios números válidos no es necesariamente incorrecto; se necesita una representación uniforme que preserve su multiplicidad.

Las coincidencias por nombre, dirección y contacto son candidatos, no autorización para eliminar filas. El portal admite varios códigos de servicio por centro según nivel, jornada o plan.
