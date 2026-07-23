"""Contratos automáticos del CSV limpio; no exige completar información ausente."""
from __future__ import annotations

import re

from .comun import catalogos, clave, texto
from .obtener import COLUMNAS


def validar(raw, clean, root):
    muni, cats = catalogos(root)
    checks = []

    def check(name, condition, detail):
        checks.append({"prueba": name, "aprobada": bool(condition), "detalle": detail})

    check("conservar_registros", len(raw) == len(clean), "No se eliminan servicios sin evidencia documentada.")
    check("conservar_codigos", raw.CODIGO.tolist() == clean.CODIGO.tolist(), "Misma secuencia de códigos y ceros iniciales.")
    check("codigo_formato", clean.CODIGO.str.fullmatch(r"\d{2}-\d{2}-\d{4}-46").all(), "Identificadores de Diversificado.")
    check("codigo_unico", clean.CODIGO.is_unique, "Cada fila representa un código de servicio único.")
    check("sin_duplicados_exactos", not clean[COLUMNAS].duplicated().any(), "Sobre todas las variables originales, ya limpiadas.")
    operational = [c for c in clean if not c.endswith("_ORIGINAL")]
    check("tipos_textuales", all(str(clean[c].dtype).startswith('string') for c in clean), "CSV se importa explícitamente como texto; no se pierden ceros.")
    check("sin_espacios_externos", all(clean[c].eq(clean[c].str.strip()).all() for c in operational), "Se excluyen columnas originales conservadas como evidencia.")
    check("sin_espacios_multiples", not any(clean[c].str.contains(r"\s{2,}").any() for c in operational), "Texto operativo uniforme.")
    check("unicode_y_mayusculas", all(clean[c].map(texto).eq(clean[c]).all() for c in operational), "NFC, mayúsculas y ausencia de caracteres invisibles.")
    check("telefono_formato", (clean.TELEFONO.eq("") | clean.TELEFONO.str.fullmatch(r"\d{8}(;\d{8})*")).all(), "Cero o más números completos; separador punto y coma.")
    check("telefono_sin_inventar", clean.TELEFONO.eq(clean.TELEFONO_LIMPIO).all(), "Alias explícito del campo limpio.")
    check("distrito_formato", (clean.DISTRITO.eq("") | clean.DISTRITO.str.fullmatch(r"\d{2}-\d{3}|\d{2}-\d{2}-\d{4}")).all(), "Se admiten los dos sistemas de códigos documentados.")
    lookup = muni.set_index("codigo_municipio").to_dict("index")
    valid = clean.apply(lambda r: r.CODIGO_MUNICIPIO in lookup and r.MUNICIPIO == lookup[r.CODIGO_MUNICIPIO]["nombre"] and r.DEPARTAMENTO == lookup[r.CODIGO_MUNICIPIO]["departamento"], axis=1)
    check("catalogo_municipio_departamento", valid.all(), "Código, nombre y departamento coinciden con catálogo oficial INAB.")
    check("geografia_sin_pendientes", clean.ESTADO_GEOGRAFIA.eq("VALIDO").all(), "Equivalencias revisadas por código; capital y zona separadas.")
    check("departamental_coherente", clean.apply(lambda r: clave(r.DEPARTAMENTAL) == clave(r.DEPARTAMENTO) or clave(r.DEPARTAMENTO) == 'GUATEMALA' and clave(r.DEPARTAMENTAL) in {'GUATEMALA NORTE', 'GUATEMALA SUR', 'GUATEMALA ORIENTE', 'GUATEMALA OCCIDENTE'} or clave(r.DEPARTAMENTO) == 'QUICHE' and clave(r.DEPARTAMENTAL) == 'QUICHE NORTE', axis=1).all(), "La dirección administrativa corresponde al territorio.")
    check("zona_capital_coherente", clean.loc[clean.ZONA_CAPITAL.ne(""), "CODIGO_MUNICIPIO"].eq("0101").all(), "Las zonas de capital pertenecen al municipio de Guatemala.")
    for col, allowed in cats.items():
        check("dominio_" + col.lower(), clean[col].isin(allowed).all(), "Catálogo explícito; no se fusionan categorías administrativas distintas.")
    for col in ["DISTRITO", "ESTABLECIMIENTO", "DIRECCION", "SUPERVISOR", "DIRECTOR"]:
        check("sin_marcadores_" + col.lower(), not clean[col].isin({"N/A", "NULL", "SIN DATO", "S/D", "-", "--", "---", "."}).any(), "La ausencia se representa mediante campo vacío.")
    return {"aprobada": all(x["aprobada"] for x in checks), "total": len(checks), "pruebas": checks}
