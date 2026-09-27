"""
Builds a print-ready PDF containing 10 Capgemini Exceller style online
assessment test sets:

    Sets 1-5    Standard / Analyst band       (moderate difficulty)
    Sets H1-H5  Senior Analyst band           (medium-hard difficulty)

Each set carries:
    Section A   Pseudo-code + computer fundamentals (30 Q)
    Section B   English communication
    Section C   Game-based cognitive (Aon smartPredict formats)
    Section D   Coding round (2 problems)

All answer keys are collected in a separate part at the end so the
question sets can be attempted as real timed tests.

Run:
    python build_pdf.py
"""

import io
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame,
                                KeepTogether, PageBreak, PageTemplate,
                                Paragraph, Preformatted, Spacer, Table,
                                TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PDF = os.path.join(HERE, "Capgemini_Exceller_10_Test_Sets.pdf")

PAGE_W, PAGE_H = A4
M_L = M_R = 17 * mm
M_T = 16 * mm
M_B = 16 * mm
FRAME_W = PAGE_W - M_L - M_R


# --------------------------------------------------------------------------
# Fonts: prefer real Windows faces, fall back to the built-in Type 1 set.
# --------------------------------------------------------------------------
def register_fonts():
    body, bold, mono = "Helvetica", "Helvetica-Bold", "Courier"
    fdir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")

    def try_reg(name, filename):
        path = os.path.join(fdir, filename)
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                return True
            except Exception:
                return False
        return False

    if try_reg("Body", "calibri.ttf") and try_reg("BodyB", "calibrib.ttf"):
        body, bold = "Body", "BodyB"
    elif try_reg("Body", "arial.ttf") and try_reg("BodyB", "arialbd.ttf"):
        body, bold = "Body", "BodyB"

    if try_reg("Mono", "consola.ttf"):
        mono = "Mono"

    return body, bold, mono


F_BODY, F_BOLD, F_MONO = register_fonts()

INK = colors.HexColor("#1A1A1A")
ACCENT = colors.HexColor("#0B5FA5")
MUTED = colors.HexColor("#5A6472")
CODE_BG = colors.HexColor("#F2F4F7")
CODE_BR = colors.HexColor("#C4CBD4")

ST_PART = ParagraphStyle("part", fontName=F_BOLD, fontSize=22, leading=27,
                         textColor=ACCENT, spaceBefore=0, spaceAfter=10)
ST_SET = ParagraphStyle("set", fontName=F_BOLD, fontSize=16, leading=20,
                        textColor=ACCENT, spaceBefore=0, spaceAfter=3)
ST_SEC = ParagraphStyle("sec", fontName=F_BOLD, fontSize=11, leading=14,
                        textColor=colors.white, backColor=colors.HexColor("#33414F"),
                        borderPadding=(4, 5, 4, 5),
                        spaceBefore=11, spaceAfter=7)
ST_SUB = ParagraphStyle("sub", fontName=F_BOLD, fontSize=10, leading=13,
                        textColor=ACCENT, spaceBefore=8, spaceAfter=3)
ST_BODY = ParagraphStyle("body", fontName=F_BODY, fontSize=9.4, leading=12.6,
                         textColor=INK, alignment=TA_LEFT, spaceAfter=5)
ST_Q = ParagraphStyle("q", fontName=F_BODY, fontSize=9.4, leading=12.6,
                      textColor=INK, spaceBefore=5, spaceAfter=2.5)
ST_OPT = ParagraphStyle("opt", fontName=F_BODY, fontSize=9.2, leading=12,
                        textColor=INK, leftIndent=9, spaceBefore=1.5,
                        spaceAfter=3)
ST_KEY = ParagraphStyle("key", fontName=F_MONO, fontSize=8.4, leading=11.6,
                        textColor=INK, leftIndent=4, spaceAfter=4)
