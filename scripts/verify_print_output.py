#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "output/pdf"

EXPECTED = [
    "adventure-cards-a4.pdf",
    "board-a4.pdf",
    "board-a4-ink-friendly.pdf",
    "crystal-tokens-a4.pdf",
    "hero-cards-a4.pdf",
    "player-reference-a6.pdf",
    "shadow-cards-a4.pdf",
    "shield-tokens-a4.pdf",
    "rulebook.pdf",
    "quickstart.pdf",
    "faq.pdf",
]

def main() -> int:
    missing = [name for name in EXPECTED if not (PDF_DIR / name).is_file()]
    if missing:
        print("ERROR: saknade PDF-filer: " + ", ".join(missing), file=sys.stderr)
        return 2

    for name in EXPECTED:
        path = PDF_DIR / name
        if path.stat().st_size == 0:
            print(f"ERROR: tom PDF: {path}", file=sys.stderr)
            return 2
        try:
            reader = PdfReader(str(path))
            pages = len(reader.pages)
        except Exception as exc:
            print(f"ERROR: oläsbar PDF {path}: {exc}", file=sys.stderr)
            return 2
        if pages < 1:
            print(f"ERROR: PDF utan sidor: {path}", file=sys.stderr)
            return 2
        print(f"OK: {name} ({pages} sidor, {path.stat().st_size} bytes)")

    print("PRINT OUTPUT VERIFICATION OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
