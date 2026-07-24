"""Genera los PDF con la portada y los estilos académicos de la UVG."""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from lxml import etree as E
from pypdf import PdfReader, PdfWriter

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML = "http://www.w3.org/XML/1998/namespace"


def tag(name):
    return f"{{{W}}}{name}"


def child(parent, name):
    result = parent.find(tag(name))
    return result if result is not None else E.SubElement(parent, tag(name))


def scrub_ids(element):
    for node in element.iter():
        for key in list(node.attrib):
            if key.endswith(("}paraId", "}textId")):
                del node.attrib[key]


def set_runs(paragraph, text, bold=False):
    first = paragraph.find(tag("r"))
    old = first.find(tag("rPr")) if first is not None else None
    proto = deepcopy(old) if old is not None else E.Element(tag("rPr"))
    for node in list(paragraph):
        if node.tag != tag("pPr"):
            paragraph.remove(node)
    for index, token in enumerate(re.split(r"\*\*(.*?)\*\*", text)):
        if not token:
            continue
        run = E.SubElement(paragraph, tag("r"))
        properties = deepcopy(proto)
        child(properties, "color").set(tag("val"), "000000")
        if bold or index % 2:
            child(properties, "b").set(tag("val"), "1")
        run.append(properties)
        for number, line in enumerate(token.replace("`", "").split("\n")):
            if number:
                E.SubElement(run, tag("br"))
            node = E.SubElement(run, tag("t"))
            node.set(f"{{{XML}}}space", "preserve")
            node.text = line


