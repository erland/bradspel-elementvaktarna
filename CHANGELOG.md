# v0.58 – GitHub Actions och automatiserad publicering

- Lade till `.github/workflows/01-validate.yml` för snabb CI-validering på pull request och push till `main`.
- Lade till `.github/workflows/02-build-preview.yml` för manuell build av samtliga PDF-filer och gemensamt preview-artifact.
- Lade till `.github/workflows/03-release.yml` för taggbaserade GitHub Releases på `v*`.
- Lade till `scripts/validate_project.py` som kontrollerar projektstruktur, YAML, assets, kortikoner, spelplansreferenser, release-inventering och gameplayvalidering.
- Lade till `scripts/package_release.py` för ren printrelease med manifest och SHA-256-checksummor.
- Lade till `scripts/verify_print_output.py` som verifierar att samtliga byggda PDF:er finns, går att läsa och innehåller sidor.
- Lade till `requirements-ci.txt` och låste Pandoc 3.1.11.1 i build-workflows.
- Ingen spelregel, balans eller grafisk komponent ändrades.

# v0.57 – Justerade platspositioner

- Flyttade Jordskogen cirka 15 mm åt vänster och 15 mm uppåt.
- Flyttade Verkstaden cirka 15 mm åt vänster och 15 mm uppåt.
- Vägar, noder, etiketter och ikoner följer de datadrivna koordinaterna i `data/board/board.yaml`.
- Regenererade standard- och ink-friendly-spelplanerna.
- Inga spelregler eller balansvärden ändrades.

# v0.56 – Fristående Släckt-altare

- Ersatte den rektangulära Släckt-rutan med ett fristående stenaltare.
- Lade till en släckt kristall, diskret rök, stensockel och sprickdetaljer.
- Flyttade Släckt-etiketten under altaret för tydligare hierarki.
- Övriga ljusnivåer, regler och balans är oförändrade.
- Regenererade standard- och ink-friendly-spelplanerna.

# v0.54 – Standard och ink-friendly spelplan

- Lade till en ljusare, tonersnål bakgrund utan att flytta eller ta bort motiv.
- Behöll standardbakgrunden som ordinarie variant.
- Uppdaterade `board.yaml` och båda byggskripten så standard och ink-friendly genereras i samma pipeline.
- Regenererade spelplans-SVG, PDF och PNG-preview för båda varianterna.
- Inga spelregler eller balansvärden ändrades.

# v0.53 – Finjusterad ljusindikator

- Flyttade hela ljusindikatorn 8 px åt vänster från v0.52.
- Slutplaceringen är +8 px relativt v0.51.
- Ingen regel- eller balansändring.

# v0.52 – Flyttad ljusindikator

- Flyttade hela SVG-overlayn för ljusindikatorn 16 px åt höger, ungefär en teckenbredd.
- Behöll storlek, pergamentstil och spelregler oförändrade.
- Regenererade spelplanens SVG, PDF och PNG-preview.

# v0.51 – Pergamentanpassad ljusindikator

- Gjorde SVG-markörfälten smalare för att lämna mer synligt pergament runt spåret.
- Ersatte de vita rundade rutorna med varm halvtransparent pergamentton.
- Lade till diskret dubbelram, rubrikornament och små sidornament.
- Anpassade Släckt-fältet till samma visuella språk.
- Regenererade spelplanens SVG, PDF och PNG-preview.
- Inga spelregler eller balansvärden ändrades.

# v0.50 – Aktiv smal pergamentbakgrund

- Lade in den godkända bakgrundsbilden som `assets/backgrounds/board-background-v0.50-a4-parchment.png`.
- Uppdaterade `data/board/board.yaml` så den nya bakgrunden används av den ordinarie spelplansbyggprocessen.
- Justerade ljusspårets SVG-overlay för den smalare pergamentytan.
- Regenererade spelplanens SVG, PDF och PNG-preview.
- Skapade release `release/v0.50/` och uppdaterade manifest och checksummor.
- Inga spelregler eller balansvärden ändrades.

# v0.49 – Integrerad A4-masterbakgrund

- Lade in den genererade A4-bakgrunden som ett permanent källasset.
- Pergamentpanelen är nu en del av spelplansbakgrunden och behöver inte komponeras som separat rasterlager.
- Behöll SVG-overlay för ljusnivåer, markörfält och exakt geometri.
- Uppdaterade `board.yaml`, spelplansmallen och båda byggskripten.
- Regenererade spelplanens SVG, PDF och PNG-preview.
- Inga spelregler eller balansvärden ändrades.

