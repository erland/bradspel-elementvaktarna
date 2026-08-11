# Elementväktarna v0.59

Spelet använder **Ljuset** som nedräkning mot **Släckt**.

- Normal: 8 Ljus
- Svår: 7 Ljus
- Mycket svår: 6 Ljus
- När en effekt utlöses: Förlora 1 Ljus
- Om Ljuset slocknar förlorar gruppen

Slutfienden heter **Skuggmästaren**.

## Bygg

```bash
python scripts/build.py
```

YAML, Markdown, mallar och script är källor. PDF-filerna är genererad output.


## Simulering

```bash
python scripts/simulate_game.py
```

Resultat skapas i `output/simulation/`. Aktuell simuleringskonfiguration finns i `data/simulation/pass-v0.45.yaml`. Senaste verifierade rapporten finns i `docs/designer/SIMULATION_REPORT_v0.45.md`.


Alla Äventyrskort löses direkt och kastas. Inga kort sparas framför hjältarna.

## Release

`output/`, `dist/`, `release/` och `archive/` versionsspåras inte. De är genererade eller historiska arbetsytor och kan återskapas från källorna och Git-historiken.

- Preview-PDF:er byggs av `.github/workflows/02-build-preview.yml` och publiceras som GitHub Actions-artifact.
- Taggar `v*` triggar `.github/workflows/03-release.yml`, som bygger om allt från källor och publicerar ett rent printpaket som GitHub Release.
- `RELEASE_INVENTORY.json` är källkonfigurationen för vilka printfiler som ska ingå.

Lokalt kan genererad output skapas med `python scripts/build.py` och releasepaket med `python scripts/package_release.py --version vX.Y.Z`.

## Regelkälla

Spelarreglerna i `docs/player/RULEBOOK.md` och strukturerade YAML-filer i `data/rules/` ska beskriva samma regler. `scripts/validate_gameplay.py` kontrollerar centrala värden och förbjudna äldre begrepp.


## Modulär spelplan v0.51

Ljusspåret använder den integrerade A4-masterbakgrunden `assets/backgrounds/board-background-v0.50-a4-parchment.png`. SVG-overlayn lägger endast på ljusnivåer, markörfält och exakt geometri. Placeringen styrs från `data/board/board.yaml`.

## Ljusindikator v0.51

Markörfälten är smalare och använder varm pergamentton, diskret dubbelram och små ornament. Bakgrundsbild och spelregler är oförändrade.


## Spelplansvarianter v0.54

Byggpipelinen genererar både `board-a4.pdf` (standard) och `board-a4-ink-friendly.pdf` (tonersnål). Bakgrunderna styrs från `data/board/board.yaml`.


## Repository-policy v0.59

Git ska innehålla källor och bygglogik, inte genererad output. `.gitignore` exkluderar därför `output/`, `dist/`, `release/` och `archive/`. `scripts/validate_project.py` kontrollerar i en Git-checkout att sådana filer inte råkat versionsspåras.

## GitHub Actions

Projektet har tre workflow-filer i `.github/workflows/`:

1. `01-validate.yml` – snabb projekt- och gameplayvalidering vid pull request och push till `main`.
2. `02-build-preview.yml` – manuell build av alla PDF-filer för förhandsgranskning och uppladdning som ett gemensamt GitHub Actions-artifact.
3. `03-release.yml` – körs på taggar `v*`, bygger om allt från källor, skapar ett rent printpaket och publicerar både paketet och de viktigaste PDF-filerna som GitHub Release-assets.

Lokalt kan samma steg köras med:

```bash
python scripts/validate_project.py
python scripts/build.py
python scripts/package_release.py --version v0.58
```

Se `docs/designer/GITHUB_ACTIONS.md` för detaljer.
