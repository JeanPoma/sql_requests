# Stratégie de Branches

## Architecture du Repository

Ce repository utilise une **architecture multi-branches** pour supporter deux systèmes de gestion de base de données différents :

### 🔵 Branche `main` - Version MariaDB
- **SGBD** : MariaDB 11
- **Public cible** : Développeurs web, applications classiques
- **Syntaxe** : MariaDB/MySQL
- **Driver Python** : pymysql

### 🟣 Branche `postgres` - Version PostgreSQL
- **SGBD** : PostgreSQL 16
- **Public cible** : Data Scientists, Data Analysts, applications avancées
- **Syntaxe** : PostgreSQL + PL/pgSQL
- **Driver Python** : psycopg2-binary

## ⚠️ Règles Importantes

### ❌ PAS de Merge Entre Branches Principales

**Les branches `main` et `postgres` ne doivent JAMAIS être mergées l'une dans l'autre.**

Ces branches représentent deux versions **parallèles** du même projet, adaptées à des SGBD différents. Elles évoluent indépendamment.

### ✅ Workflows Autorisés

#### Pour des modifications communes (documentation générale, structure de projet)
```bash
# 1. Créer une branche feature depuis main
git checkout main
git checkout -b feature/my-feature

# 2. Faire vos modifications et commit
git add .
git commit -m "feat: my feature"

# 3. Merger dans main
git checkout main
git merge feature/my-feature

# 4. Cherry-pick dans postgres si nécessaire
git checkout postgres
git cherry-pick <commit-hash>
# Adapter manuellement pour PostgreSQL si besoin
```

#### Pour des modifications spécifiques à MariaDB
```bash
git checkout main
git checkout -b feature/mariadb-specific
# Modifications...
git checkout main
git merge feature/mariadb-specific
```

#### Pour des modifications spécifiques à PostgreSQL
```bash
git checkout postgres
git checkout -b feature/postgres-specific
# Modifications...
git checkout postgres
git merge feature/postgres-specific
```

## 🤖 Protection Automatique

Un workflow GitHub Actions (`prevent-cross-branch-prs.yml`) ferme automatiquement toute pull request qui tente de merger :
- `postgres` → `main`
- `main` → `postgres`

## 📋 Checklist pour les Contributeurs

- [ ] Je comprends que `main` et `postgres` sont des branches parallèles
- [ ] Je sais sur quelle branche travailler selon ma modification
- [ ] Si ma modification affecte les deux versions, je sais que je dois l'appliquer séparément sur chaque branche
- [ ] Je ne créerai pas de PR de `postgres` vers `main` ou vice-versa

## 🔗 Branches de Développement

Les branches de développement doivent suivre cette nomenclature :
- `feature/<nom>-mariadb` : pour des features spécifiques MariaDB
- `feature/<nom>-postgres` : pour des features spécifiques PostgreSQL
- `feature/<nom>-common` : pour des features communes (puis cherry-pick sur les deux branches)

## 📞 Questions

Si vous avez des questions sur la stratégie de branches, référez-vous à :
- `README.md` (section "Choisir votre SGBD")
- `docs/MARIADB_VS_POSTGRESQL.md` (guide comparatif)
- `README_POSTGRES.md` (spécificités PostgreSQL)
