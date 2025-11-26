# 🔄 Guide de Migration : MariaDB → PostgreSQL

Ce document liste toutes les différences entre MariaDB et PostgreSQL rencontrées dans ce projet.

## 📋 Table des matières

- [Syntaxe SQL de base](#syntaxe-sql-de-base)
- [Fonctions d'agrégation](#fonctions-dagrégation)
- [Vues](#vues)
- [Procédures stockées](#procédures-stockées)
- [Triggers](#triggers)
- [Index et optimisation](#index-et-optimisation)

---

## Syntaxe SQL de base

### ✅ Compatible sans modification

Ces concepts fonctionnent de manière identique :
- `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `OFFSET`
- `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN`
- `GROUP BY`, `HAVING`
- `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`
- `DISTINCT`, `UNION`, `UNION ALL`
- `RANK()`, `DENSE_RANK()`, `ROW_NUMBER()`, `LAG()`, `LEAD()`
- `PARTITION BY`, `OVER`
- CTEs (`WITH ... AS`)
- `CASE WHEN ... THEN ... END`

### ⚠️ Différences mineures

| Concept | MariaDB | PostgreSQL |
|---------|---------|------------|
| **Concaténation de chaînes** | `GROUP_CONCAT(col)` | `STRING_AGG(col, ',')` |
| **Concaténation avec séparateur** | `GROUP_CONCAT(col SEPARATOR '|')` | `STRING_AGG(col, '\|')` |
| **Auto-increment** | `AUTO_INCREMENT` | `SERIAL` ou `GENERATED ALWAYS AS IDENTITY` |
| **Quotes pour identifiants** | `` `table` `` (backticks) | `"table"` (double quotes) |
| **Limite TOP N** | `LIMIT 10` | `LIMIT 10` (identique) |
| **ILIKE (case insensitive)** | N/A (utiliser `LOWER()`) | `WHERE col ILIKE '%pattern%'` |

### Exemple : GROUP_CONCAT → STRING_AGG

**MariaDB :**
```sql
SELECT
    genre,
    GROUP_CONCAT(name ORDER BY name SEPARATOR ', ') as games
FROM games
GROUP BY genre;
```

**PostgreSQL :**
```sql
SELECT
    genre,
    STRING_AGG(name, ', ' ORDER BY name) as games
FROM games
GROUP BY genre;
```

---

## Fonctions d'agrégation

### Fonctions spécifiques

| Fonction | MariaDB | PostgreSQL |
|----------|---------|------------|
| **Concaténation** | `GROUP_CONCAT()` | `STRING_AGG()` ou `ARRAY_AGG()` |
| **Médiane** | Pas native (utiliser `PERCENTILE_CONT`) | `PERCENTILE_CONT(0.5)` |
| **Array** | Non supporté | `ARRAY_AGG(col)` |

---

## Vues

### ✅ Vues simples : Identiques

Les vues simples fonctionnent de la même manière.

### 🔄 Vues matérialisées : Natif dans PostgreSQL !

**MariaDB** (simulation) :
```sql
-- Créer la table
CREATE TABLE genre_stats AS
SELECT genre_id, COUNT(*) as total
FROM game_genres
GROUP BY genre_id;

-- Maintenir avec des triggers
CREATE TRIGGER update_stats AFTER INSERT ON game_genres
FOR EACH ROW
BEGIN
    -- mise à jour manuelle
END;
```

**PostgreSQL** (natif) :
```sql
-- Créer la vue matérialisée
CREATE MATERIALIZED VIEW genre_stats AS
SELECT genre_id, COUNT(*) as total
FROM game_genres
GROUP BY genre_id;

-- Rafraîchir
REFRESH MATERIALIZED VIEW genre_stats;

-- Rafraîchir sans bloquer les lectures
REFRESH MATERIALIZED VIEW CONCURRENTLY genre_stats;
```

**Avantage PostgreSQL** : Vues matérialisées natives avec gestion automatique !

---

## Procédures stockées

### 🔴 Différences MAJEURES

PostgreSQL utilise **PL/pgSQL**, une syntaxe différente de SQL procédural MariaDB.

### Différences de syntaxe

| Concept | MariaDB | PostgreSQL |
|---------|---------|------------|
| **Délimiteur** | `DELIMITER //` ... `DELIMITER ;` | `$$` ... `$$` |
| **Langage** | Implicite (SQL) | `LANGUAGE plpgsql` (obligatoire) |
| **Déclaration** | `DECLARE var TYPE;` | `DECLARE var TYPE;` (avant BEGIN) |
| **Affectation** | `SET var = valeur;` | `var := valeur;` |
| **IF/ELSE** | `ELSEIF` | `ELSIF` |
| **SELECT INTO** | `SELECT col INTO var FROM ...` | Identique |
| **RETURN** | Optionnel pour procédures | `RETURN NEW;` (triggers) |

### Exemple : Procédure simple

**MariaDB :**
```sql
DELIMITER //
CREATE PROCEDURE sp_get_total(OUT total INT)
BEGIN
    SELECT COUNT(*) INTO total FROM games;
END //
DELIMITER ;

-- Appel
CALL sp_get_total(@total);
SELECT @total;
```

**PostgreSQL :**
```sql
CREATE OR REPLACE PROCEDURE sp_get_total(OUT total INT)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT COUNT(*) INTO total FROM games;
END;
$$;

-- Appel
CALL sp_get_total(NULL);
```

### Exemple : Procédure avec IF/ELSE

**MariaDB :**
```sql
DELIMITER //
CREATE PROCEDURE sp_classify(IN score INT, OUT label VARCHAR(50))
BEGIN
    IF score >= 90 THEN
        SET label = 'Excellent';
    ELSEIF score >= 70 THEN
        SET label = 'Bon';
    ELSE
        SET label = 'Moyen';
    END IF;
END //
DELIMITER ;
```

**PostgreSQL :**
```sql
CREATE OR REPLACE PROCEDURE sp_classify(score INT, OUT label VARCHAR(50))
LANGUAGE plpgsql
AS $$
BEGIN
    IF score >= 90 THEN
        label := 'Excellent';
    ELSIF score >= 70 THEN
        label := 'Bon';
    ELSE
        label := 'Moyen';
    END IF;
END;
$$;
```

---

## Triggers

### 🔴 Différences MAJEURES

PostgreSQL nécessite une **fonction séparée** pour chaque trigger.

### Architecture

| Aspect | MariaDB | PostgreSQL |
|--------|---------|------------|
| **Structure** | Trigger contient le code | Trigger + Fonction séparée |
| **Langage** | SQL procédural inline | PL/pgSQL dans fonction |
| **SIGNAL** | `SIGNAL SQLSTATE '45000'` | `RAISE EXCEPTION` |
| **RETURN** | Non nécessaire | `RETURN NEW;` ou `RETURN NULL;` |

### Exemple : Trigger BEFORE INSERT

**MariaDB :**
```sql
DELIMITER //
CREATE TRIGGER trg_validate_insert
BEFORE INSERT ON games
FOR EACH ROW
BEGIN
    IF NEW.year < 1970 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid year';
    END IF;
END //
DELIMITER ;
```

**PostgreSQL :**
```sql
-- 1. Créer la fonction trigger
CREATE OR REPLACE FUNCTION validate_insert()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.year < 1970 THEN
        RAISE EXCEPTION 'Invalid year';
    END IF;
    RETURN NEW;  -- OBLIGATOIRE !
END;
$$;

-- 2. Créer le trigger
CREATE TRIGGER trg_validate_insert
BEFORE INSERT ON games
FOR EACH ROW
EXECUTE FUNCTION validate_insert();
```

### Exemple : Trigger AFTER INSERT

**MariaDB :**
```sql
DELIMITER //
CREATE TRIGGER trg_audit
AFTER INSERT ON games
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (game_id, operation, op_time)
    VALUES (NEW.id, 'INSERT', NOW());
END //
DELIMITER ;
```

**PostgreSQL :**
```sql
-- 1. Fonction
CREATE OR REPLACE FUNCTION audit_insert()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO audit_log (game_id, operation, op_time)
    VALUES (NEW.id, 'INSERT', NOW());
    RETURN NEW;
END;
$$;

-- 2. Trigger
CREATE TRIGGER trg_audit
AFTER INSERT ON games
FOR EACH ROW
EXECUTE FUNCTION audit_insert();
```

---

## Index et optimisation

### ✅ Index standards : Identiques

```sql
CREATE INDEX idx_name ON games(name);
CREATE INDEX idx_year ON games(year);
```

### 🔄 Index avancés : PostgreSQL plus riche

| Type d'index | MariaDB | PostgreSQL |
|--------------|---------|------------|
| **B-Tree** | ✅ (par défaut) | ✅ (par défaut) |
| **Hash** | ✅ | ✅ |
| **Full-text** | ✅ (FULLTEXT) | ✅ (GIN, tsvector) |
| **Partial** | ❌ | ✅ `WHERE clause` |
| **Expression** | ❌ | ✅ `ON (LOWER(name))` |
| **GIN** | ❌ | ✅ (JSON, arrays) |
| **GiST** | ❌ | ✅ (géospatial) |

**Exemple PostgreSQL (index partiel) :**
```sql
-- Index uniquement sur les jeux notés
CREATE INDEX idx_rated_games ON games(metacritic)
WHERE metacritic IS NOT NULL;
```

### EXPLAIN : Sortie différente

**MariaDB :**
```sql
EXPLAIN SELECT * FROM games WHERE year = 2020;
```
Sortie : `type`, `possible_keys`, `key`, `rows`, `Extra`

**PostgreSQL :**
```sql
EXPLAIN ANALYZE SELECT * FROM games WHERE year = 2020;
```
Sortie : Plan d'exécution détaillé avec temps réels

---

## 🎯 Résumé des impacts

| Niveau | Impact | Effort |
|--------|--------|--------|
| **Exercices débutants (q00a-q00h)** | ✅ Aucun | 0h |
| **Exercices intermédiaires (q01-q10)** | ⚠️ Faible (GROUP_CONCAT) | 1-2h |
| **Exercices avancés (q11-q20)** | ⚠️ Moyen (EXPLAIN) | 2-3h |
| **Vues (v01-v06)** | ⚠️ Moyen (vues matérialisées) | 3-4h |
| **Procédures (p01-p06)** | 🔴 MAJEUR (PL/pgSQL) | 8-10h |
| **Triggers (t01-t06)** | 🔴 MAJEUR (fonctions séparées) | 8-10h |

---

## 📚 Ressources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PL/pgSQL Documentation](https://www.postgresql.org/docs/current/plpgsql.html)
- [PostgreSQL vs MySQL Comparison](https://www.postgresqltutorial.com/)
- [Migrating from MySQL to PostgreSQL](https://wiki.postgresql.org/wiki/Converting_from_other_Databases_to_PostgreSQL)
