# 🐘 Branche PostgreSQL - SQL Learning Project

Cette branche contient une version **PostgreSQL 16** du projet SQL d'apprentissage.

## 🎯 Objectif

Permettre aux utilisateurs de suivre le même parcours d'apprentissage SQL avec **PostgreSQL** au lieu de MariaDB, adaptée aux publics :
- **Data Scientists** : PostgreSQL très utilisé en data science
- **Data Analysts** : Fonctionnalités analytiques avancées
- **Développeurs Backend** : PostgreSQL populaire en production

## 📊 Compatibilité avec la branche principale (MariaDB)

| Composant | Compatibilité | Notes |
|-----------|---------------|-------|
| **Exercices débutants** (q00a-q00h) | ✅ 100% | Aucune modification nécessaire |
| **Exercices intermédiaires** (q01-q10) | ✅ 100% | SQL standard |
| **Exercices avancés** (q11-q20) | ✅ 100% | SQL standard |
| **Vues** (v01-v06) | ✅ Amélioré | v04 utilise MATERIALIZED VIEW native |
| **Procédures** (p01-p06) | ⚠️ Adapté | Réécrits en PL/pgSQL |
| **Triggers** (t01-t06) | ⚠️ Adapté | Architecture fonction + trigger |

**Total : 38 exercices** entièrement fonctionnels avec PostgreSQL !

## 🚀 Installation

### 1. Démarrer PostgreSQL

```bash
docker compose up -d postgres
docker compose up -d adminer
```

### 2. Installer les dépendances Python

```bash
docker compose run -d --name vg-app app bash -lc "pip install -r requirements.txt && tail -f /dev/null"
```

### 3. Charger les données

```bash
docker exec -it vg-app python scripts/load_rawg_csv.py
```

⏱️ Cette étape prend ~5-10 minutes.

### 4. Vérifier l'installation

```bash
docker exec -it vg-app pytest tests/test_00a*.py -v
```

## 🎓 Utilisation

### Workflow identique à la branche MariaDB

```bash
# Éditer un exercice
nano sql/queries/q00a_select_all_games.sql

# Tester
docker exec -it vg-app pytest tests/test_00a_select_all_games.py -v

# Voir la progression
docker exec -it vg-app python scripts/show_progress.py
```

### Adminer (Interface web)

1. Ouvrir **http://localhost:8080**
2. Connexion :
   - **Système** : PostgreSQL
   - **Serveur** : postgres
   - **Utilisateur** : root
   - **Mot de passe** : rootpwd
   - **Base** : vg

## 📚 Différences PostgreSQL vs MariaDB

Consultez **`docs/MARIADB_VS_POSTGRESQL.md`** pour un guide complet des différences syntaxiques.

### Principales différences

#### Procédures stockées (PL/pgSQL)

**MariaDB :**
```sql
DELIMITER //
CREATE PROCEDURE sp_example(IN param INT)
BEGIN
    SELECT * FROM games WHERE id = param;
END //
DELIMITER ;
```

**PostgreSQL :**
```sql
CREATE OR REPLACE FUNCTION sp_example(param INT)
RETURNS TABLE(...)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM games WHERE id = param;
END;
$$;
```

#### Triggers

**MariaDB :**
```sql
DELIMITER //
CREATE TRIGGER trg_validate
BEFORE INSERT ON games
FOR EACH ROW
BEGIN
    IF NEW.year < 1970 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid year';
    END IF;
END //
DELIMITER ;
```

**PostgreSQL :**
```sql
-- 1. Fonction trigger
CREATE OR REPLACE FUNCTION validate_insert()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.year < 1970 THEN
        RAISE EXCEPTION 'Invalid year';
    END IF;
    RETURN NEW;
END;
$$;

-- 2. Trigger
CREATE TRIGGER trg_validate
BEFORE INSERT ON games
FOR EACH ROW
EXECUTE FUNCTION validate_insert();
```

#### Vues matérialisées

**PostgreSQL a un avantage majeur** avec les vues matérialisées natives :

