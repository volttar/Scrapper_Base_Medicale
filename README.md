# Scrapper Base Médicale

Ce projet fournit une base **asynchrone et modulaire** pour scraper des sources médicales
(ANSM, HAS, Thériaque, DrugBank, Vidal, etc.). L'objectif est d'avoir un pipeline performant,
respectueux des sites (rate limiting, retries), et extensible par sources.

> ⚠️ Vérifiez les CGU/robots.txt de chaque site avant d'activer un scraper en production.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage rapide

```bash
scrapper-med --site ansm --site has --output output/data.jsonl
```

Par défaut, chaque source utilise un **scraper dédié** dans `scrapper_base/scrapers/`.
Les parseurs sont séparés dans `scrapper_base/parsers/`.

## Architecture

- `scrapper_base/fetcher.py` : client HTTP asynchrone, retries, rate limiting.
- `scrapper_base/scrapers/` : scrapers par site.
- `scrapper_base/parsers/` : parse HTML -> objets normalisés.
- `scrapper_base/storage.py` : sortie JSONL.

## Ajouter une source

1. Créez un scraper dans `scrapper_base/scrapers/`.
2. Ajoutez un parseur dans `scrapper_base/parsers/`.
3. Enregistrez la source dans `scrapper_base/registry.py`.

## Notes de conformité

- Respecter les quotas et délais.
- Prévoir un cache si vous interrogez des milliers de pages.
- Documenter la finalité du scraping et conserver les preuves d’autorisation si besoin.