class AcademicDocument:
    def __init__(self, template, title):
        with ZipFile(template) as source:
            self.parts = {name: source.read(name) for name in source.namelist()}
        self.xml = E.fromstring(self.parts["word/document.xml"])
        self.body = self.xml.find(tag("body"))
        paragraphs = self.body.findall(tag("p"))
        self.heading_pattern = deepcopy(paragraphs[7])
        self.text_pattern = deepcopy(paragraphs[8])
        self.table_pattern = deepcopy(self.body.find(tag("tbl")))
        self.section = deepcopy(self.body.find(tag("sectPr")))
        cover = [deepcopy(p) for p in paragraphs[:7]]
        set_runs(cover[4], "Proyecto 1\n" + title, True)
        properties = child(cover[4], "pPr")
        child(properties, "pStyle").set(tag("val"), "Title")
        child(properties, "spacing").set(tag("after"), "1250")
        borders = child(properties, "pBdr")
        for side in ["top", "left", "bottom", "right", "between"]:
            child(borders, side).set(tag("val"), "nil")
        set_runs(cover[5], "Ihan Marroquin - 23108\nDiego Patzan - 23525\nMilton Polanco - 23471")
        set_runs(cover[6], "GUATEMALA, 23 de julio del 2026", True)
        for node in list(self.body):
            self.body.remove(node)
        self.body.extend(cover)
        self.first_body = True
        self.group = []

    def flush_group(self):
        for i, p in enumerate(self.group):
            properties = child(p, "pPr")
            child(properties, "keepNext").set(tag("val"), "1" if i < len(self.group) - 1 else "0")
            child(properties, "keepLines").set(tag("val"), "1")
        self.group = []

    def paragraph(self, text, heading=0):
        if heading:
            self.flush_group()
        p = deepcopy(self.heading_pattern if heading else self.text_pattern)
        scrub_ids(p)
        set_runs(p, text, bool(heading))
        properties = child(p, "pPr")
        if heading:
            child(properties, "pStyle").set(tag("val"), "Heading2" if heading >= 3 else "Heading1")
        if self.first_body:
            child(properties, "pageBreakBefore").set(tag("val"), "1")
            self.first_body = False
        self.body.append(p)
        if heading >= 3 or self.group:
            self.group.append(p)

    def table(self, rows):
        self.flush_group()
        table = deepcopy(self.table_pattern)
        scrub_ids(table)
        count = len(rows[0])
        widths = [5040, 2160, 2160] if count == 3 else [2300, 4060, 1500, 1500] if count == 4 else [9360 // count] * count
        old_rows = table.findall(tag("tr"))
        prototypes = [deepcopy(old_rows[0]), deepcopy(old_rows[1])]
        for tr in old_rows:
            table.remove(tr)
        grid = child(table, "tblGrid")
        for column in list(grid):
            grid.remove(column)
        for width in widths:
            E.SubElement(grid, tag("gridCol")).set(tag("w"), str(width))
        for i, values in enumerate(rows):
            tr = deepcopy(prototypes[0 if i == 0 else 1])
            properties = child(tr, "trPr")
            child(properties, "cantSplit")
            if i == 0:
                child(properties, "tblHeader")
            sample = deepcopy(tr.find(tag("tc")))
            for tc in list(tr.findall(tag("tc"))):
                tr.remove(tc)
            for j, value in enumerate(values):
                tc = deepcopy(sample)
                cp = child(tc, "tcPr")
                node = child(cp, "tcW")
                node.set(tag("type"), "dxa")
                node.set(tag("w"), str(widths[j]))
                child(cp, "vAlign").set(tag("val"), "center")
                sample_p = tc.find(tag("p"))
                p = deepcopy(sample_p if sample_p is not None else self.text_pattern)
                for node in list(tc):
                    if node.tag != tag("tcPr"):
                        tc.remove(node)
                set_runs(p, value.replace("\\|", "|"), i == 0)
                pp = child(p, "pPr")
                child(pp, "keepNext").set(tag("val"), "0")
                child(pp, "jc").set(tag("val"), "center" if j and re.fullmatch(r"-?[\d,.%]+", value) else "left")
                tc.append(p)
                tr.append(tc)
            table.append(tr)
        self.body.append(table)

    def markdown(self, text):
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            if line.startswith("| "):
                rows = []
                while i < len(lines) and lines[i].startswith("|"):
                    values = [v.strip() for v in re.split(r"(?<!\\)\|", lines[i].strip().strip("|"))]
                    if not all(re.fullmatch(r":?-+:?", v) for v in values):
                        rows.append(values)
                    i += 1
                self.table(rows)
                continue
            if line.startswith("# "):
                i += 1
                continue
            if line.startswith("### "):
                self.paragraph(line[4:], 3)
            elif line.startswith("## "):
                self.paragraph(line[3:], 2)
            else:
                value = line.removeprefix("- ")
                while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(("#", "|", "- ")):
                    i += 1
                    value += " " + lines[i].strip()
                self.paragraph(value)
            i += 1
        self.flush_group()

    def save(self, path):
        self.body.append(self.section)
        # Mantener el orden de propiedades definido por OOXML para Word.
        sequences = {
            "pPr": "pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr suppressLineNumbers pBdr shd tabs suppressAutoHyphens kinsoku wordWrap overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi adjustRightInd snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc textDirection textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange",
            "rPr": "rStyle rFonts b bCs i iCs caps smallCaps strike dstrike outline shadow emboss imprint noProof snapToGrid vanish webHidden color spacing w kern position sz szCs highlight u effect bdr shd fitText vertAlign rtl cs em lang eastAsianLayout specVanish oMath rPrChange",
            "trPr": "cnfStyle divId gridBefore gridAfter wBefore wAfter cantSplit trHeight tblHeader tblCellSpacing jc hidden ins del trPrChange",
        }
        for name, order in sequences.items():
            ranks = {tag(value): i for i, value in enumerate(order.split())}
            for properties in self.xml.iter(tag(name)):
                properties[:] = sorted(properties, key=lambda node: ranks.get(node.tag, 999))
        self.parts["word/document.xml"] = E.tostring(self.xml, xml_declaration=True, encoding="UTF-8", standalone=True)
        with ZipFile(path, "w", compression=ZIP_DEFLATED) as output:
            for name, value in self.parts.items():
                info = ZipInfo(name, date_time=(2026, 7, 23, 23, 20, 0))
                info.compress_type = ZIP_DEFLATED
                output.writestr(info, value)


def generar_word(root, work):
    data = json.loads((root / "reports/resumen_final.json").read_text(encoding="utf-8"))
    paths = []
    for stem, title in {"LIBRO_DE_CODIGOS": "Libro de códigos", "INFORME_CALIDAD": "Informe de calidad de datos"}.items():
        document = AcademicDocument(root / "assets/plantilla_uvg.docx", title)
        content = (root / f"docs/{stem}.md").read_text(encoding="utf-8")
        if stem == "LIBRO_DE_CODIGOS":
            document.paragraph("Descripción del conjunto de datos", 2)
            document.paragraph(f"Este libro documenta {data['variables_limpias']} variables de {data['registros_limpios']:,} códigos de servicio educativo de nivel Diversificado en Guatemala. Incluye los {data['variables_originales']} campos de origen y las variables de trazabilidad y control utilizadas durante la limpieza. Las definiciones, dominios y transformaciones permiten interpretar y volver a utilizar el CSV final.")
            content = content[content.index("## Procedencia"):]
        document.markdown(content)
        path = work / f"{stem}.docx"
        document.save(path)
        paths.append(path)
    return paths


def exportar_pdf(root, paths):
    if sys.platform == "win32":
        command = "& '" + str(root / "src/exportar_word.ps1").replace("'", "''") + "' -InputFiles @("
        command += ",".join("'" + str(p).replace("'", "''") + "'" for p in paths)
        command += ") -OutputDirectory '" + str(root / "docs").replace("'", "''") + "'"
        shell = shutil.which("pwsh.exe") or "powershell.exe"
        subprocess.run([shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command], check=True, timeout=180)
    else:
        office = shutil.which("soffice")
        if not office:
            raise RuntimeError("La exportación PDF requiere Microsoft Word en Windows o LibreOffice en Linux/macOS.")
        subprocess.run([office, "--headless", "--convert-to", "pdf", "--outdir", str(root / "docs"), *map(str, paths)], check=True)
    for source in paths:
        path = root / "docs" / (source.stem + ".pdf")
        reader = PdfReader(path)
        writer = PdfWriter()
        writer.clone_document_from_reader(reader)
        if "/Metadata" in writer.root_object:
            del writer.root_object["/Metadata"]
        writer.metadata = None
        writer.add_metadata({"/Title": "Proyecto 1 Data Science", "/Author": "Ihan Marroquin; Diego Patzan; Milton Polanco", "/Subject": "Entrega del 23 de julio de 2026", "/FechaEntrega": "2026-07-23"})
        writer.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
        temporary = path.with_suffix(".publicacion.pdf")
        with temporary.open("wb") as stream:
            writer.write(stream)
        temporary.replace(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directorio-trabajo", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.directorio_trabajo:
        args.directorio_trabajo.mkdir(parents=True, exist_ok=True)
        exportar_pdf(root, generar_word(root, args.directorio_trabajo))
    else:
        with tempfile.TemporaryDirectory(prefix="documentos_uvg_") as folder:
            exportar_pdf(root, generar_word(root, Path(folder)))
