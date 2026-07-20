"""Funciones compartidas y lectura que conserva identificadores y valores vacíos."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

from .obtener import COLUMNAS


def texto(value: str) -> str:
    value = unicodedata.normalize("NFC", str(value))
    value = "".join(c for c in value if unicodedata.category(c) != "Cf")
    return re.sub(r"\s+", " ", value).strip().upper()


def clave(value: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", texto(value))
                   if not unicodedata.combining(c))


def guardar_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def guardar_csv(path: Path, df: pd.DataFrame):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8", lineterminator="\n")


def cargar(root: Path) -> pd.DataFrame:
    folder = root / "data/raw"
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    if len(manifest["archivos"]) != 23:
        raise ValueError("La extracción no tiene las 23 consultas territoriales")
    frames = []
    for entry in manifest["archivos"]:
        path = folder / entry["archivo"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError(f"Se modificó un archivo crudo: {path.name}")
        df = pd.read_csv(path, dtype="string", keep_default_na=False)
        if list(df.columns) != COLUMNAS or len(df) != entry["registros"]:
            raise ValueError(f"Esquema o número de filas inesperado: {path.name}")
        if not df["DEPARTAMENTO"].map(clave).eq(clave(entry["territorio"])).all():
            raise ValueError(f"La consulta contiene otro territorio: {path.name}")
        frames.append(df)
    result = pd.concat(frames, ignore_index=True)
    if len(result) != manifest["registros"]:
        raise ValueError("El manifiesto y el consolidado no coinciden")
    return result


def catalogos(root: Path):
    muni = pd.read_csv(root / "data/catalogos/municipios.csv", dtype="string", keep_default_na=False)
    cats = json.loads((root / "data/catalogos/categorias.json").read_text(encoding="utf-8"))
    return muni, cats
