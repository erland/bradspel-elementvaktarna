# Arbetsflöde för hjälteillustrationer

## Struktur

```text
assets/heroes/
  fire_guardian.png
  water_guardian.png
  wind_guardian.png
  earth_guardian.png
```

`data/heroes/heroes.yaml` refererar till respektive bild:

```yaml
image: assets/heroes/fire_guardian.png
image_fit: cover
image_focus:
  x: 0.5
  y: 0.45
```

## Byggflöde

```text
heroes.yaml
    +
hero-card.svg
    +
assets/heroes/*.png
        ↓
scripts/build.py
        ↓
hero-cards-a4.svg
        ↓
hero-cards-a4.pdf
hero-cards-a4.png
```

Bilderna bäddas in i master-SVG:n och klipps till kortets rundade bildruta med `clipPath`.

## Viktiga principer

- Illustrationerna är separata assets.
- Kortlayouten ligger i SVG-mallen.
- Bildreferenserna ligger i YAML.
- PDF och PNG byggs från samma SVG.
- Bildfilerna ska inte innehålla namn, regler eller annan speltext.