ST_NOTE = ParagraphStyle("note", fontName=F_BODY, fontSize=8.8, leading=11.8,
                         textColor=MUTED, spaceAfter=5)
ST_CODE = ParagraphStyle("code", fontName=F_MONO, fontSize=8.1, leading=10.1,
                         textColor=INK)
ST_TITLE = ParagraphStyle("title", fontName=F_BOLD, fontSize=27, leading=32,
                          textColor=ACCENT, alignment=TA_CENTER, spaceAfter=6)
ST_SUBTITLE = ParagraphStyle("subtitle", fontName=F_BODY, fontSize=12.5,
                             leading=17, textColor=MUTED, alignment=TA_CENTER,
                             spaceAfter=4)

# Pass 1 records which page each set starts on; pass 2 reads that map so the
# running header is correct on the page where a set begins, not one page late.
_page_map = {}
_recording = {"on": True}


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def code_block(lines):
    txt = "\n".join(lines) if lines else " "
    inner = Preformatted(txt, ST_CODE)
    t = Table([[inner]], colWidths=[FRAME_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, CODE_BR),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def header_for(page):
    """Name of the set that owns this page, from the pass-1 page map."""
    best = ""
    for start in sorted(_page_map):
        if start <= page:
            best = _page_map[start]
        else:
            break
    return best


def on_page(canv, doc):
    canv.saveState()
    canv.setFont(F_BODY, 7.6)
    canv.setFillColor(MUTED)
    label = "" if _recording["on"] else header_for(doc.page)
    if label:
        canv.drawString(M_L, PAGE_H - M_T + 5 * mm, label)
    canv.drawRightString(PAGE_W - M_R, PAGE_H - M_T + 5 * mm,
                         "Capgemini Exceller - Practice Assessment Sets")
    canv.setStrokeColor(CODE_BR)
    canv.setLineWidth(0.4)
    canv.line(M_L, PAGE_H - M_T + 4 * mm, PAGE_W - M_R, PAGE_H - M_T + 4 * mm)
    canv.line(M_L, M_B - 4 * mm, PAGE_W - M_R, M_B - 4 * mm)
    canv.drawString(M_L, M_B - 8.5 * mm,
                    "Practice material - not affiliated with or endorsed by Capgemini.")
    canv.drawRightString(PAGE_W - M_R, M_B - 8.5 * mm, "Page %d" % doc.page)
    canv.restoreState()


class SetName(Flowable):
    """Zero-height marker. During pass 1 it records its own page number."""

    def __init__(self, name):
        Flowable.__init__(self)
        self.name = name

    def wrap(self, availWidth, availHeight):
        return (0, 0)

    def draw(self):
        if _recording["on"]:
            _page_map[self.canv.getPageNumber()] = self.name


# --------------------------------------------------------------------------
# Markup parser
#
#   #PART t     new page, part banner
#   #SET t      new page, set heading + running header
#   #SEC t      section bar
#   #SUB t      small sub-heading
#   #Q n|text   numbered question (text optional)
#   #C ... #E   literal monospace block
#   #O t        options line
#   #P t        paragraph
#   #B t        bold paragraph
#   #N t        muted note paragraph
#   #K t        monospace answer-key line
#   #SP n       vertical space of n points
#   #PB         page break
# --------------------------------------------------------------------------
def parse(src):
    flow = []
    group = []

    def flush():
        if not group:
            return
        if len(group) == 1:
            flow.append(group[0])
        else:
            flow.append(KeepTogether(list(group)))
        group.clear()

    lines = src.split("\n")
    i = 0
    while i < len(lines):
        s = lines[i].strip()

        if s.startswith("#PART "):
            flush()
            flow.append(PageBreak())
            # A part banner is not a set, so clear the running header.
            flow.append(SetName(""))
            flow.append(Paragraph(esc(s[6:]), ST_PART))
        elif s.startswith("#SET "):
            flush()
            name = s[5:]
            flow.append(PageBreak())
            flow.append(SetName(name))
            flow.append(Paragraph(esc(name), ST_SET))
        elif s.startswith("#SEC "):
            flush()
            flow.append(Paragraph(esc(s[5:]), ST_SEC))
        elif s.startswith("#SUB "):
            flush()
            group.append(Paragraph(esc(s[5:]), ST_SUB))
        elif s.startswith("#Q "):
            flush()
            payload = s[3:]
            if "|" in payload:
                num, txt = payload.split("|", 1)
                group.append(Paragraph("<b>Q%s.</b> %s" % (esc(num), esc(txt)),
                                       ST_Q))
            else:
                group.append(Paragraph("<b>Q%s.</b>" % esc(payload), ST_Q))
        elif s == "#C":
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != "#E":
                block.append(lines[i].rstrip("\r\n"))
                i += 1
            group.append(code_block(block))
        elif s.startswith("#O "):
            group.append(Paragraph(esc(s[3:]), ST_OPT))
        elif s.startswith("#P "):
            group.append(Paragraph(esc(s[3:]), ST_BODY))
        elif s.startswith("#B "):
            group.append(Paragraph("<b>%s</b>" % esc(s[3:]), ST_BODY))
        elif s.startswith("#N "):
            group.append(Paragraph(esc(s[3:]), ST_NOTE))
        elif s.startswith("#K "):
            flush()
            flow.append(Paragraph(esc(s[3:]), ST_KEY))
        elif s.startswith("#SP "):
            group.append(Spacer(1, float(s[4:])))
        elif s == "#PB":
            flush()
            flow.append(PageBreak())
        i += 1

    flush()
    return flow


def cover():
    return [
        SetName(""),
        Spacer(1, 46 * mm),
        Paragraph("Capgemini Exceller", ST_TITLE),
        Paragraph("Online Assessment - 10 Full Practice Sets", ST_SUBTITLE),
        Spacer(1, 9 * mm),
        Paragraph("Sets 1-5 &nbsp;|&nbsp; Standard Analyst band - moderate difficulty",
                  ST_SUBTITLE),
        Paragraph("Sets H1-H5 &nbsp;|&nbsp; Senior Analyst band - medium to hard",
                  ST_SUBTITLE),
        Spacer(1, 12 * mm),
        Paragraph("Pseudo-code &bull; Computer Fundamentals &bull; English "
                  "Communication<br/>Game-Based Cognitive (Aon smartPredict) "
                  "&bull; Coding Round", ST_SUBTITLE),
        Spacer(1, 20 * mm),
        Paragraph("300 pseudo-code and fundamentals questions &bull; 90 English "
                  "questions<br/>50 game-based items &bull; 20 coding problems "
                  "&bull; complete answer keys", ST_NOTE),
    ]


def make_story(parts):
    story = cover()
    for chunk in parts:
        story.extend(parse(chunk))
    return story


def _doc(target):
    doc = BaseDocTemplate(
        target, pagesize=A4,
        leftMargin=M_L, rightMargin=M_R, topMargin=M_T, bottomMargin=M_B,
        title="Capgemini Exceller - 10 Practice Assessment Sets",
        author="Practice material", subject="Placement preparation",
    )
    frame = Frame(M_L, M_B, FRAME_W, PAGE_H - M_T - M_B, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame],
                                       onPage=on_page)])
    return doc


def build(parts):
    # Pass 1: identical layout, discarded output, records set start pages.
    _page_map.clear()
    _recording["on"] = True
    _doc(io.BytesIO()).build(make_story(parts))

    # Pass 2: real output, headers resolved from the page map.
    _recording["on"] = False
    _doc(OUT_PDF).build(make_story(parts))
    return OUT_PDF


if __name__ == "__main__":
    import content

    path = build(content.PARTS)
    size = os.path.getsize(path)
    print("Wrote %s (%.1f KB)" % (path, size / 1024.0))
