"""Guarda un catálogo territorial oficial independiente de los datos educativos."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pandas as pd
import requests

from .comun import guardar_csv, guardar_json

URL_INAB = "https://sig.inab.gob.gt/server/rest/services/Hosted/service_fff38eb7eac44746a91435fc53d2b5d1/FeatureServer/7"
DEPARTAMENTOS = dict(enumerate(["GUATEMALA", "EL PROGRESO", "SACATEPÉQUEZ", "CHIMALTENANGO", "ESCUINTLA", "SANTA ROSA", "SOLOLÁ", "TOTONICAPÁN", "QUETZALTENANGO", "SUCHITEPÉQUEZ", "RETALHULEU", "SAN MARCOS", "HUEHUETENANGO", "QUICHÉ", "BAJA VERAPAZ", "ALTA VERAPAZ", "PETÉN", "IZABAL", "ZACAPA", "CHIQUIMULA", "JALAPA", "JUTIAPA"], start=1))


def descargar_catalogo(root: Path):
    target = root / "data/catalogos"
    target.mkdir(parents=True, exist_ok=True)
    if (target / "municipios.csv").exists():
        raise FileExistsError("El catálogo ya existe; conserve la versión antes de actualizarlo")
    response = requests.get(URL_INAB, params={"f": "pjson"}, timeout=60)
    response.raise_for_status()
    data = response.json()
    fields = {f["name"]: f for f in data["fields"]}
    domain = fields["codmuni_i"]["domain"]["codedValues"]
    if len(domain) != 340:
        raise ValueError("El dominio oficial no tiene los 340 municipios esperados")
    rows = []
    for item in domain:
        code = item["code"].removeprefix("gt-")
        rows.append({"codigo_municipio": code, "codigo_departamento": code[:2],
                     "departamento": DEPARTAMENTOS[int(code[:2])], "nombre": item["name"]})
    guardar_csv(target / "municipios.csv", pd.DataFrame(rows).sort_values("codigo_municipio"))
    guardar_json(target / "fuente.json", {"url": URL_INAB + "?f=pjson", "institucion": "Instituto Nacional de Bosques (INAB)",
        "campo": "codmuni_i", "municipios": 340, "fecha_entrega": "2026-07-23",
        "sha256_respuesta": hashlib.sha256(response.content).hexdigest(),
        "nota": "Dominio territorial externo. Las variantes de nombres del MINEDUC se documentan por separado."})


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    descargar_catalogo(p.parse_args().root)
