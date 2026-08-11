# Projektstatus

## Version

v0.58 – CI- och releaseautomation

## Klart

- Regelbok, QuickStart, FAQ och A6-referens använder samma värden och begrepp.
- Träna ger 2 energi och Bygg ger 2 Skydd i alla källor.
- Äventyrskort löses direkt och sparas aldrig.
- Regeln för 0 energi är dokumenterad och strukturerad.
- Elementplatsernas fyra krafter är officiella och dokumenterade.
- Scenariot använder Ljus 8 till Släckt i stället för det äldre Mörkersystemet.
- Komponentlistan använder Ljusmarkör, fyra spelpjäser och fyra livmarkörer till Skuggmästaren.
- Versionsmärkning och releasevägar är uppdaterade till v0.45.
- Valideringen kontrollerar centrala regler och söker efter borttagna begrepp.

- Simuleringskonfigurationen är versionsspårad som `data/simulation/pass-v0.45.yaml` och en verifieringskörning reproducerar tidigare balansresultat.


- Jordskogen och Verkstaden är flyttade cirka 15 mm åt vänster och 15 mm uppåt för bättre överensstämmelse med bakgrundsillustrationen.

## Viktiga designbeslut

Elementplatskrafterna behålls eftersom de redan används av simulatorn och ger platserna taktisk identitet. De gäller endast när matchande elementhjälte är på platsen och endast mot Kristallväktare.

## Rekommenderat nästa steg

- Gör en testutskrift av A6-referensen och kontrollera läsbarheten.
- Genomför ett observerat speltest med fokus på elementplatskrafterna och regeln för 0 energi.
- Gå därefter vidare mot v0.50 för externt blindtest.


## Senaste justering

Spelarterminologin använder nu **slut på energi**, **Skuggvakt** och **Skuggmästaren** konsekvent. A6-referensen har omstrukturerats för bättre läsbarhet.

## v0.45 layoutprototyp

Enkelsidigt A6-referenskort har omstrukturerats och regenererats. Hjälteunika förmågor ligger endast på hjältekorten. Referensen förtydligar nu platskrafternas begränsning, Skuggmästarens krav och att Skydd inte stoppar Ljusförlust. Spelregler och balans är oförändrade. A6-layouten är godkänd och publicerad i release/v0.49/. Tidigare release-mappar är borttagna.

## Release-status

- Aktuell lokalt paketerad release: `release/v0.57/`
- Status: extern blindtestversion
- Tidigare release-mappar är borttagna ur projektzippen.


## v0.48

Spelplanens ljusindikator är modulär och tonerreducerad. Nästa rekommenderade steg är fysisk testutskrift av spelplanen och kontroll av läsbarhet på 100 % skala.


## v0.49

Spelplanen använder nu en komplett A4-masterbakgrund där pergamentpanelen är integrerad i illustrationen. Ljusnivåer och markörfält läggs fortfarande på datadrivet som SVG-overlay i byggpipelinen.

## v0.50 – Integrerad smal pergamentbakgrund

- Den godkända A4-bakgrunden är aktiv källa för spelplansbygget.
- `data/board/board.yaml` pekar på `assets/backgrounds/board-background-v0.50-a4-parchment.png`.
- Ljusspårets SVG-overlay är omplacerad och skalad för den smalare pergamentytan.
- Spelplanens SVG, PDF och PNG-preview är regenererade från den ordinarie byggpipelinen.
- Inga spelregler eller balansvärden har ändrats.

## v0.53 – Finjusterad ljusindikator

- Flyttade ljusindikatorn 8 px åt vänster från v0.52, till +8 px relativt v0.51.
- Ingen regel- eller balansändring.

## v0.51 – Pergamentanpassad ljusindikator

- Ljusnivåernas markörfält är smalare.
- Fälten använder varm halvtransparent pergamentton, dubbelram och diskret ornamentik.
- Släckt-fältet har anpassats till samma visuella språk.
- Spelregler, balans och A4-bakgrund är oförändrade.


## v0.54 – Standard och ink-friendly spelplan

- Behåller standardbakgrunden som ordinarie version.
- Lägger till den godkända ljusare bakgrunden som ink-friendly-variant.
- Samma SVG-overlay, platser och spelregler används för båda varianterna.
- Byggpipelinen genererar båda spelplans-PDF:erna automatiskt.


## Senaste justering v0.56

- Släckt-läget på ljusindikatorn är nu ett fristående stenaltare med en släckt kristall, utan rektangulär rutram.
- Standard- och ink-friendly-spelplanerna byggs från samma pipeline.

## v0.58 – GitHub Actions

- `.github/` ligger i repositoryts rot på samma nivå som `README.md`.
- Automatisk snabbvalidering körs vid pull request och push till `main`.
- Manuell preview-build genererar alla utskrivbara PDF:er som GitHub Actions-artifact.
- Taggar `v*` bygger projektet från källor, paketerar en ren printrelease och publicerar GitHub Release-assets.
- Ny `scripts/validate_project.py` kontrollerar projektstruktur, YAML, tillgångar, spelplansreferenser, kortikoner, release-inventering och befintlig gameplayvalidering.
- Ny `scripts/package_release.py` skapar reproducerbart releasepaket med manifest och SHA-256-checksummor.
