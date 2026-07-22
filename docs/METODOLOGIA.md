# Metodología del proyecto

El proceso comienza con 23 consultas territoriales del MINEDUC para el nivel Diversificado. Los CSV crudos se conservan sin modificar y se verifican mediante sus sumas SHA-256.

La consolidación comprueba el esquema, la cobertura y el número de registros antes de generar las estadísticas de calidad. El diagnóstico identifica ausencias, marcadores, inconsistencias de formato y candidatos a duplicación. El plan establece reglas y riesgos antes de aplicar las transformaciones.

Para consolidar y diagnosticar sin limpiar: `python -m src.consolidar`. El proceso completo de limpieza, validación y documentación se ejecuta con los comandos indicados en README.md.
