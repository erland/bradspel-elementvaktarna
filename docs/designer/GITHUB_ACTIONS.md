# GitHub Actions för Elementväktarna

`.github/` ligger i repositoryts rot på samma nivå som `README.md`.

## 01 Validate

Fil: `.github/workflows/01-validate.yml`

Körs:
- vid pull request mot `main`
- vid push till `main`
- manuellt via `workflow_dispatch`

Kontroller:
- obligatoriska projektfiler
- att alla YAML-filer går att läsa
- spelplansbakgrunder, ljusindikator-overlay, plats-id:n, vägar och ikoner
- hjältebilder
- kortikoner
- `RELEASE_INVENTORY.json`
- befintlig gameplay- och terminologivalidering

Workflowen installerar bara PyYAML och är därför avsiktligt snabb.

## 02 Build Preview PDFs

Fil: `.github/workflows/02-build-preview.yml`

Startas manuellt via GitHub Actions.

Den:
1. validerar projektet
2. installerar låst Pandoc-version och Python-beroenden
3. rensar `output/`
4. kör `python scripts/build.py`
5. verifierar med `scripts/verify_print_output.py` att alla förväntade PDF-filer finns, går att läsa och har minst en sida
6. laddar upp `output/pdf/*.pdf` som ett gemensamt artifact: `elementvaktarna-preview-pdfs`

Artifact retention är 7 dagar.

## 03 Release Print Package

Fil: `.github/workflows/03-release.yml`

Triggas när en tagg som börjar med `v` pushas, exempelvis:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

Workflowen:
1. validerar projektet
2. bygger om all output från källorna
3. kör `scripts/package_release.py`
4. skapar `elementvaktarna-vX.Y.Z-print.zip`
5. publicerar printpaketet och de viktigaste PDF-filerna som GitHub Release-assets

GitHub Actions använder repositoryts automatiska `GITHUB_TOKEN`; inga egna hemligheter behövs för normal GitHub.com-användning.

## Lokala motsvarigheter

```bash
python scripts/validate_project.py
python scripts/build.py
python scripts/package_release.py --version vX.Y.Z
```

## Reproducerbarhet

- Python: 3.12 i GitHub Actions
- Pandoc: 3.1.11.1
- Python-beroenden: `requirements-ci.txt`
- PDF är rekommenderat utskriftsformat.
- YAML, Markdown, mallar, assets och script är källor. `output/`, `dist/`, `release/` och `archive/` är genererade/historiska arbetsytor och versionsspåras inte.

## Repository-policy

`output/`, `dist/`, `release/` och `archive/` finns i `.gitignore` och ska inte committas.

- `output/` skapas av buildskripten.
- `dist/` skapas av releasepaketeringen.
- `release/` ersätts av GitHub Releases.
- `archive/` ersätts av Git-historiken för gamla filer.

`01 Validate` kör `scripts/validate_project.py`. I en riktig Git-checkout använder valideraren `git ls-files` och stoppar bygget om någon av dessa kataloger ändå har råkat läggas till i Git-index.
