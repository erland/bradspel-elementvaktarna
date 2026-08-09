# Elementväktarna v0.57

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

Den rekommenderade speltestreleasen finns i:

```text
release/v0.54/
```

- `release/v0.54/print/pdf/` innehåller rekommenderade printfiler.
- `release/v0.54/docs/` innehåller spelarregler.
- `release/v0.54/playtest/` innehåller instruktion, komponentlista och feedbackformulär.
- `output/` är fortsatt arbetsyta för genererade filer och är inte samma sak som en release.

## Regelkälla

Spelarreglerna i `docs/player/RULEBOOK.md` och strukturerade YAML-filer i `data/rules/` ska beskriva samma regler. `scripts/validate_gameplay.py` kontrollerar centrala värden och förbjudna äldre begrepp.


## Modulär spelplan v0.51

Ljusspåret använder den integrerade A4-masterbakgrunden `assets/backgrounds/board-background-v0.50-a4-parchment.png`. SVG-overlayn lägger endast på ljusnivåer, markörfält och exakt geometri. Placeringen styrs från `data/board/board.yaml`.

## Ljusindikator v0.51

Markörfälten är smalare och använder varm pergamentton, diskret dubbelram och små ornament. Bakgrundsbild och spelregler är oförändrade.


## Spelplansvarianter v0.54

Byggpipelinen genererar både `board-a4.pdf` (standard) och `board-a4-ink-friendly.pdf` (tonersnål). Bakgrunderna styrs från `data/board/board.yaml`.
