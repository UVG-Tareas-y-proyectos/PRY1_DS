"""Genera el libro de códigos Markdown a partir del esquema y datos reales."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .comun import catalogos
from .obtener import COLUMNAS

DESCRIPCIONES = {
    "CODIGO": ("Código único del servicio educativo autorizado. No identifica necesariamente un plantel físico único.", "Identificador textual", "Dos dígitos de territorio, dos de municipio/zona, cuatro de servicio y sufijo 46: 00-00-0000-46. Único y no vacío.", "Conservar ceros iniciales y guiones; normalizar solo espacios externos. No inventar ni renumerar códigos."),
    "DISTRITO": ("Código de distrito o supervisión educativa informado por el MINEDUC.", "Identificador textual opcional", "00-000 o 00-00-0000; vacío si falta o está incompleto.", "Mantener ambos formatos; retirar espacios externos, convertir marcadores e incompletos en vacío y conservar DISTRITO_ORIGINAL y ESTADO_DISTRITO."),
    "DEPARTAMENTO": ("Departamento territorial del establecimiento según catálogo oficial.", "Categórica nominal", "22 departamentos del catálogo municipios.csv.", "Normalizar acentos/espacios por catálogo. CIUDAD CAPITAL se integra en GUATEMALA, con origen y zona conservados."),
    "MUNICIPIO": ("Municipio territorial validado por código. Las zonas de capital se almacenan por separado.", "Categórica nominal", "Nombres oficiales de los 340 municipios; el nombre puede repetirse en varios departamentos, por lo que se usa CODIGO_MUNICIPIO.", "Validar código, nombre y departamento con INAB; aceptar solo equivalencias explícitas. No aplicar unificación difusa."),
    "ESTABLECIMIENTO": ("Nombre del centro educativo asociado al código de servicio.", "Texto nominal opcional", "Texto de longitud variable o vacío; nombres iguales pueden representar servicios o sedes diferentes.", "Unicode NFC, espacios uniformes y mayúsculas. Mantener tildes existentes, siglas y puntuación con significado; no fusionar nombres automáticamente."),
    "DIRECCION": ("Dirección física del establecimiento informada en la fuente.", "Texto opcional", "Texto o vacío; números de casa, guiones y referencias son significativos.", "Convertir marcadores explícitos en vacío; retirar caracteres invisibles y espacios repetidos; expandir AV./AVDA./AVEN. y uniformar KM. sin modificar números."),
    "TELEFONO": ("Uno o más teléfonos completos extraídos de la cadena de contacto original.", "Identificador textual opcional", "Ocho dígitos por número; varios separados por punto y coma; vacío cuando no existe ningún número completo verificable por formato.", "Unir grupos 4+4 y retirar prefijo explícito +502/(502); separar números completos sin completar rangos, teléfonos antiguos o dígitos faltantes. Mantener original, estado y notas."),
    "SUPERVISOR": ("Nombre de la persona responsable de supervisión educativa.", "Texto nominal opcional", "Texto o vacío. No se interpreta como una identidad personal verificada.", "Normalizar Unicode, espacios y mayúsculas; marcadores de ausencia a vacío; conservar tildes, partículas y apellidos compuestos."),
    "DIRECTOR": ("Nombre de la persona registrada como directora o director.", "Texto nominal opcional", "Texto o vacío; no imputar nombres faltantes.", "Mismo tratamiento que SUPERVISOR. Se conserva el valor original para revisar marcadores y escritura."),
    "NIVEL": ("Nivel educativo autorizado del servicio.", "Categórica constante", "DIVERSIFICADO.", "Normalizar texto y comprobar que todas las filas correspondan al nivel 46."),
    "SECTOR": ("Tipo de gestión del servicio educativo.", "Categórica nominal", "Dominio explícito en categorias.json, clave SECTOR.", "Uniformar escritura contra catálogo; conservar oficial, privado, municipal y cooperativa como categorías distintas."),
    "AREA": ("Clasificación urbana/rural del establecimiento.", "Categórica nominal", "URBANA, RURAL o SIN ESPECIFICAR.", "Uniformar escritura. SIN ESPECIFICAR permanece como categoría informada y no se reemplaza por ausencia."),
    "STATUS": ("Estado administrativo del código de servicio.", "Categórica nominal", "Dominio explícito en categorias.json, clave STATUS.", "Conservar cierres temporales, definitivos y estados temporales. No filtrar a establecimientos abiertos."),
    "MODALIDAD": ("Modalidad lingüística autorizada del servicio.", "Categórica nominal", "MONOLINGUE o BILINGUE.", "Normalizar texto contra catálogo sin inferir idioma específico."),
    "JORNADA": ("Jornada en la que está autorizado el servicio educativo.", "Categórica nominal", "Dominio explícito en categorias.json, clave JORNADA.", "Uniformar escritura; SIN JORNADA se conserva separada de la ausencia. No fusionar jornadas."),
    "PLAN": ("Plan o frecuencia de atención educativa autorizada.", "Categórica nominal", "Dominio explícito en categorias.json, clave PLAN.", "Mantener planes diarios, de fin de semana, virtuales y semipresenciales diferenciados. Normalización por equivalencia de acentos/caso/espacios."),
    "DEPARTAMENTAL": ("Dirección departamental administrativa responsable del servicio.", "Categórica nominal", "Regiones autorizadas en categorias.json, clave DEPARTAMENTAL; puede incluir Guatemala Norte/Sur/Oriente/Occidente o Quiché Norte.", "Normalizar por catálogo; validar correspondencia con departamento territorial, sin confundir región administrativa con departamento."),
}

DERIVADAS = {
    "ESTADO_DISTRITO": ("Resultado de la comprobación del distrito.", "Categórica nominal", "VALIDO, AUSENTE, INCOMPLETO o INVALIDO.", "Derivado del patrón observado antes de vaciar códigos incompletos. Permite separar ausencia real de formatos incompletos."),
    "TELEFONO_LIMPIO": ("Alias explícito del campo TELEFONO después de la limpieza.", "Identificador textual opcional", "Igual a TELEFONO en todas las filas.", "Copia del resultado del analizador; facilita distinguir el valor limpio de TELEFONO_ORIGINAL."),
    "ESTADO_TELEFONO": ("Estado de la extracción del contacto.", "Categórica nominal", "VALIDO, MULTIPLE, PARCIAL, INVALIDO o AUSENTE.", "VALIDO: un número sin resto; MULTIPLE: varios sin resto; PARCIAL: números válidos más fragmentos/notas; INVALIDO: dato presente sin un número completo; AUSENTE: vacío/marcador."),
    "TELEFONO_NOTAS": ("Fragmentos no interpretados, notas o cadena inválida del contacto.", "Texto opcional", "Texto o vacío; nunca se convierte automáticamente en otro número.", "Se guarda el resto del analizador o la cadena inválida para revisión. Las notas y extensiones pueden activar PARCIAL."),
    "ZONA_CAPITAL": ("Zona urbana de la Ciudad Capital separada del municipio.", "Identificador textual opcional", "Dígitos de zona cuando el territorio original es CIUDAD CAPITAL; vacío en los demás casos.", "Se extrae ZONA n y se comprueba contra el segundo segmento del código MINEDUC. No es un municipio independiente."),
    "CODIGO_MUNICIPIO": ("Código territorial municipal de cuatro dígitos.", "Identificador textual", "Código existente en municipios.csv. 0101 para las zonas de Ciudad Capital.", "Se deriva del prefijo del servicio y se valida contra catálogo; en capital se utiliza explícitamente Guatemala 0101."),
    "ESTADO_GEOGRAFIA": ("Resultado de las comprobaciones territoriales.", "Categórica nominal", "VALIDO o REVISAR; la entrega requiere todos VALIDO.", "Comprueba código, equivalencias de nombre, departamento y zona. No corrige por semejanza de cadenas."),
}


def variable_section(col, spec, series, raw=False):
    description, kind, domain, treatment = spec
    counts = series.value_counts()
    unique = int(series[series.ne("")].nunique())
    values = [str(x) for x in counts.index if x != ""]
    observed = "; ".join(values if len(values) <= 15 else values[:5])
    if len(values) > 15:
        observed = f"{unique} valores no vacíos distintos. Ejemplos más frecuentes: {observed}."
    blank = int(series.eq("").sum())
    return f"""### {col}

