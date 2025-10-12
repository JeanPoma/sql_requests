# 🎮 Cours SQL + TDD (MariaDB + Python) — Dataset RAWG (Kaggle)

Ce projet propose une progression TDD pour apprendre SQL avec des **données réelles** (dataset RAWG par jummyegg).

## Prérequis
- Docker / Docker Compose
- Fichier Kaggle: placez `rawg_games.csv` dans `data/` (dézippé)

## Installation
1. Démarrer la base et créer le schéma
   ```bash
   docker compose up -d mariadb
   ```
2. Charger le dataset dans MariaDB
   ```bash
   docker compose run --rm app python scripts/load_rawg_csv.py
   ```
3. Lancer la suite de tests (TDD)
   ```bash
   docker compose run --rm app pytest -q
   ```

## Où écrire le SQL ?
- Les **requêtes à implémenter** sont dans `sql/queries/*.sql`.
- Chaque fichier **ne contient que des consignes**. Remplacez les consignes par **votre requête SQL** (une seule requête par fichier).
- Relancez `pytest` pour voir les tests passer/échouer.

## Conseils pédagogiques
- Travaillez en binôme: l’un lit les tests, l’autre propose une requête.
- Commencez par `q01` → `q05` (bases, agrégats, fenêtres), puis la suite selon votre rythme.
- Pour les avancés: fenêtre (LEAD/LAG), percentiles, CTEs, EXPLAIN & index, gaps & islands, vues (fichier BONUS).

## Dépannage
- Si `games` est vide: vérifiez `data/rawg_games.csv` et relancez `load_rawg_csv.py`.
- Si les fenêtres échouent: assurez-vous d’utiliser MariaDB ≥ 10.5.
- Si EXPLAIN n’utilise pas l’index: rendez la clause WHERE plus sélective et vérifiez `idx_games_year`.

## Licence & Données
- Dataset: RAWG (agrégé par jummyegg sur Kaggle). Respectez les conditions d’usage de la source.
