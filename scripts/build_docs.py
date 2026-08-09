from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUTPDF = ROOT / "output/pdf"
OUTPDF.mkdir(parents=True, exist_ok=True)

def md_to_pdf(md: Path, out: Path) -> None:
    html_path = OUTPDF / (out.stem + ".html")
    subprocess.run([
        "pandoc", str(md), "-s",
        "--css", str(ROOT / "templates/docs/rulebook.css"),
        "-o", str(html_path)
    ], check=True)
    subprocess.run(["weasyprint", str(html_path), str(out)], check=True)
    html_path.unlink(missing_ok=True)

md_to_pdf(ROOT / "docs/player/RULEBOOK.md", OUTPDF / "rulebook.pdf")
md_to_pdf(ROOT / "docs/player/QUICKSTART.md", OUTPDF / "quickstart.pdf")
md_to_pdf(ROOT / "docs/player/FAQ.md", OUTPDF / "faq.pdf")