**Descripción:** {description}

**Tipo de dato:** {kind}; almacenamiento CSV UTF-8 e importación Python como string.

**Dominio permitido:** {domain}

**Valores observados:** {observed or 'Solo valores vacíos en esta extracción.'}

**Ausencias:** {blank:,} campos vacíos de {len(series):,} registros ({100 * blank / len(series):.2f}%). El CSV representa ausencia mediante campo vacío, no mediante el literal NA.

**Tratamiento y utilidad:** {treatment}

**Metadatos:** fuente y fecha de entrega de la sección de procedencia; versión 1.0.0. {'Variable preservada del dato de origen.' if raw else 'Se registra cualquier modificación del campo de origen en transformaciones_detalle.csv; las derivadas se documentan en su fórmula.'}

"""


def generar(root):
    clean = pd.read_csv(root / "data/processed/diversificado_limpio.csv", dtype="string", keep_default_na=False)
    manifest = json.loads((root / "data/raw/manifest.json").read_text(encoding="utf-8"))
    final = json.loads((root / "reports/resumen_final.json").read_text(encoding="utf-8"))
    original = "## Variables del conjunto de origen\n\n" + "".join(variable_section(c, DESCRIPCIONES[c], clean[c]) for c in COLUMNAS)
    derived = "## Variables de trazabilidad y control\n\n"
    for col in clean.columns:
        if col in COLUMNAS:
            continue
        if col.endswith("_ORIGINAL"):
            field = col.removesuffix("_ORIGINAL")
            spec = (f"Valor exacto de {field} antes de la limpieza.", "Texto original opcional", "Contenido original sin normalización; admite espacios, marcadores y formatos inconsistentes de la fuente.", "Copia previa a toda transformación. Permite auditar cada decisión; no se incluye en contratos de formato del dato limpio.")
            derived += variable_section(col, spec, clean[col], raw=True)
        else:
            derived += variable_section(col, DERIVADAS[col], clean[col])
    metadata = f'''## Procedencia, versión y uso

- Curso: CC3084 Data Science, Universidad del Valle de Guatemala, semestre II de 2026.
- Integrantes: Ihan Marroquin (23108), Diego Patzan (23525) y Milton Polanco.
- Unidad de observación: código de servicio educativo autorizado de nivel Diversificado. Un centro físico puede tener varios códigos.
- Fuente de datos: https://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/.
- Consulta: 23 territorios; nivel 46/DIVERSIFICADO; todos los sectores, planes, modalidades y estados.
- Fecha de entrega: 23 de julio de 2026.
- Cobertura de la extracción: {len(clean):,} registros, 17 campos de origen, {len(clean.columns)} columnas finales. No es un censo de personas, alumnos o edificios.
- Catálogo territorial: dominio codmuni_i del servicio público INAB; procedencia, fecha y 340 municipios en data/catalogos/fuente.json y municipios.csv.
- Versión: 1.0.0; codificación UTF-8, separador coma y encabezado. Los textos entre comillas y las comas se escapan mediante el estándar CSV.
- Ausencia: campo vacío. Se recomienda keep_default_na=False al leer para distinguirlo de categorías expresas como SIN JORNADA.
- Identificadores: leer CODIGO, DISTRITO, TELEFONO, ZONA_CAPITAL y CODIGO_MUNICIPIO como texto; no convertirlos a números.

## Transformaciones, validación y decisiones

Las correcciones se detallan en reports/transformaciones_detalle.csv y se resumen por variable y regla en reports/registro_transformaciones.csv. Se modificaron {final['celdas_modificadas']:,} celdas y se conservaron todas las filas. No se imputaron teléfonos, directores, supervisores ni distritos.

Las {final['pruebas']} reglas automáticas de la entrega verifican tipos, códigos, unicidad, espacios, teléfono, distritos, categorías y coherencia territorial. Las ausencias documentadas son permitidas; un contrato de formato no certifica que un teléfono esté activo. El resultado está en reports/validacion.json.

Se identificaron {final['pares_candidatos']:,} pares de posibles coincidencias con RapidFuzz dentro de municipio. Cada par tiene decisión y justificación. La semejanza no prueba que un código sea un duplicado; se conservan servicios legítimos y se señalan los casos que requieren revisión humana. No se eliminaron ni fusionaron registros.

## Reproducibilidad

La entrega incluye los 23 CSV crudos y el catálogo usado. Para reproducir los resultados sin acceder a la red: python -m src.pipeline, python -m src.documentacion y python -m src.pdf. El proceso verifica las sumas SHA-256 antes y después. Una descarga futura puede cambiar y se guarda en una carpeta diferente. Los comandos completos y las dependencias probadas están en README.md.
'''
    book = "# Libro de códigos\n\nProyecto 1 · Obtención y limpieza de datos\n\nEstablecimientos educativos de Guatemala · Nivel Diversificado\n\n" + metadata + "\n" + original + "\n" + derived
    (root / "docs/LIBRO_DE_CODIGOS.md").write_text(book, encoding="utf-8")
    print(f"Libro de códigos: {len(clean.columns)} variables documentadas")


if __name__ == "__main__":
    generar(Path(__file__).resolve().parents[1])