# v0.47 – Hybridbaserat ljusspår

- Ersatte det aktiva SVG-dekorlagret med en målad PNG-bakgrund.
- Lade till separat SVG-overlay för skarpa ramar och markörfält.
- Uppdaterade `data/board/board.yaml` och båda spelplansbyggskripten.
- Behöll tonerreducerad profil med ljusa fält och begränsade mörka partier.
- Regenererade spelplanens SVG, PDF och preview.
- Inga spelregler eller balansvärden ändrades.

# v0.46 – Modulär spelplanslayout

- Ljusindikatorn är nu ett separat dekorlager.
- Placering och storlek styrs från `data/board/board.yaml`.
- Ny tonerreducerad ljusspårsdesign med ljusa markörfält och begränsad mörk fyllning.
- Spelplanens SVG, PDF och preview regenererade.
- Inga spelregler eller balansvärden ändrades.

# Changelog

## v0.46 – Första release candidate

- Godkände den enkelsidiga A6-layouten som officiell spelarreferens.
- Skapade en ren release i `release/v0.46/`.
- Lade till release-README, manifest, checksummor och uppdaterat blindtestpaket.
- Tog bort tidigare release-mappar ur projektet.
- Regenererade och verifierade spelar-PDF:er.
- Spelregler och balans är oförändrade från v0.45.

## v0.45 – Enkelsidig A6-omstrukturering

- Tog bort Vindväktarens individuella rörelseförmåga från A6-kortet; hjälteförmågor hänvisas till hjältekorten.
- Förtydligade Flytta till 0–1 steg längs en väg.
- Förtydligade att platskrafter endast gäller mot Kristallväktare.
- Lade till att Skuggmästaren kräver alla fyra kristaller och har fyra liv.
- Lade till att Skydd aldrig stoppar Ljusförlust.


## v0.44 – Terminologi och A6-förtydligande

- Ersatte spelarbegreppet **0 energi** med **slut på energi**.
- Ersatte det generella begreppet **kortfiende** med **Skuggvakt**, eftersom det är den enda fienden som förekommer på Äventyrskort.
- Förtydligade i regelboken att Skuggvakten dyker upp när Äventyrskortet Skuggvakt dras.
- Ersatte **Boss** med **Skuggmästaren** i spelartexter och A6-referens.
- Delade A6-avsnittet **Kämpa & Skydd** i tydligare avsnitt för **Stridsslag** och **Skydd**.
- Gav varje platskraft en egen rad och tog bort rubriken **Kom ihåg** i sidfoten.
- Ändrade A6-raden för slut på energi till att börja med **Flytta till Träningsgården**.
- Regenererade spelar-PDF:er och A6-referens.

## v0.44 - Konsistens- och regelharmonisering

- Synkroniserade regelbok, QuickStart, FAQ, A6-referens och YAML.
- Rättade Träna till +2 energi och Bygg till 2 Skydd överallt.
- Tog bort kvarvarande hänvisningar till sparade Äventyrskort.
- Gjorde elementplatsernas fyra krafter till officiella spelarregler.
- Dokumenterade fullständig regel för 0 energi.
- Konverterade första scenariot från Mörker till Ljus/Släckt.
- Standardiserade komponentnamn och antal, inklusive fyra livmarkörer för Skuggmästaren.
- Uppdaterade versionsmärkning och releasehantering till v0.44.
- Utökade gameplay-valideringen med korsfilskontroller och sökning efter äldre begrepp.
- Versionsspårade simuleringspasset som `pass-v0.44.yaml`, uppdaterade simulatorhänvisningar och verifierade samma balansutfall som tidigare.

## v0.42
- Etablerade första strukturerade speltestreleasen i `release/v0.42/`.
- Lade till release-README och maskinläsbart `RELEASE_MANIFEST.json`.
- Skapade ett rent printpaket med rekommenderade PDF-filer.
- Lade till Läs mig först, komponentlista och blindtest-feedback som Markdown och PDF.
- Skilde tydligt mellan arbetsoutput i `output/` och delbar release i `release/`.
- Lade till automatisk fontskalning för kortnamn i den gemensamma kortgeneratorn.
- Behåller 21 pt för kortnamn som ryms och skalar stegvis ned till 14 pt vid behov.
- Verifierade att Skuggornas grepp och Modigt samarbete hålls inom rubrikrutan.
- Regenererade kortens SVG-, PDF- och previewfiler.
- Inga spelregler eller balansvärden ändrades.

