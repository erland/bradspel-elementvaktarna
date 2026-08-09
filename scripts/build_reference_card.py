
from pathlib import Path
import html, textwrap, yaml
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/reference/player-reference-a6.yaml"
TEMPLATE = (ROOT / "templates/reference/player-reference-a6.svg").read_text(encoding="utf-8")
OUT_SVG = ROOT / "output/svg/reference"
OUT_PDF = ROOT / "output/pdf"
OUT_PREVIEW = ROOT / "output/preview"

for p in [OUT_SVG, OUT_PDF, OUT_PREVIEW]:
    p.mkdir(parents=True, exist_ok=True)

with DATA.open(encoding="utf-8") as f:
    cfg = yaml.safe_load(f)["reference_card"]

W = cfg["format"]["width_px"]
H = cfg["format"]["height_px"]

def t(text, x, y, size=9.0, weight=400, fill="#17211C", anchor="start"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-family="DejaVu Sans, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}">{html.escape(text)}</text>')

def box(x, y, w, h, title, fill="#F7FAF8"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
        f'fill="{fill}" stroke="#C7D8D0" stroke-width="1.4"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="19" rx="8" fill="#DDECE5"/>'
        f'<rect x="{x}" y="{y+11}" width="{w}" height="8" fill="#DDECE5"/>'
        f'{t(title, x+8, y+13.5, 9.4, 700, "#245B46")}'
    )

parts=[]

# LEFT: turn flow and actions
parts.append(box(20, 76, 255, 224, "DIN TUR"))
y=108
for num, heading, line in [
    ("1", "FLYTTA", "Flytta 0–1 steg längs en väg."),
    ("2", "VÄLJ 1 HANDLING", ""),
]:
    parts.append(f'<circle cx="35" cy="{y-3}" r="9" fill="#245B46"/>')
    parts.append(t(num,35,y,9,700,"#FFFFFF","middle"))
    parts.append(t(heading,50,y,9.2,700,"#7B4E25"))
    if line:
        parts.append(t(line,50,y+13,8.4))
    y += 31 if line else 22

actions=[
    ("UTFORSKA","Dra 1 äventyrskort."),
    ("KÄMPA","Mot Kristallväktare eller Skuggmästaren."),
    ("TRÄNA","På Träningsgården: +2 energi, max 5."),
    ("BYGG","I Verkstaden: få och fördela 2 Skydd."),
]
for lab, desc in actions:
    parts.append(t(lab,35,y,8.7,700,"#7B4E25"))
    wrapped=textwrap.wrap(desc,width=31)
    for i,line in enumerate(wrapped):
        parts.append(t(line,98,y+i*10,8.3))
    y += max(13,10*len(wrapped)+3)

parts.append(f'<circle cx="35" cy="{y-3}" r="9" fill="#245B46"/>')
parts.append(t("3",35,y,9,700,"#FFFFFF","middle"))
parts.append(t("SKUGGKORT",50,y,9.2,700,"#7B4E25"))
parts.append(t("Dra och lös 1 skuggkort.",50,y+13,8.4))

# RIGHT TOP: place powers, compact one-line grid
parts.append(box(284, 76, 255, 114, "PLATSKRAFTER"))
parts.append(t("Matchande hjälte · endast mot Kristallväktare.",294,107,7.8))
place_rows=[
    ("ELD","3+ mot Kristallväktaren."),
    ("VATTEN","+1 energi efter seger."),
    ("VIND","Slå om ett misslyckat slag."),
    ("JORD","Miss = ingen energiförlust."),
]
yy=123
for lab,desc in place_rows:
    parts.append(t(lab,294,yy,8.5,700,"#7B4E25"))
    parts.append(t(desc,355,yy,8.3))
    yy+=16

# RIGHT MID: combat split into two subcolumns
parts.append(box(284, 198, 255, 102, "STRID OCH SKYDD"))
parts.append(t("STRIDSSLAG",294,230,8.5,700,"#7B4E25"))
for line in ["Kristallväktare 4+","Skuggvakt 3+","Skuggmästaren 4+"]:
    parts.append(t("• "+line,294,244,8.2))
    yy=258 if line=="Kristallväktare 4+" else yy
# explicit positions
parts[-3:]=[
    t("• Kristallväktare 4+",294,244,8.2),
    t("• Skuggvakt 3+",294,257,8.2),
    t("• Skuggmästaren 4+",294,270,8.2),
]
parts.append(t("SKYDD",416,230,8.5,700,"#7B4E25"))
parts.append(t("• 1 Skydd = +1 före slag",416,244,8.0))
parts.append(t("• eller stoppa -1 energi",416,257,8.0))
parts.append(t("• stoppar aldrig Ljusförlust",416,270,7.6))

# Footer: three compact zones, no heading
parts.append('<rect x="20" y="309" width="519" height="70" rx="9" fill="#F1E6C8"/>')
# left footer
parts.append(t("SLUT PÅ ENERGI",31,329,8.4,700,"#7B4E25"))
parts.append(t("Flytta till Träningsgården",31,342,8.1))
parts.append(t("och få 2 energi.",31,353,8.1))
# mid footer
parts.append(t("KRISTALLBELÖNINGAR",207,329,8.4,700,"#7B4E25"))
parts.append(t("Eld +1 energi  •  Vatten alla +1",207,342,7.8))
parts.append(t("Vind flytta 1  •  Jord 2 Skydd",207,353,7.8))
# right footer
parts.append(t("SKUGGMÄSTAREN",405,329,8.4,700,"#7B4E25"))
parts.append(t("Kräver alla 4 kristaller · 4 liv.",405,342,7.8))
parts.append(t("Miss: -1 energi och -1 Ljus.",405,354,8.0))
parts.append(t("Ljuset släcks = förlust.",405,366,8.0))

values={
    "W":W,"H":H,"INNER_W":W-14,"INNER_H":H-14,
    "HEADER_W":W-32,"FOOT_W":W-36,"CX":W/2,"DIVIDER_X":W/2,
    "TITLE":html.escape(cfg["title"].upper()+" · REFERENS"),
    "LEFT_CONTENT":"\n".join(parts),
    "RIGHT_CONTENT":"",
    "BOTTOM_SECTION":"",
}
svg=TEMPLATE
for k,v in values.items():
    svg=svg.replace("{{"+k+"}}",str(v))
# remove template divider; content already uses cards
svg=svg.replace('<line x1="{{DIVIDER_X}}" y1="73" x2="{{DIVIDER_X}}" y2="300"\n       stroke="#C7D8D0" stroke-width="2"/>','')
svg_path=OUT_SVG/"player-reference-a6.svg"
pdf_path=OUT_PDF/"player-reference-a6.pdf"
png_path=OUT_PREVIEW/"player-reference-a6.png"
svg_path.write_text(svg,encoding="utf-8")
cairosvg.svg2pdf(url=str(svg_path),write_to=str(pdf_path))
cairosvg.svg2png(url=str(svg_path),write_to=str(png_path),output_width=1118)
print(svg_path); print(pdf_path); print(png_path)