```sql
-- Créer
CREATE MATERIALIZED VIEW genre_stats AS
SELECT genre_id, COUNT(*) as total
FROM game_genres
GROUP BY genre_id;

-- Rafraîchir
REFRESH MATERIALIZED VIEW genre_stats;

-- Rafraîchir sans bloquer
REFRESH MATERIALIZED VIEW CONCURRENTLY genre_stats;
```

MariaDB nécessite une simulation avec table + triggers (beaucoup plus complexe).

## ✨ Avantages PostgreSQL

### Pour ce projet pédagogique

1. **Vues matérialisées natives** (exercice v04)
2. **PL/pgSQL** plus proche du SQL standard
3. **Types avancés** (ARRAY, JSON, RANGE)
4. **Fonctions window** plus complètes
5. **Full-text search** intégré
6. **Extensions** (PostGIS, pg_trgm, etc.)

### En production

- **Conformité SQL** stricte
- **Performance** sur requêtes complexes
- **ACID** rigoureux
- **Communauté** très active
- **Documentation** excellente

## 🧪 Tests

Les tests sont adaptés pour psycopg2 :

```bash
# Tous les tests
docker exec -it vg-app pytest -v

# Tests avancés uniquement
docker exec -it vg-app pytest tests/test_advanced/ -v

# Test spécifique
docker exec -it vg-app pytest tests/test_advanced/test_procedures.py::test_p01_cleanup_old_data_procedure -v
```

## 📖 Documentation

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [PL/pgSQL Guide](https://www.postgresql.org/docs/current/plpgsql.html)
- [Guide comparatif](docs/MARIADB_VS_POSTGRESQL.md) (dans ce repo)

## 🔄 Retour à MariaDB

Pour revenir à MariaDB :

```bash
git checkout claude/improve-sql-project-docs-018UT7ZwFois9A2nwqgUkbNe
docker compose down -v
docker compose up -d mariadb adminer
```

## 🎯 Parcours recommandé

Même parcours que la branche MariaDB :

1. **Débutant** : q00a → q00h (SELECT, WHERE, ORDER BY)
2. **Intermédiaire** : q01 → q10 (Agrégats, Jointures, Windows)
3. **Avancé** : q11 → q20 (Optimisation, CTEs, Quality)
4. **Module avancé** :
   - Vues (v01-v06)
   - Procédures PL/pgSQL (p01-p06)
   - Triggers (t01-t06)

## 💡 Conseils spécifiques PostgreSQL

### Utiliser psql (CLI PostgreSQL)

```bash
docker exec -it postgres psql -U root -d vg
```

Commandes utiles psql :
- `\dt` : Lister les tables
- `\dv` : Lister les vues
- `\df` : Lister les fonctions
- `\di` : Lister les index
- `\d games` : Décrire une table
- `\q` : Quitter

### EXPLAIN ANALYZE

PostgreSQL a un EXPLAIN plus détaillé :

```sql
EXPLAIN ANALYZE
SELECT * FROM games WHERE year = 2020;
```

### Extensions utiles

```sql
-- Activer pg_trgm (similarité de texte)
CREATE EXTENSION pg_trgm;

-- Activer uuid
CREATE EXTENSION "uuid-ossp";
```

## 🏆 Compétences acquises

À la fin de ce parcours PostgreSQL, vous maîtriserez :

- ✅ SQL standard (compatible multi-SGBD)
- ✅ **PL/pgSQL** (langage procédural PostgreSQL)
- ✅ **Vues matérialisées** natives
- ✅ **Triggers avec fonctions** (architecture PostgreSQL)
- ✅ **Types avancés** PostgreSQL
- ✅ **Optimisation** avec EXPLAIN ANALYZE
- ✅ **Conformité SQL** stricte

**Vous serez prêt pour des postes en Data Engineering, Data Analytics, et Backend Development avec PostgreSQL !** 🚀

---

**Questions ?** Consultez `docs/MARIADB_VS_POSTGRESQL.md` ou la documentation officielle PostgreSQL.