## v0.41
- Lade till Förberett anfall: spendera 1 Skydd före ett stridsslag för +1 på slaget.
- Begränsade bonusen till högst 1 Skydd per slag.
- Uppdaterade regler, QuickStart, FAQ, A6-kort, strukturerad regeldata och simulator.
- Körde ny simulering och validering.

## v0.40
- Ändrade Kraftkälla till ett val mellan 1 energi och att återfå 1 Ljus.
- Begränsade återställt Ljus till spelets startvärde.
- Uppdaterade regler, FAQ, QuickStart, A6-kort och simulator.
- Körde simulering, full build och PDF-verifiering.

## v0.39
- Tog bort hjälpkortssystemet.
- Gjorde alla Äventyrskort omedelbara.
- Skrev om Elementkraft, Svag punkt, Modigt samarbete och Reservdelar.
- Uppdaterade regler, A6-kort, validering och simulator.
- Körde simulering, full build och PDF-verifiering.

## v0.38
- Träna ger nu 2 energi.
- Bygg ger nu 2 Skydd att fördela på platsen.
- Jordväktaren får fördela de 2 Skydden mellan valfria hjältar.
- Uppdaterade validering, regler, komponenttexter och simulator.
- Körde simulering, full build och PDF-verifiering.

## v0.37
- Minskat Ljuset falnar från 4 till 2 exemplar.
- Lagt till Mörk dimma.
- Lagt till Skuggornas grepp.
- Uppdaterat spelartexter och simulator.
- Kört nytt simuleringspass och jämförelse mot v0.36.
- Kört full build och PDF-verifiering.

## v0.36
- Lade till YAML-driven spelsimulator.
- Körde 27 000 huvudsimuleringar för 8/7/6 Ljus.
- Lade till känslighetsanalys för 8-16 Ljus.
- Lade till ablationstest för elementens relevans.
- Sparade rådata, exempelloggar, antaganden och rapport.
- Ingen spelregel ändrades i denna version.

## v0.35
- Ersatte Ljusspåret med Ljuset i spelartexterna.
- Tog bort lättläget på 10 Ljus.
- Ändrade svårighetsgraderna till Normal 8, Svår 7 och Mycket svår 6.
- Synkroniserade regler, QuickStart, FAQ, A6-kort och YAML.
- Kördes full build och PDF-verifiering.

## v0.34
- Ersatte Mörkerspåret med ett nedräknande Ljusspår.
- Spåret visar 8 till 1 och därefter Släckt.
- Lade till svårighetsgraderna 10, 8 och 6 Ljus.
- Uppdaterade kort, regler, FAQ, QuickStart och A6-referens.
- Standardiserade Skuggmästaren i spelartexterna.
- Kördes full build och PDF-verifiering.

## v0.34-dev2
- Uppdaterade korttexter till Förlora 1 Ljus.
- Bytte Mörkret växer mot Ljuset falnar.
- Uppdaterade regelbok, QuickStart, FAQ och A6-referens.
- Standardiserade Skuggmästaren i spelartexterna.

## v0.34-dev1
- Införde strukturerat Ljusspår med 10/8/6 som svårighetsgrader.
- Definierade Släckt som förlustläge.
- Bytte intern slutfiendeterminologi från boss till shadow_master.
- Ersatte `boss.yaml` med `shadow-master.yaml`.

## v0.33
- Tog bort smaktexten från kortens visuella rendering.
- Behöll smaktexten i YAML som strukturerad källdata.
- Flyttade ikon, beskrivningsruta, statusrad och kortlekstyp nedåt.
- Förbättrade kortens vertikala balans och avstånd till sidhuvudet.

## v0.32
- Förbättrade kortens vertikala balans.
- Flyttade ikon och beskrivningsruta uppåt.
- Gav statusrad, korttyp och smaktext mer luft.
- Tog bort Din tur/Viktigt-rubrikerna från A6-kortet.
- Flyttade handlingsbeskrivningarna längre åt höger.
- Ersatte A6-fotraden med en egen Kom ihåg-sektion.

