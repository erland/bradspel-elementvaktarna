# Elementväktarna

Ett print-and-play-samarbetsspel där fyra elementväktare samlar kristaller och besegrar Skuggmästaren innan Ljuset når **Släckt**.

## Viktiga källor

- `docs/player/RULEBOOK.md` – spelarregler
- `data/rules/` – strukturerade regler
- `data/cards/` – kortdata
- `data/board/board.yaml` – spelplansdata
- `assets/` – källgrafik
- `templates/` – layoutmallar
- `scripts/` – build, validering, simulering och releasepaketering

## Bygg

```bash
python scripts/build.py
```

YAML, Markdown, mallar, assets och script är källor. `output/` är genererad build-output och versionsspåras inte.

## Spelplansvarianter

Byggpipelinen genererar:

- `board-a4.pdf` – standard
- `board-a4-ink-friendly.pdf` – tonersnål

Aktiva bakgrunder:

- `assets/backgrounds/board-background-standard.png`
- `assets/backgrounds/board-background-ink-friendly.png`

Ljusindikatorn ligger som SVG-overlay ovanpå bakgrunden och placeras från `data/board/board.yaml`.

## Simulering

```bash
python scripts/simulate_game.py
```

Aktuell simuleringskonfiguration finns i `data/simulation/pass.yaml`. Resultat skapas i `output/simulation/`. Historiska rapporter i `docs/designer/` behåller versionsnamn eftersom de dokumenterar vilket regeläge som faktiskt testades.

## Validering

```bash
python scripts/validate_project.py
```

Spelarreglerna och strukturerade YAML-filer ska beskriva samma regler. Valideringen kontrollerar även projektstruktur, assets, spelplansreferenser, kortikoner och att genererade kataloger inte versionsspåras.

## Repository-policy

Git innehåller källor och bygglogik, inte genererad output:

- `output/`, `dist/`, `release/` och `archive/` ignoreras.
- Git-historiken ersätter versionskopior av aktiva källfiler.
- Aktuella källfiler använder stabila filnamn utan projektreleaseversioner.
- Git-taggen är källa för releaseversionen.

`CHANGELOG.md` och historiska test-/simuleringsrapporter får innehålla versionsnummer eftersom versionen där är historisk information.

Se `docs/designer/VERSIONING_POLICY.md` för den fullständiga policyn.

## GitHub Actions

Projektet har tre workflows:

1. `.github/workflows/01-validate.yml` – validering vid pull request/push.
2. `.github/workflows/02-build-preview.yml` – manuell preview-build av alla utskrivbara PDF:er.
3. `.github/workflows/03-release.yml` – taggar `v*` bygger och publicerar en GitHub Release.

Lokalt releasepaket:

```bash
python scripts/build.py
python scripts/package_release.py --version vX.Y.Z
```

Se `docs/designer/GITHUB_ACTIONS.md` för detaljer.
