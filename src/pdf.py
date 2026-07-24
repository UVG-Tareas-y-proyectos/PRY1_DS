"""Exporta el libro de códigos y el informe a PDF con ReportLab."""
from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate,
                               Spacer, Table, TableStyle)

NAVY = colors.HexColor("#12334A")
TEAL = colors.HexColor("#087E8B")


def fonts():
    candidates = [Path("C:/Windows/Fonts/arial.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")]
    for p in candidates:
        if p.exists():
            pdfmetrics.registerFont(TTFont("Body", str(p)))
            bold = p.with_name("arialbd.ttf" if p.name == "arial.ttf" else "DejaVuSans-Bold.ttf")
            pdfmetrics.registerFont(TTFont("BodyBold", str(bold if bold.exists() else p)))
            pdfmetrics.registerFontFamily("Body", normal="Body", bold="BodyBold", italic="Body", boldItalic="BodyBold")
            return "Body", "BodyBold"
    return "Helvetica", "Helvetica-Bold"


def inline(text):
    value = html.escape(text.replace("\\|", "|"))
    value = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`([^`]+)`", r"<font color='#087E8B'>\1</font>", value)
    return value


def exportar(source: Path, target: Path):
    normal, bold = fonts()
    styles = getSampleStyleSheet()
    base = dict(fontName=normal, fontSize=9, leading=13, textColor=NAVY, spaceAfter=7)
    styles.add(ParagraphStyle("Texto", **base))
    styles.add(ParagraphStyle("TablaTexto", **{**base, "fontSize": 7.4, "leading": 10, "spaceAfter": 0}))
    styles.add(ParagraphStyle("TituloDoc", fontName=bold, fontSize=25, leading=30, textColor=NAVY, spaceAfter=16))
    styles.add(ParagraphStyle("SeccionDoc", fontName=bold, fontSize=15, leading=20, textColor=TEAL, spaceBefore=15, spaceAfter=9, keepWithNext=True))
    styles.add(ParagraphStyle("VariableDoc", fontName=bold, fontSize=11, leading=15, textColor=NAVY, spaceBefore=12, spaceAfter=7, keepWithNext=True))
    story = []
    lines = source.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("| "):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                raw = lines[i].strip().strip("|")
                cols = [x.strip() for x in re.split(r"(?<!\\)\|", raw)]
                if not all(re.fullmatch(r":?-+:?", x) for x in cols):
                    rows.append([Paragraph(inline(x), styles["TablaTexto"]) for x in cols])
                i += 1
            n = len(rows[0])
            widths = [16.6 * cm / n] * n
            if n == 4:
                widths = [3.2 * cm, 9 * cm, 2.2 * cm, 2.2 * cm]
            table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDECF0")),
                ("LINEBELOW", (0, 0), (-1, 0), 1, TEAL),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7F8")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]))
            story.extend([table, Spacer(1, 9)])
            continue
        if line.startswith("### "):
            style, value = "VariableDoc", line[4:]
        elif line.startswith("## "):
            style, value = "SeccionDoc", line[3:]
        elif line.startswith("# "):
            style, value = "TituloDoc", line[2:]
        else:
            style, value = "Texto", line.removeprefix("- ")
            while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(("#", "|", "- ")):
                i += 1
                value += " " + lines[i].strip()
        story.append(Paragraph(inline(value), styles[style]))
        if style == "TituloDoc":
            story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=13))
        i += 1

    def page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.setFont(normal, 7)
        canvas.drawString(2.2 * cm, 28.65 * cm, "UVG  /  CC3084 DATA SCIENCE  /  PROYECTO 1")
        canvas.setStrokeColor(colors.HexColor("#DDECF0"))
        canvas.line(2.2 * cm, 1.65 * cm, 18.8 * cm, 1.65 * cm)
        canvas.drawString(2.2 * cm, 1.15 * cm, "Versión 1.0.0  |  MINEDUC - Diversificado")
        canvas.drawRightString(18.8 * cm, 1.15 * cm, str(doc.page))
        canvas.restoreState()

    # Mantener íntegra cada ficha de variable para no dejar su tratamiento
    # o metadatos en otra página sin el nombre del campo.
    rebuilt, group, pending_heading = [], [], []
    for flow in story:
        heading = isinstance(flow, Paragraph) and flow.style.name in {"VariableDoc", "SeccionDoc"}
        if heading and group:
            rebuilt.append(KeepTogether(group))
            group = []
        if isinstance(flow, Paragraph) and flow.style.name == "SeccionDoc" and flow.getPlainText().startswith("Variables"):
            pending_heading = [flow]
            continue
        if isinstance(flow, Paragraph) and flow.style.name == "VariableDoc":
            group = pending_heading + [flow]
            pending_heading = []
        elif group:
            group.append(flow)
        else:
            rebuilt.append(flow)
    if group:
        rebuilt.append(KeepTogether(group))
    target.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(target), pagesize=(21 * cm, 29.7 * cm),
                            rightMargin=2.2 * cm, leftMargin=2.2 * cm,
                            topMargin=1.7 * cm, bottomMargin=2.05 * cm,
                            title=lines[0].removeprefix("# "),
                            author="Ihan Marroquin; Diego Patzan; Milton Polanco")
    doc.build(rebuilt, onFirstPage=page, onLaterPages=page)
    print(f"PDF generado: {target.name}")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    for name in ["LIBRO_DE_CODIGOS", "INFORME_CALIDAD"]:
        exportar(root / f"docs/{name}.md", root / f"docs/{name}.pdf")