## v0.31
- Flyttade all kortfotstext innanför kortens säkerhetszon.
- Gjorde smaktexten till en automatiskt storleksanpassad enkelrad.
- Minskade beskrivningsrutans höjd och införde kompaktare radavstånd.
- Justerade A6-referenskortets etikettkolumner och radbrytning.
- Delade A6-fotraden i två centrerade rader.
- Verifierade ny SVG- och PDF-output.

## v0.30
- Standardiserade PDF-filnamn utan versionsnummer.
- Tog bort preview, genererade SVG och temporära buildmappar ur releasepaketet.
- Tog bort gamla manifest och inaktuella granskningsrapporter.
- Behöll endast aktuella spelar- och designerdokument.
- Verifierade full build från tom output.

## v0.29
- Rensade bort samtliga äldre PDF-versioner ur output.
- Tog bort oversonerade kortleksdubbletter.
- Tog bort det gamla A4-referenskortet från output och byggscript.
- Rensade äldre PNG- och SVG-spår.
- Synkroniserade aktuella kort- och dokumentfilnamn till v0.29.
- Lade till strikt output-whitelist i cleanup-verifieringen.

## v0.28
- Lade till fullständiga regler för 2-4 spelare.
- Definierade att alla fyra hjältar alltid används.
- Lade till fast hjälteordning.
- Förtydligade separat energi, Skydd och hjälpkort per hjälte.
- Förtydligade skuggkort efter varje hjältes tur.
- Uppdaterade regelbok, QuickStart, FAQ och A6-referenskort.
- Lade till `data/rules/player-count.yaml`.

## v0.27
- Gjorde A6-referenskortet ensidigt.
- Ändrade formatet till liggande A6.
- Införde tvåspaltslayout.
- Kortade innehållet till de mest använda reglerna.
- Genererade ny SVG, PDF och PNG-preview.

## v0.26
- Lade till ett dubbelsidigt A6-referenskort för spelarna.
- Lade till strukturerad YAML-källa.
- Lade till Markdown-översikt.
- Lade till SVG-mall och separat buildscript.
- Integrerade referenskortet i huvudbuilden.
- Genererade SVG, PDF och PNG-preview.

## v0.25-dev3 - Dokument
- Uppdaterade regelboken med kristallbelöningar och bossens mörkerstraff.
- Uppdaterade QuickStart och FAQ.
- Uppdaterade A6-referenskorten.
- Lade till COMPONENT_REFERENCE.md.
- Lade till DESIGN_DECISIONS.md.
- Uppdaterade PDF-sidfoten till v0.25-dev3.
- Genererade nya dokument-PDF:er.

## v0.25-dev2 — Kortsystem
- Polerade alla äventyrs- och skuggkort.
- Standardiserade reglernas språk på korten.
- Lade till smaktext på samtliga kort.
- Förtydligade behållna hjälpkort och Vägen stängs.
- Uppdaterade kortgeneratorn för smaktext.
- Lade till CARD_SYSTEM_REVIEW.md.
- Genererade nya v0.25-dev2-kortfiler.

## v0.25-dev1 — Gameplay Polish
- Lade till omedelbara belöningar för fyra kristaller.
- Lade till mörkerökning vid misslyckade bossanfall.
- Lade till designroller för platser.
- Lade till simuleringsmetadata på kort.
- Lade till simuleringsmodell och balansmål.
- Lade till GAMEPLAY_REVIEW.md.
- PDF och spelartexter lämnas oförändrade i detta steg.

## v0.24
- Införde max 2 behållna hjälpkort per hjälte.
- Lade till regel för att kasta ett hjälpkort vid överskriden gräns.
- Gjorde Elementkraft, Svag punkt, Modigt samarbete och Reservdelar till behållna engångskort.
- Ändrade Vägen stängs till ett kort som ligger framför aktiv hjälte till efter nästa tur.
- Lade till Skydd-påminnelser på skadegivande kort.
- Uppdaterade kortgenerator, regler, snabbstart, FAQ, referenskort och validering.

## v0.23
- Införde handlingarna Träna och Bygg.
- Uppdaterade samtliga fyra hjälteförmågor.
- Gjorde elementplatsernas krafter beroende av rätt hjältes närvaro.
- Förtydligade att Vattengrottan bara ger energi vid seger.
- Begränsade Jordskogens skydd till Kristallväktaren där.
- Förtydligade att misslyckade bossanfall kostar 1 energi.
- Införde generella Skyddsmarkörer som kan blockera energiförlust på 1.
- Lade till åtta utskrivbara Skyddsmarkörer.
- Uppdaterade regelbok, snabbstart, FAQ, referenskort och validering.

