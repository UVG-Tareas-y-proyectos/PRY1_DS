"""Candidatos parciales por similitud; nunca elimina servicios automáticamente."""
from __future__ import annotations

import numpy as np
import pandas as pd
from rapidfuzz import fuzz, process

from .comun import clave

COLUMNAS_PARES = ["codigo_a", "codigo_b", "similitud_nombre", "misma_direccion", "mismo_telefono",
                  "jornada_a", "jornada_b", "plan_a", "plan_b", "decision", "justificacion"]


def detectar(df):
    pairs = []
    # Comparar dentro de municipio evita emparejar colegios de territorios distintos.
    for _, block in df.groupby("CODIGO_MUNICIPIO", sort=True):
        block = block[block.ESTABLECIMIENTO.ne("")].reset_index(drop=True)
        names = block.ESTABLECIMIENTO.map(clave).tolist()
        if len(names) < 2:
            continue
        scores = process.cdist(names, names, scorer=fuzz.token_sort_ratio,
                               score_cutoff=90, dtype=np.float32, workers=1)
        a, b = np.where(np.triu(scores, k=1) >= 90)
        for i, j in zip(a.tolist(), b.tolist()):
            left, right = block.iloc[i], block.iloc[j]
            same_address = bool(left.DIRECCION and clave(left.DIRECCION) == clave(right.DIRECCION))
            same_phone = bool(set(left.TELEFONO.split(";")) & set(right.TELEFONO.split(";")) - {""})
            if scores[i, j] < 97 and not (same_address or same_phone):
                continue
            distinct_service = left.JORNADA != right.JORNADA or left.PLAN != right.PLAN
            reason = ("Códigos distintos y distinta jornada o plan: servicios educativos distintos."
                      if distinct_service else "Códigos distintos; similitud no demuestra duplicación. Conservar; candidato para revisión humana.")
            pairs.append({"codigo_a": left.CODIGO, "codigo_b": right.CODIGO,
                          "similitud_nombre": round(float(scores[i, j]), 2), "misma_direccion": same_address,
                          "mismo_telefono": same_phone, "jornada_a": left.JORNADA, "jornada_b": right.JORNADA,
                          "plan_a": left.PLAN, "plan_b": right.PLAN,
                          "decision": "CONSERVAR_SERVICIOS_DISTINTOS" if distinct_service else "CONSERVAR_PARA_REVISION",
                          "justificacion": reason})
    return pd.DataFrame(pairs, columns=COLUMNAS_PARES)
