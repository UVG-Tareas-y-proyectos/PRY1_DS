# Proyecto 1 - Obtención y limpieza de datos

CC3084 Data Science · Universidad del Valle de Guatemala · Semestre II 2026

Equipo: **Ihan Marroquin (23108), Diego Patzan (23525) y Milton Polanco**.

Obtención, diagnóstico y limpieza reproducible de servicios educativos autorizados de nivel **Diversificado** en Guatemala. Fuente oficial: [MINEDUC](https://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/).

## Entregables

- [CSV limpio: 12,043 filas, 32 columnas](data/processed/diversificado_limpio.csv).
- [Libro de códigos en Markdown](docs/LIBRO_DE_CODIGOS.md) y [PDF](docs/LIBRO_DE_CODIGOS.pdf): documenta las 32 variables.
- [Informe de calidad en Markdown](docs/INFORME_CALIDAD.md) y [PDF](docs/INFORME_CALIDAD.pdf).
- [Plan de limpieza por variable, reglas y riesgos](docs/plan_limpieza.csv).
- [Registro resumido de transformaciones](reports/registro_transformaciones.csv) y [detalle por celda](reports/transformaciones_detalle.csv).
- [Pares de posibles duplicados y decisiones](reports/duplicados_parciales.csv).
- [Validación automática](reports/validacion.json) y [casos pendientes de revisión](reports/casos_para_revision.csv).

## Reproducir la entrega sin red

Entorno probado: Python 3.12; versiones exactas en requirements.txt.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.pipeline
python -m unittest discover -s tests -v
python -m src.documentacion
python -m src.pdf
```

En Linux/macOS, active el entorno con `source .venv/bin/activate`. La ejecución usa los 23 CSV y el catálogo versionados, y verifica que las fuentes no cambien. No necesita credenciales ni conexión después de instalar dependencias.

La exportación de los PDF utiliza la plantilla institucional de `assets/plantilla_uvg.docx`: Microsoft Word en Windows o LibreOffice en Linux/macOS. Conserva la portada de la UVG, el formato de texto y las tablas del modelo académico.

Para ejecutar solo la consolidación y el diagnóstico: `python -m src.consolidar`. Para volver a descargar, guarde otra versión con `python -m src.obtener --destino data/nueva_extraccion`. El servidor puede ofrecer datos distintos y no debe sobrescribirse la extracción utilizada en esta entrega.

## Resultado y decisiones

Se conservan los **12,043 códigos de servicio**, sin eliminar ni fusionar filas. El diagnóstico y la comparación antes/después usan las mismas 17 columnas; el archivo final añade 15 campos de trazabilidad y control. Se registran **13,919 correcciones de celdas**, en **8,025 servicios**.

Los municipios se contrastan con un [catálogo oficial externo del INAB](data/catalogos/fuente.json). Las zonas de capital se conservan aparte y se asignan al municipio de Guatemala. Las equivalencias por nombre están documentadas, sin usar similitud difusa para decidir geografía.

La semejanza de nombres se usa para detectar candidatos, sin eliminar códigos legítimos. Se documentan **12,063 pares**; **9,441** tienen distinta jornada o plan y **2,622** se conservan para revisión humana. Un centro puede tener varios códigos según su servicio.

La entrega aprueba **29 contratos de calidad y 5 pruebas de casos límite**. Se mantienen ausencias reales y se señalan teléfonos/distritos incompletos sin completar datos por suposición. Un teléfono con formato válido no certifica que esté activo. El libro y el informe detallan estas limitaciones.

## Estructura

```text
data/raw/          23 CSV territoriales y manifiesto SHA-256
data/catalogos/    340 municipios, dominios y equivalencias
data/interim/      consolidado crudo de 17 columnas
data/processed/    conjunto limpio único
src/               obtención, diagnóstico, limpieza, validación y documentación
tests/             casos límite de reglas de transformación
reports/           estadísticas, trazabilidad, candidatos y pruebas
docs/              plan, libro de códigos, informe y PDFs de referencia
```