## v0.22
- Införde tre ömsesidigt uteslutande handlingar.
- Gjorde kristallerna synliga och platsbundna.
- Införde Kristallväktare med slag på 4+.
- Tog bort Kristallens sken ur äventyrsleken.
- Lade till fyra nya stödkort för kristallstrider.
- Definierade att kortfiender löses direkt.
- Uppdaterade regler, snabbstart, FAQ och referenskort.
- Lade till kristallmarkörer som SVG, PDF och PNG.
- Uppdaterade speldata, scenario och validering.

## v0.21
- Tog bort dubbla titlar i PDF-exporten.
- Flyttade spelarens dokument till `docs/player/`.
- Lade utvecklingsmaterial i `docs/designer/`.
- Tog bort prototyp-, speltest- och anteckningsspråk från regelbok, snabbstart och FAQ.
- Lade till konsekventa PDF-sidfötter med version och sidnummer.
- Uppdaterade buildscriptets sökvägar och PDF-filnamn.
- Uppdaterade README och projektstatus.

## v0.20
- Lade till strukturerad spelmotor under `data/rules/`.
- Lade till första scenariofilen.
- Definierade turordning, handlingar och energiregler.
- Definierade sju platsförmågor.
- Införde fyra dolda och slumpade kristaller på elementplatser.
- Definierade Skuggmästaren med fyra sköldar och fyra liv.
- Uppdaterade Kristallens sken till fyra kopior.
- Skapade RULEBOOK.md, QUICKSTART.md och FAQ.md.
- Lade till PDF-export via Pandoc och WeasyPrint.
- Skapade A6-referenskort på A4.
- Lade till gameplay-validering.
- Uppdaterade README och projektstatus.

## v0.19
- Ersatte teckenbaserad radbrytning med pixelbaserad mätning i DejaVu Sans.
- Begränsade varje textrad till 160 px inom den 188 px breda textrutan.
- Lade till automatisk fontstorlek 10-15 px utifrån verklig textbredd och höjd.
- Lade till assertions som stoppar build om en rad är för bred.
- Skapade nya versionsnamn för PDF och PNG för att undvika gamla länkar/cache.

## v0.18
- Lade till adaptiv radbrytning för kortens beskrivningstext.
- Lade till automatisk textstorlek mellan 11 och 15 px.
- Centrerade beskrivningstexten vertikalt i textrutan.
- Byggde om äventyrs- och skuggkortens SVG, PDF och PNG-preview.
- Verifierade PDF-filerna genom omrendering.

## v0.17
- Lade till `data/cards/adventure.yaml` och `data/cards/shadow.yaml`.
- Skapade 12 äventyrskort och 8 skuggkort.
- Lade till återanvändbar SVG-kortmall.
- Lade till åtta kortikoner.
- Lade till `scripts/build_cards.py` och kopplade det till huvudbuilden.
- Genererade A4-SVG, PDF och PNG-preview för båda kortlekarna.
- Lade till `docs/card-system.md`.
- Uppdaterade README och projektstatus.

## v0.16
- Delade upp den genererade 2×2-hjältebilden i fyra separata illustrationer.
- Sparade alla bilder som 1600 × 900 px i `assets/heroes/`.
- Uppdaterade `data/heroes/heroes.yaml` till de nya `_wide.png`-filerna.
- Byggde om hjältekortens SVG, PDF och PNG-preview.
- Verifierade att samtliga outputfiler skapades.

## v0.15
- Lade till illustrationsprompter i Markdown och YAML.
- Dokumenterade 16:9-format, filnamn och integrationsflöde.

## v0.14
- Minskade hjältebildernas visningsyta från 344 × 190 px till 324 × 166 px.
- Flyttade bildytan nedåt till y=142.
- Bytte bildpassning från `slice` till `meet` för att undvika avklippta huvuden.
- Gjorde bildramens position, storlek och passning datadriven i `heroes.yaml`.
- Genererade om SVG, PDF och PNG från samma master.

## v0.13
- Lade till fyra separata hjälteillustrationer i `assets/heroes/`.
- Lade till bildreferenser i `data/heroes/heroes.yaml`.
- Uppdaterade hjältekortsmallen med `clipPath` för bildytan.
- Uppdaterade `scripts/build.py` så att bilder bäddas in i master-SVG.
- Genererade nya SVG-, PDF- och PNG-filer från samma illustrerade master.
- Lade till `docs/hero-art-workflow.md`.

