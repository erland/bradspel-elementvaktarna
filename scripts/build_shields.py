from pathlib import Path
import yaml, cairosvg
ROOT=Path(__file__).resolve().parents[1]
cfg=yaml.safe_load((ROOT/"data/tokens/shields.yaml").read_text(encoding="utf-8"))["shield_tokens"]
OUTSVG=ROOT/"output/svg/tokens"; OUTPDF=ROOT/"output/pdf"; OUTPRE=ROOT/"output/preview"
for p in [OUTSVG,OUTPDF,OUTPRE]: p.mkdir(parents=True,exist_ok=True)

W,H=794,1123
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<rect width="794" height="1123" fill="#fff"/>',
       '<text x="397" y="72" text-anchor="middle" font-family="DejaVu Sans Condensed" font-size="30" font-weight="700" fill="#245b46">SKYDDSMARKÖRER</text>']
positions=[]
for row in range(4):
    for col in range(2):
        positions.append((220+350*col,220+220*row))
for i,(x,y) in enumerate(positions[:cfg["count"]]):
    parts.append(f'<path d="M{x},{y-72} L{x+68},{y-40} L{x+54},{y+44} Q{x},{y+98} {x-54},{y+44} L{x-68},{y-40} Z" fill="{cfg["color"]}" stroke="#17211c" stroke-width="6"/>')
    parts.append(f'<path d="M{x},{y-52} V{y+60} M{x-45},{y-25} Q{x},{y+5} {x+45},{y-25}" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/>')
    parts.append(f'<text x="{x}" y="{y+18}" text-anchor="middle" font-family="DejaVu Sans" font-size="18" font-weight="700" fill="#17211c">SKYDD</text>')
parts.append('</svg>')
svg=OUTSVG/"shield-tokens-a4.svg"; svg.write_text("\n".join(parts),encoding="utf-8")
cairosvg.svg2pdf(url=str(svg),write_to=str(OUTPDF/"shield-tokens-a4.pdf"))
cairosvg.svg2png(url=str(svg),write_to=str(OUTPRE/"shield-tokens-a4.png"),output_width=1200)
print(OUTPDF/"shield-tokens-a4.pdf")
