"""Diagnóstico previo a cualquier transformación del conjunto crudo."""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from .comun import catalogos, clave, guardar_csv, guardar_json, texto

MARCADORES = {"", "N/A", "NA", "NULL", "NONE", "SIN DATO", "SIN DATOS", "S/D", "-", "--", "---", "."}
CATEGORICAS = ["NIVEL", "SECTOR", "AREA", "STATUS", "MODALIDAD", "JORNADA", "PLAN", "DEPARTAMENTO", "MUNICIPIO", "DEPARTAMENTAL"]


def perfil(df):
    rows = []
    for col in df:
        s = df[col].fillna("").astype("string")
        vacios = s.eq("")
        faltantes = s.map(texto).isin(MARCADORES)
        rows.append({"variable": col, "tipo_lectura": str(s.dtype),
                     "tipo_semantico": "identificador_textual" if col in {"CODIGO", "DISTRITO", "TELEFONO"} else "texto",
                     "vacios": int(vacios.sum()), "faltantes_con_marcadores": int(faltantes.sum()),
                     "porcentaje_faltantes": round(100 * float(faltantes.mean()), 4),
                     "valores_unicos_con_vacio": int(s.nunique(dropna=False)),
                     "espacios_externos": int(s.ne(s.str.strip()).sum()),
                     "espacios_multiples": int(s.str.contains(r"\s{2,}", regex=True).sum()),
                     "caracteres_invisibles": int(s.map(lambda x: any(__import__('unicodedata').category(c) == 'Cf' for c in x)).sum()),
                     "variantes_por_mayusculas_y_espacios": int(s.nunique() - s.map(texto).nunique())})
    return pd.DataFrame(rows)


def metricas(df):
    p = perfil(df)
    phone = df["TELEFONO"].fillna("")
    return {"registros": len(df), "variables": len(df.columns),
            "celdas": int(df.size), "vacios": int(df.fillna("").eq("").sum().sum()),
            "faltantes_con_marcadores": int(p.faltantes_con_marcadores.sum()),
            "porcentaje_faltantes_con_marcadores": round(100 * int(p.faltantes_con_marcadores.sum()) / df.size, 4),
            "variables_con_faltantes": int((p.faltantes_con_marcadores > 0).sum()),
            "variables_con_vacios": int((p.vacios > 0).sum()),
            "porcentaje_vacios": round(100 * int(df.fillna("").eq("").sum().sum()) / df.size, 4),
            "duplicados_exactos": int(df.duplicated().sum()),
            "codigos_unicos": int(df.CODIGO.nunique()),
            "variables_con_formato_inconsistente": int(((p.espacios_externos + p.espacios_multiples + p.caracteres_invisibles + p.variantes_por_mayusculas_y_espacios) > 0).sum()),
            "telefonos_fuera_formato": int((phone.ne("") & ~phone.str.fullmatch(r"\d{8}(;\d{8})*", na=False)).sum()),
            "codigos_fuera_formato": int((~df.CODIGO.str.fullmatch(r"\d{2}-\d{2}-\d{4}-46", na=False)).sum()),
            "distritos_incompletos": int(df.DISTRITO.str.fullmatch(r"\d{2}-", na=False).sum()),
            "municipios_distintos": int(df.MUNICIPIO.nunique()),
            "tipos_incorrectos": sum(not isinstance(df[c].dtype, pd.StringDtype) for c in df)}


def diagnosticar(df, root: Path, destino: Path):
    destino.mkdir(parents=True, exist_ok=True)
    guardar_csv(destino / "perfil_variables.csv", perfil(df))
    guardar_json(destino / "resumen.json", metricas(df))
    guardar_csv(destino / "por_territorio.csv", df.groupby("DEPARTAMENTO", dropna=False).size().rename("registros").reset_index())
    domains = []
    for col in CATEGORICAS:
        for value, count in df[col].value_counts(dropna=False).items():
            domains.append({"variable": col, "valor": value, "registros": int(count)})
    guardar_csv(destino / "categorias_observadas.csv", pd.DataFrame(domains))
    normalized = df[["ESTABLECIMIENTO", "DIRECCION", "TELEFONO"]].map(texto)
    guardar_json(destino / "duplicados_iniciales.json", {
        "exactos": int(df.duplicated().sum()), "codigos_repetidos": int(df.CODIGO.duplicated().sum()),
        "filas_adicionales_mismo_nombre_direccion_telefono": int(normalized.duplicated().sum()),
        "nota": "Una coincidencia no autoriza eliminar servicios con distinto código, jornada o plan."})
    guardar_csv(destino / "codigos_repetidos.csv", df[df.CODIGO.duplicated(keep=False)])
    guardar_csv(destino / "duplicados_exactos.csv", df[df.duplicated(keep=False)])
    muni, cats = catalogos(root)
    allowed_muni = set(muni.nombre.map(clave))
    allowed_dept = set(muni.departamento.map(clave)) | {"CIUDAD CAPITAL"}
    invalid = []
    for col in CATEGORICAS:
        allowed = allowed_muni if col == "MUNICIPIO" else allowed_dept if col == "DEPARTAMENTO" else set(map(clave, cats[col]))
        for value, count in df[col].value_counts().items():
            # Zonas de capital se reportan como una diferencia de semántica.
            if clave(value) not in allowed:
                invalid.append({"variable": col, "valor": value, "registros": int(count),
                                "problema": "zona_capital" if col == "MUNICIPIO" and re.fullmatch(r"ZONA \d+", value) else "requiere_catalogo_o_equivalencia"})
    guardar_csv(destino / "valores_fuera_catalogo.csv", pd.DataFrame(invalid, columns=["variable", "valor", "registros", "problema"]))
    return metricas(df)
