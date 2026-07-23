"""Reproduce diagnóstico, limpieza, candidatos, validación e informe final."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .consolidar import ejecutar as consolidar
from .comun import cargar, guardar_csv, guardar_json
from .diagnostico import diagnosticar, metricas
from .duplicados import detectar
from .limpieza import limpiar
from .obtener import COLUMNAS
from .validacion import validar


def tabla(df):
    def cell(x):
        if isinstance(x, float) and x.is_integer():
            x = int(x)
        return str(x).replace("|", "\\|").replace("\n", " ")
    return "| " + " | ".join(df.columns) + " |\n| " + " | ".join(["---"] * len(df.columns)) + " |\n" + "\n".join("| " + " | ".join(map(cell, row)) + " |" for row in df.itertuples(index=False, name=None))


def ejecutar(root):
    raw, before = consolidar(root)
    clean, audit = limpiar(raw, root)
    candidates = detectar(clean)
    checks = validar(raw, clean, root)
    guardar_csv(root / "data/processed/diversificado_limpio.csv", clean)
    guardar_csv(root / "reports/transformaciones_detalle.csv", audit)
    summary = audit.groupby(["variable", "regla"], sort=True).agg(registros_afectados=("codigo", "nunique"), celdas_modificadas=("codigo", "size")).reset_index()
    guardar_csv(root / "reports/registro_transformaciones.csv", summary)
    guardar_csv(root / "reports/duplicados_parciales.csv", candidates)
    guardar_json(root / "reports/validacion.json", checks)
    after = diagnosticar(clean[COLUMNAS], root, root / "reports/diagnostico_limpio")
    comparative = pd.DataFrame([{"metrica": k, "antes": before[k], "despues": after[k]} for k in before])
    guardar_csv(root / "reports/calidad_antes_despues.csv", comparative)
    pending = clean.loc[clean.ESTADO_TELEFONO.isin(["INVALIDO", "PARCIAL"]) | clean.ESTADO_DISTRITO.isin(["INCOMPLETO", "INVALIDO"]) | clean.ESTADO_GEOGRAFIA.ne("VALIDO"), ["CODIGO", "DISTRITO_ORIGINAL", "ESTADO_DISTRITO", "TELEFONO_ORIGINAL", "TELEFONO", "ESTADO_TELEFONO", "ESTADO_GEOGRAFIA"]]
    guardar_csv(root / "reports/casos_para_revision.csv", pending)
    guardar_json(root / "reports/resumen_final.json", {
        "version": "1.0.0", "registros_crudos": len(raw), "registros_limpios": len(clean),
        "variables_originales": len(COLUMNAS), "variables_limpias": len(clean.columns),
        "celdas_modificadas": len(audit), "registros_modificados": int(audit.codigo.nunique()),
        "pares_candidatos": len(candidates), "codigos_en_pares": int(pd.concat([candidates.codigo_a, candidates.codigo_b]).nunique()) if len(candidates) else 0,
        "pares_conservar_servicios_distintos": int(candidates.decision.eq("CONSERVAR_SERVICIOS_DISTINTOS").sum()),
        "pares_conservar_para_revision": int(candidates.decision.eq("CONSERVAR_PARA_REVISION").sum()),
        "registros_eliminados": 0, "registros_fusionados": 0,
        "estados_telefono": {str(k): int(v) for k, v in clean.ESTADO_TELEFONO.value_counts().items()},
        "estados_distrito": {str(k): int(v) for k, v in clean.ESTADO_DISTRITO.value_counts().items()},
        "validacion_aprobada": checks["aprobada"], "pruebas": checks["total"]})
    manifest = json.loads((root / "data/raw/manifest.json").read_text(encoding="utf-8"))
    display_comparative = comparative.rename(columns={"metrica": "Métrica", "antes": "Antes", "despues": "Después"}).copy()
    display_comparative["Métrica"] = display_comparative["Métrica"].str.replace("_", " ").str.capitalize()
    display_summary = summary.rename(columns={"variable": "Variable", "regla": "Regla y justificación", "registros_afectados": "Registros", "celdas_modificadas": "Celdas"})
    content = f'''# Informe de calidad de los datos

## Alcance y procedencia

Versión 1.0.0. Fuente: buscador oficial MINEDUC, nivel DIVERSIFICADO y resto de filtros TODOS. Se consolidan {len(raw):,} registros en 17 variables de origen, procedentes de 23 CSV. El manifiesto data/raw/manifest.json contiene los datos de procedencia, filtros y sumas SHA-256.

## Comparación en las mismas 17 variables

{tabla(display_comparative)}

El CSV final tiene {len(clean.columns)} columnas: 17 campos de origen y {len(clean.columns)-17} columnas de trazabilidad, validación y ubicación. La tabla anterior usa las mismas 17 columnas antes y después para evitar atribuir a la limpieza los vacíos añadidos por campos derivados opcionales.

Los valores faltantes pueden aumentar al convertir marcadores y teléfonos o distritos incompletos en campos vacíos. Esto hace explícita la ausencia, sin inventar información. Las columnas originales y el registro por celda permiten recuperar cada valor.

## Registro de transformaciones

{tabla(display_summary)}

Se modificaron {len(audit):,} celdas en {audit.codigo.nunique():,} servicios. Los conteos de celdas no equivalen a personas ni establecimientos físicos. El detalle incluye código, variable, valor anterior, valor posterior y justificación.

## Duplicados exactos y parciales

Duplicados exactos después: {after['duplicados_exactos']}. Se identificaron {len(candidates):,} pares candidatos mediante token_sort_ratio de RapidFuzz dentro de municipio: umbral 97, o 90 con dirección/teléfono coincidente. Se conservan todos los códigos. Diferencias de jornada o plan justifican servicios distintos; los demás pares se conservan para revisión humana. No se afirma haber realizado una revisión manual inexistente. Consulte reports/duplicados_parciales.csv para la decisión y justificación de cada par.

No se eliminaron ni fusionaron filas. La fuente MINEDUC explica que un centro puede tener múltiples códigos según nivel, plan o jornada. Los nombres similares no prueban duplicación.

## Validación y limitaciones

Resultado: {'APROBADO' if checks['aprobada'] else 'CON ERRORES'}; {sum(x['aprobada'] for x in checks['pruebas'])}/{checks['total']} reglas aprobadas. El registro ejecutable está en reports/validacion.json.

Persisten ausencias reales de la fuente y contactos incompletos: {len(pending):,} registros requieren revisión de teléfono, distrito o geografía. Se documentan sin imputación en reports/casos_para_revision.csv. Un teléfono con ocho dígitos tiene formato válido; no demuestra que esté activo ni que pertenezca al establecimiento. Se respetan los dos formatos de distrito porque no se dispone de un catálogo público que justifique su unificación. El catálogo INAB comprueba municipio y departamento; DEPARTAMENTAL se valida con las regiones administrativas observadas en el MINEDUC y su correspondencia territorial.

La reproducibilidad local usa los CSV y catálogos versionados. Una nueva consulta a la web puede cambiar y debe guardarse en otra carpeta. Los datos de procedencia están en los manifiestos.
'''
    (root / "docs/INFORME_CALIDAD.md").write_text(content, encoding="utf-8")
    # Comprueba que el proceso no modificó las fuentes.
    cargar(root)
    if not checks["aprobada"]:
        failed = [x["prueba"] for x in checks["pruebas"] if not x["aprobada"]]
        raise ValueError("Falló la validación: " + ", ".join(failed))
    return clean


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    result = ejecutar(parser.parse_args().root)
    print(f"Proceso completo: {len(result)} registros, {len(result.columns)} variables")
