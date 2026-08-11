# Projektstatus

## Aktuell fas

Releasekandidat / blindtestförberedelse. Git-taggen är källa för projektreleaseversionen; denna fil beskriver endast aktuellt tillstånd.

## Klart

- Regelbok, QuickStart, FAQ och A6-referens använder samma centrala begrepp.
- Träna ger 2 energi och Bygg ger 2 Skydd.
- Äventyrskort löses direkt och sparas inte.
- Regeln för slut på energi är dokumenterad.
- Elementplatsernas fyra krafter är officiella och dokumenterade.
- Scenariot använder Ljus till Släckt.
- Spelplanen genereras från YAML, stabila bakgrundsassets och SVG-overlay.
- Standard- och ink-friendly-spelplan byggs från samma pipeline.
- Jordskogen och Verkstaden är placerade för att bättre följa bakgrundsillustrationen.
- Ljusindikatorn har pergamentanpassade markörfält och ett separat Släckt-altare.
- Simulatorn använder `data/simulation/pass.yaml`.
- GitHub Actions validerar, bygger preview-PDF:er och publicerar taggade printreleaser.
- Genererade kataloger ligger inte i Git.

## Viktiga designbeslut

- Elementplatskrafterna behålls och gäller endast mot Kristallväktare när matchande elementhjälte är på platsen.
- Git-historiken används för äldre källversioner i stället för parallella versionsfiler.
- Aktuella källfiler ska ha stabila filnamn utan projektreleaseversion.
- Versionsnummer behålls där de är verklig historisk data, främst i `CHANGELOG.md`, playtestloggar och historiska simuleringsrapporter.
- Git-taggen är releaseversionens enda primära källa.

## Kända risker

- Fysiska blindtester behövs fortfarande för regelklarhet och spelupplevelse.
- Simulatorresultat är designhypoteser och behöver kalibreras mot mänskliga spel.
- Standard- och ink-friendly-spelplanerna bör testutskrivas på 100 % skala.

## Rekommenderat nästa steg

1. Kör en GitHub Actions preview-build från en ren checkout.
2. Testutskriv spelplan, kort och A6-referens.
3. Genomför observerat test eller blindtest och logga återkommande frågor.
4. Skapa nästa riktiga release genom en Git-tagg när materialet är godkänt.