## v0.12
- Införde SVG som enda visuella master.
- Lade till riktiga SVG-mallar för spelbräde och hjältekort.
- Ersatte separata generatorer med `scripts/build.py`.
- Genererar PDF och PNG-preview från samma SVG via CairoSVG.
- Lade till A4-PDF för spelbräde och hjältekort.
- Tog bort den separata Pillow-layouten.
- Rensade äldre genererade outputspår.
- Lade till `docs/build-architecture-v1.md`.
- Uppdaterade README och projektstatus.

## v0.11
- Ökade förmågebeskrivningarnas textstorlek i SVG från 16 px till 19 px.
- Ökade motsvarande text i PNG-preview från 10 px till 12 px.
- Ökade radavståndet för förbättrad läsbarhet.
- Gav outputfilerna nya versionsnamn v0.3 för att undvika gamla länkar eller cache.
- Validerade SVG som XML och verifierade nya filhashar.

## v0.10
- Rättade dubbelt `font-family`-attribut i hjältekortens SVG.
- Förstärkte rubrikhierarkin med större kondenserade hjältenamn.
- Lade till tydligare bokstavsavstånd i element- och förmågerubriker.
- Uppdaterade PNG-previewn så att den visuellt matchar SVG-typografin.
- Validerade den genererade SVG-filen som XML.
- Genererade nya hjältekortsfiler v0.2.

## v0.9
- Bytte hjältekortens rubrikfont till DejaVu Sans Condensed Bold.
- Använder DejaVu Sans för brödtext och etiketter.
- Justerade typografisk hierarki och bokstavsavstånd.
- Lade till `docs/typography.md`.
- Genererade om hjältekortens SVG och PNG-preview.

## v0.8
- Delade upp `data/` per komponenttyp.
- Flyttade spelbrädesdata till `data/board/board.yaml`.
- Lade till `data/heroes/heroes.yaml`.
- Lade till `scripts/generate_heroes.py`.
- Skapade fyra individuella hjältekort i SVG.
- Skapade ett A4-ark med fyra hjältekort.
- Skapade PNG-preview av hjältekorten.
- Lade till dokumentation för gemensam komponentarkitektur.
- Uppdaterade README och projektstatus.

## v0.7
- Utökade arbetsytan till A4 liggande.
- Flyttade kartan till vänster för att frigöra en högerspalt.
- Lade mörkerspåret längst till höger.
- Gjorde mörkerspåret datadrivet via `data/board.yaml`.
- Lade till separata SVG-lager för vägar, noder, etiketter, ikoner och mörkerspår.
- Genererade ny komplett SVG-overlay och ny A4-preview.

## v0.6
- Minskade platsnamnsrutorna från 184 × 44 px till 166 × 40 px.
- Centrerade platsnamnen vertikalt i rutorna.
- Tog bort ikonerna ur själva platsnamnsrutorna för att möjliggöra ren vertikal centrering.
- Genererade ny SVG-overlay och ny förhandsvisning.

## v0.5
- Tog bort platsnumren 1–7 från samtliga platscirklar.
- Behöll platsnamnen i etikettrutorna som enda platsidentifiering.
- Genererade ny SVG-overlay och ny förhandsvisning från uppdaterade källfiler.

## v0.4
- Flyttade etiketter för Jordskogen, Verkstaden och Skuggtemplet under respektive markör.
- Tog bort rutan ”Flytta till en angränsande plats längs en markerad väg.” från SVG-overlayen.
- Genererade ny SVG-overlay och nytt slutligt spelbräde från uppdaterade källfiler.

## v0.3

- Lade till `docs/board-layer-architecture.md`.
- Lade till `docs/board-build-guide.md`.
- Dokumenterade exakt hur bakgrund, SVG-overlay och ikoner kombineras.
- Tydliggjorde att `data/board.yaml` är sanningskälla.
- Tydliggjorde vilka filer som är källor och vilka som är genererad output.
- Lade till dokumentation för framtida separata overlay-lager.
- Uppdaterade README och PROJECT_STATUS.

## v0.2

- Tog bort speltext från bakgrundsbilden.
- Införde `data/board.yaml` som sanningskälla.
- Lade till `scripts/generate_board.py`.
- Lade till separata SVG-ikoner.
- Genererade SVG-overlay och sammanslagen förhandsvisning.
