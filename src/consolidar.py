"""Ejecuta únicamente consolidación y diagnóstico; no realiza limpieza."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


from .comun import cargar, guardar_csv
from .diagnostico import diagnosticar


def ejecutar(root):
    raw = cargar(root)
    guardar_csv(root / "data/interim/diversificado_crudo.csv", raw)
    metrics = diagnosticar(raw, root, root / "reports/diagnostico")
    return raw, metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    _, metrics = ejecutar(args.root)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
