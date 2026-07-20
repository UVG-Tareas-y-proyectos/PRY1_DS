"""Descarga las 23 consultas oficiales de Diversificado sin limpiar sus valores."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/"
PREFIX = "_ctl0:ContentPlaceHolder1:"
COLUMNAS = ["CODIGO", "DISTRITO", "DEPARTAMENTO", "MUNICIPIO", "ESTABLECIMIENTO",
            "DIRECCION", "TELEFONO", "SUPERVISOR", "DIRECTOR", "NIVEL", "SECTOR",
            "AREA", "STATUS", "MODALIDAD", "JORNADA", "PLAN", "DEPARTAMENTAL"]


def formulario(soup):
    data = {x["name"]: x.get("value", "") for x in soup.select("input[type=hidden]")}
    for select in soup.select("select"):
        option = select.select_one("option[selected]") or select.select_one("option")
        # El municipio se carga mediante AJAX. No enviar un valor vacío que el
        # servidor no reconoce como opción válida (causa un HTTP 500).
        if option is not None:
            data[select["name"]] = option.get("value", "")
    for x in soup.select("input[type=text]"):
        data[x["name"]] = x.get("value", "")
    return data


def descargar(destino: Path, html_dir: Path | None = None):
    destino.mkdir(parents=True, exist_ok=True)
    if (destino / "manifest.json").exists():
        raise FileExistsError("El destino ya tiene una extracción; use otro directorio para conservarla.")
    session = requests.Session()
    session.headers["User-Agent"] = "Proyecto-academico-CC3084/1.0 (consulta publica MINEDUC)"
    response = session.get(URL, timeout=60)
    response.raise_for_status()
    initial = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
    options = initial.find("select", attrs={"name": PREFIX + "cmbDepartamento"})
    territorios = [(o["value"], o.get_text()) for o in options.find_all("option")
                   if o.get("value", "").isdigit()]
    if len(territorios) != 23:
        raise ValueError(f"Se esperaban 23 consultas territoriales, se encontraron {len(territorios)}")
    manifest = {"fuente": URL, "nivel": "DIVERSIFICADO", "filtros_restantes": "TODOS",
                "fecha_entrega": "2026-07-23",
                "nota": "Exportación de consultas territoriales del MINEDUC con nivel DIVERSIFICADO.",
                "archivos": []}
    for index, (codigo, nombre) in enumerate(territorios):
        # Una página inicial fresca por consulta conserva la validación ASP.NET.
        if index:
            response = session.get(URL, timeout=60)
            response.raise_for_status()
            initial = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        data = formulario(initial)
        data.update({PREFIX + "cmbDepartamento": codigo, PREFIX + "cmbNivel": "46",
                     PREFIX + "IbtnConsultar.x": "5", PREFIX + "IbtnConsultar.y": "5"})
        for attempt in range(3):
            response = session.post(URL, data=data, timeout=120)
            if response.ok:
                break
            if attempt == 2:
                response.raise_for_status()
            time.sleep(2 ** attempt)
        soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        table = soup.find("table", id="_ctl0_ContentPlaceHolder1_dgResultado")
        if table is None:
            raise ValueError(f"No se encontró la tabla de resultados para {nombre}")
        rows = table.find_all("tr", recursive=False)
        headers = [x.get_text(strip=True) for x in rows[0].find_all("td", recursive=False)][1:]
        if headers != COLUMNAS:
            raise ValueError(f"El esquema cambió en {nombre}: {headers}")
        values = []
        for tr in rows[1:]:
            cells = tr.find_all("td", recursive=False)
            if len(cells) != 18:
                raise ValueError(f"Fila inesperada en {nombre}")
            if tr.get("bgcolor", "").lower() == "gold" and all(not td.get_text().strip() for td in cells):
                continue  # Pie decorativo vacío del DataGrid; no es un registro.
            # NBSP solo representa una celda vacía en el HTML del portal. Los
            # demás espacios, signos, tildes y marcadores se conservan intactos.
            values.append(["" if td.get_text() == "\xa0" else td.get_text() for td in cells[1:]])
        count = soup.find(id="_ctl0_ContentPlaceHolder1_lblPie1")
        if count:
            import re
            match = re.search(r"([\d,]+)\s+Establecimientos", count.get_text())
            if match and int(match[1].replace(",", "")) != len(values):
                raise ValueError(f"La tabla está incompleta en {nombre}")
        path = destino / f"{codigo}_diversificado.csv"
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(COLUMNAS)
            writer.writerows(values)
        if html_dir:
            html_dir.mkdir(parents=True, exist_ok=True)
            (html_dir / f"{codigo}.html").write_bytes(response.content)
        manifest["archivos"].append({"archivo": path.name, "codigo_territorio": codigo,
                                     "territorio": nombre, "registros": len(values),
                                     "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                     "fecha_entrega": "2026-07-23"})
        print(f"{codigo} {nombre}: {len(values)} registros", flush=True)
        time.sleep(0.3)
    manifest["registros"] = sum(x["registros"] for x in manifest["archivos"])
    (destino / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destino", type=Path, default=Path("data/raw"))
    parser.add_argument("--html-dir", type=Path)
    args = parser.parse_args()
    descargar(args.destino, args.html_dir)
