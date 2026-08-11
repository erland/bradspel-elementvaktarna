# Versionspolicy

## Princip

Git-taggen är den primära källan för projektreleaseversionen.

Aktuella källfiler ska därför använda stabila namn och beskriva nuläget, inte bära kopior av releaseversionen.

## Versionsnummer ska finnas här

- Git-taggar och GitHub Releases.
- `CHANGELOG.md`, där versionen identifierar historiska ändringar.
- Historiska playtest- och simuleringsrapporter när versionen är en del av testdatan.
- Genererade releasepaket och release-manifest, eftersom de kan lämna GitHub-kontexten.

## Versionsnummer ska normalt inte finnas här

- Aktiva YAML-källor.
- Aktuella assets och deras filnamn.
- README och projektstatus.
- Spelarregler, QuickStart, FAQ eller A6-källor.
- Mallar och CSS.
- Preview-output.

## Stabil namngivning

Exempel:

```text
assets/backgrounds/board-background-standard.png
assets/backgrounds/board-background-ink-friendly.png
data/simulation/pass.yaml
```

Git-historiken används för att se hur dessa filer såg ut i äldre releaser.

## Release-build

Releaseversionen skickas in från Git-taggen:

```bash
python scripts/package_release.py --version vX.Y.Z
```

GitHub Actions använder taggnamnet automatiskt.
