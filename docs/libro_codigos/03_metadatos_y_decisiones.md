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
