"""Transformaciones conservadoras con trazabilidad por celda y sin imputación."""
from __future__ import annotations

import re

import pandas as pd

from .comun import catalogos, clave, texto
from .diagnostico import MARCADORES

ORIGINALES = ["DISTRITO", "DEPARTAMENTO", "MUNICIPIO", "ESTABLECIMIENTO", "DIRECCION", "TELEFONO", "SUPERVISOR", "DIRECTOR"]


def telefono(value):
    original = texto(value)
    if original in MARCADORES:
        return "", "AUSENTE", ""
    s = re.sub(r"(?:\+502|\(502\))\s*", "", original)
    # Solo se unen grupos 4+4; no se completan dígitos ni rangos abreviados.
    s = re.sub(r"(?<!\d)(\d{4})[ -](\d{4})(?!\d)", r"\1\2", s)
    nums = []
    for number in re.findall(r"(?<!\d)\d{8}(?!\d)", s):
        if len(set(number)) > 1 and number not in nums:
            nums.append(number)
    rest = re.sub(r"(?<!\d)\d{8}(?!\d)", " ", s)
    rest = re.sub(r"[,;/\-\s]+|\bY\b", " ", rest).strip()
    if not nums:
        return "", "INVALIDO", original
    state = "PARCIAL" if rest else "MULTIPLE" if len(nums) > 1 else "VALIDO"
    return ";".join(nums), state, rest


def limpiar(raw, root):
    df = raw.copy()
    for col in ORIGINALES:
        df[col + "_ORIGINAL"] = raw[col]
    for col in raw:
        df[col] = raw[col].map(texto).astype("string")
    for col in ["DISTRITO", "ESTABLECIMIENTO", "DIRECCION", "TELEFONO", "SUPERVISOR", "DIRECTOR"]:
        df.loc[df[col].isin(MARCADORES), col] = ""
    incomplete = df.DISTRITO.str.fullmatch(r"\d{2}-", na=False)
    df["ESTADO_DISTRITO"] = "VALIDO"
    df.loc[df.DISTRITO.eq(""), "ESTADO_DISTRITO"] = "AUSENTE"
    df.loc[incomplete, "ESTADO_DISTRITO"] = "INCOMPLETO"
    df.loc[incomplete, "DISTRITO"] = ""
    unexpected = df.DISTRITO.ne("") & ~df.DISTRITO.str.fullmatch(r"\d{2}-\d{3}|\d{2}-\d{2}-\d{4}", na=False)
    df.loc[unexpected, "ESTADO_DISTRITO"] = "INVALIDO"
    df.loc[unexpected, "DISTRITO"] = ""
    # Abreviaturas inequívocas; no se retiran guiones de casas ni decimales.
    df["DIRECCION"] = df.DIRECCION.str.replace(r"\bAV(?:DA|EN)?\.\s*", "AVENIDA ", regex=True).str.replace(r"\bKM\.\s*", "KM ", regex=True).map(texto)
    phones = [telefono(x) for x in raw.TELEFONO]
    df["TELEFONO"] = [x[0] for x in phones]
    df["TELEFONO_LIMPIO"] = df.TELEFONO
    df["ESTADO_TELEFONO"] = [x[1] for x in phones]
    df["TELEFONO_NOTAS"] = [x[2] for x in phones]
    municipalities, categories = catalogos(root)
    muni = municipalities.set_index("codigo_municipio").to_dict("index")
    aliases = __import__('json').loads((root / "data/catalogos/equivalencias_municipios.json").read_text(encoding="utf-8"))
    df["ZONA_CAPITAL"] = ""
    df["CODIGO_MUNICIPIO"] = ""
    df["ESTADO_GEOGRAFIA"] = "VALIDO"
    for i, row in df.iterrows():
        match = re.fullmatch(r"(\d{2})-(\d{2})-\d{4}-46", row.CODIGO)
        code = match[1] + match[2] if match else ""
        capital = bool(match and match[1] == "00")
        if capital:
            code = "0101"
            zone = re.fullmatch(r"ZONA (\d{1,2})", row.MUNICIPIO)
            if not zone or int(zone[1]) != int(match[2]):
                df.at[i, "ESTADO_GEOGRAFIA"] = "REVISAR"
                continue
            df.at[i, "ZONA_CAPITAL"] = zone[1]
        official = muni.get(code)
        accepted = {clave(official["nombre"])} if official else set()
        accepted |= {clave(x) for x in aliases.get(code, [])}
        dept_ok = official and (capital and row.DEPARTAMENTO == "CIUDAD CAPITAL" or clave(row.DEPARTAMENTO) == clave(official["departamento"]))
        if official and dept_ok and (capital or clave(row.MUNICIPIO) in accepted):
            df.at[i, "DEPARTAMENTO"] = official["departamento"]
            df.at[i, "MUNICIPIO"] = official["nombre"]
            df.at[i, "CODIGO_MUNICIPIO"] = code
        else:
            df.at[i, "ESTADO_GEOGRAFIA"] = "REVISAR"
    # Catálogos explícitos: solo se igualan acentos/caso/espacios cuando existe
    # una correspondencia única. SIN JORNADA y SIN ESPECIFICAR se conservan.
    for col, values in categories.items():
        canonical = {clave(x): x for x in values}
        df[col] = df[col].map(lambda x: canonical.get(clave(x), x))
    for col in df:
        df[col] = df[col].astype("string")
    audits = []
    reasons = {"DISTRITO": "No completar códigos; mantener formatos válidos y marcar incompletos.",
               "DEPARTAMENTO": "Catálogo territorial oficial; capital pertenece a Guatemala.",
               "MUNICIPIO": "Catálogo por código y equivalencias documentadas; separar zona capital.",
               "TELEFONO": "Separar números válidos de ocho dígitos; conservar original y pendientes.",
               "DIRECCION": "Normalizar espacios y abreviaturas inequívocas sin alterar números."}
    for col in raw:
        changed = raw[col].ne(df[col])
        for i in raw.index[changed]:
            audits.append({"fila_origen": int(i), "codigo": raw.at[i, "CODIGO"], "variable": col,
                           "antes": raw.at[i, col], "despues": df.at[i, col],
                           "regla": reasons.get(col, "Unicode NFC, espacios, mayúsculas y marcadores explícitos de ausencia; sin imputar datos.")})
    audit = pd.DataFrame(audits, columns=["fila_origen", "codigo", "variable", "antes", "despues", "regla"])
    return df, audit
