# Spelbrädets lagerarkitektur

## Översikt

Spelbrädet byggs av flera separata lager. Ingen enskild fil ska bära all information.

```text
Bakgrundsbild
    +
Vägar och platsmarkörer
    +
Textrutor och etiketter
    +
Ikoner
    +
Ljusspår och andra regellager
    =
Färdig spelbrädespreview / printfil
```

## Lager 1: Bakgrund

Fil:

```text
assets/backgrounds/board-background-standard.png
```

Bakgrunden innehåller endast illustration:

- landskap
- byggnader
- grottor
- skog
- tempel
- vatten, lava och dekor

Bakgrunden ska inte innehålla:

- platsnamn
- regler
- vägar som måste vara spelmässigt exakta
- ljusspår
- nummer
- ikoner
- textrutor

Bakgrunden är alltså dekorativ grafik, inte sanningskälla för spelregler.

## Lager 2: Kartdata

Fil:

```text
data/board/board.yaml
```

Detta är projektets sanningskälla för själva kartlogiken.

Här finns bland annat:

- canvasstorlek
- plats-id
- platsnamn
- x- och y-position
- platsnummer
- vilken ikon platsen använder
- vilka platser som är sammankopplade
- placering av etiketter
- ljusspår
- färgtema

När något ska flyttas eller ändras görs ändringen i `data/board/board.yaml`.

Exempel:

```yaml
locations:
  - id: earth
    number: 5
    name: Jordskogen
    x: 165
    y: 505
    icon: protect
    label:
      position: bottom
```

För att flytta Jordskogens textruta under markören används:

```yaml
label:
  position: bottom
```

## Lager 3: Vägar och platsmarkörer

Genereras från `data/board/board.yaml`.

Detta lager innehåller:

- linjer mellan angränsande platser
- numrerade platsmarkörer
- eventuella markeringsringar

Det ska gå att slå av detta lager separat vid felsökning.

## Lager 4: Etiketter och textrutor

Genereras också från `data/board/board.yaml`.

Detta lager innehåller:

- platsnamn
- eventuella korta platseffekter
- etikettbakgrunder
- regler för placering ovanför eller under platsmarkören

Textrutor ska inte vara inbakade i bakgrundsbilden.

## Lager 5: Ikoner

Källor:

```text
assets/icons/*.svg
```

Ikonerna är separata SVG-filer och refereras via namn från `data/board/board.yaml`.

Exempel:

```yaml
icon: protect
```

motsvarar:

```text
assets/icons/protect.svg
```

## Lager 6: Extra regellager

Exempel:

- ljusspår
- kristallmarkeringar
- startmarkering
- bossmarkering
- scenarioinformation
- variantlager

Dessa bör kunna slås av och på via data eller buildinställning.

## Lagerordning

Rekommenderad ordning vid rendering:

1. bakgrund
2. vägar
3. platsmarkörer
4. etiketter
5. ikoner
6. ljusspår och andra regellager
7. debuglager, endast vid behov

## Vad generatorn gör

`scripts/build_board_only.py` ska:

1. läsa `data/board/board.yaml`
2. kontrollera att plats-id:n är unika
3. kontrollera att alla vägar refererar till befintliga platser
4. skapa SVG-lager
5. skapa en komplett overlay-SVG
6. lägga overlayn ovanpå bakgrunden för preview
7. skriva genererade filer till `output/board/`

Generatorn ska inte vara sanningskälla för positioner eller texter. Den ska bara tolka data och mallar.

## Vad som ska redigeras

Redigera normalt:

```text
data/board/board.yaml
assets/icons/*.svg
assets/backgrounds/board-background-standard.png
templates/board/
```

Redigera normalt inte:

```text
output/board/*.svg
output/board/*.png
```

Filer i `output/` är genererade och kan skrivas över vid nästa build.

## Rekommenderat arbetsflöde

```text
1. Ändra board.yaml
2. Kör generatorn
3. Kontrollera preview
4. Justera data
5. Generera på nytt
```

Detta gör att kartan går att ändra utan att manuellt redigera den färdiga SVG-filen.


## Hybridbaserat ljusspår

Ljusindikatorn använder nu två lager:

```text
assets/backgrounds/board-background-standard.png
assets/backgrounds/board-background-ink-friendly.png
assets/board/light-track/light-track-overlay.svg
```

PNG-lagret innehåller målad textur, ljus, skugga och mjuka kanter så att indikatorn smälter ihop med spelplanens illustration. SVG-lagret innehåller endast exakta ramar och markörfält. Rubrik, siffror och slutetikett genereras från `data/board/board.yaml`.

Denna uppdelning ger bättre visuell integration än en ren SVG-panel och behåller samtidigt skarp text, låg tonerbelastning och enkel redigering.
