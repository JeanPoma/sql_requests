## 📚 Ressources SQL - Guide Complet

Ce document regroupe toutes les ressources pour progresser en SQL, organisées par niveau et par concept.

---

## 🎯 Par Niveau de Difficulté

### 🟢 **Niveau Débutant** (Bases du SQL)

#### Tutoriels recommandés
1. **SQL Zoo - Bases**
   - [Tutorial 0 : SELECT basics](https://sqlzoo.net/wiki/SELECT_basics) - Premières requêtes SELECT
   - [Tutorial 1 : SELECT name](https://sqlzoo.net/wiki/SELECT_names) - WHERE, LIKE, filtres
   - [Tutorial 2 : SELECT from World](https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial) - ORDER BY, LIMIT
   - [Tutorial 3 : SELECT from Nobel](https://sqlzoo.net/wiki/SELECT_from_Nobel_Tutorial) - Filtres avancés

2. **Documentation MariaDB**
   - [Getting Started with SQL](https://mariadb.com/kb/en/getting-started-with-sql/) - Introduction officielle
   - [SELECT Statement](https://mariadb.com/kb/en/select/) - Syntaxe complète du SELECT

3. **Tutoriels interactifs**
   - [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial/) - Excellent pour débutants
   - [W3Schools SQL Tutorial](https://www.w3schools.com/sql/) - Référence rapide

#### Exercices complémentaires
- **SQLZoo** : Tutorials 0-3
- **LeetCode** : [Easy SQL Problems](https://leetcode.com/problemset/database/?difficulty=EASY)
- **HackerRank** : [Basic Select](https://www.hackerrank.com/domains/sql?filters%5Bsubdomains%5D%5B%5D=select)

---

### 🟡 **Niveau Intermédiaire** (Agrégats, Jointures, Window Functions)

#### Tutoriels recommandés
1. **SQL Zoo - Intermédiaire**
   - [Tutorial 5 : SUM and COUNT](https://sqlzoo.net/wiki/SUM_and_COUNT) - Fonctions d'agrégation, GROUP BY
   - [Tutorial 6 : JOIN](https://sqlzoo.net/wiki/The_JOIN_operation) - INNER JOIN, LEFT JOIN
   - [Tutorial 7 : More JOIN](https://sqlzoo.net/wiki/More_JOIN_operations) - Jointures complexes
   - [Tutorial 8 : Using Null](https://sqlzoo.net/wiki/Using_Null) - Gestion des NULL
   - [Tutorial 8+ : Window Functions](https://sqlzoo.net/wiki/Window_functions) - RANK, DENSE_RANK
   - [Tutorial 9 : Self JOIN & Window LAG](https://sqlzoo.net/wiki/Window_LAG) - Fonctions avancées

2. **Documentation MariaDB**
   - [Aggregate Functions](https://mariadb.com/kb/en/aggregate-functions/) - COUNT, SUM, AVG, MIN, MAX
   - [Joins Overview](https://mariadb.com/kb/en/joins-overview/) - Types de jointures
   - [Window Functions](https://mariadb.com/kb/en/window-functions/) - Documentation complète

3. **Articles approfondis**
   - [Understanding SQL Window Functions](https://www.windowfunctions.com/) - Guide interactif
   - [SQL JOINs Explained](https://www.sql-join.com/) - Visualisation des JOIN

#### Exercices complémentaires
- **SQLZoo** : Tutorials 5-9
- **LeetCode** : [Medium SQL Problems](https://leetcode.com/problemset/database/?difficulty=MEDIUM)
- **HackerRank** : [Aggregation](https://www.hackerrank.com/domains/sql?filters%5Bsubdomains%5D%5B%5D=aggregation) & [Joins](https://www.hackerrank.com/domains/sql?filters%5Bsubdomains%5D%5B%5D=join)

---

### 🔴 **Niveau Avancé** (Optimisation, Sous-requêtes, Patterns)

#### Tutoriels recommandés
1. **SQL Zoo - Avancé**
   - [Tutorial 9+ : COVID-19](https://sqlzoo.net/wiki/Window_function) - Cas d'usage réels avec window functions
   - [Tutorial 10 : Self JOIN](https://sqlzoo.net/wiki/Self_join) - Auto-jointures

2. **Documentation MariaDB**
   - [Query Optimizations](https://mariadb.com/kb/en/query-optimizations/) - Optimiser vos requêtes
   - [EXPLAIN](https://mariadb.com/kb/en/explain/) - Analyser les plans d'exécution
   - [Indexes](https://mariadb.com/kb/en/optimization-and-indexes/) - Comprendre les index
   - [Common Table Expressions (CTE)](https://mariadb.com/kb/en/with/) - Sous-requêtes nommées

3. **Patterns SQL avancés**
   - [Gaps and Islands](https://www.red-gate.com/simple-talk/databases/sql-server/t-sql-programming-sql-server/gaps-islands-problem/) - Séquences continues
   - [Running Totals and Moving Averages](https://www.sqltutorial.org/sql-window-functions/sql-window-function-sample-database/) - Calculs cumulés
   - [Hierarchical Queries](https://learnsql.com/blog/do-it-in-sql-recursive-cte/) - Requêtes récursives

#### Exercices complémentaires
- **SQLZoo** : Tous les tutorials 9+
- **LeetCode** : [Hard SQL Problems](https://leetcode.com/problemset/database/?difficulty=HARD)
- **HackerRank** : [Advanced Select](https://www.hackerrank.com/domains/sql?filters%5Bsubdomains%5D%5B%5D=advanced-select)

---

## 🧩 Par Concept SQL

### 📊 **SELECT, WHERE, ORDER BY** (Bases)
**Exercices du projet** : q00a, q00b, q00c, q00d, q00e, q00f

**Ressources** :
- [SQLZoo Tutorial 0-1](https://sqlzoo.net/wiki/SELECT_basics)
- [MariaDB SELECT](https://mariadb.com/kb/en/select/)
- [W3Schools SQL SELECT](https://www.w3schools.com/sql/sql_select.asp)

**Concepts clés** :
- `SELECT *` vs colonnes spécifiques
- `WHERE` avec `=`, `>`, `<`, `>=`, `<=`, `<>`
- `AND`, `OR`, `IN`, `BETWEEN`, `LIKE`
- `ORDER BY ASC/DESC`
- `LIMIT` et `OFFSET`

---

### 🔢 **Fonctions d'Agrégation** (GROUP BY, HAVING)
**Exercices du projet** : q00g, q00h, q03, q04

**Ressources** :
- [SQLZoo Tutorial 5](https://sqlzoo.net/wiki/SUM_and_COUNT)
- [MariaDB Aggregate Functions](https://mariadb.com/kb/en/aggregate-functions/)
- [SQL GROUP BY Explained](https://www.sqlshack.com/sql-group-by-clause/)

**Concepts clés** :
- `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`
- `GROUP BY` simple et multi-colonnes
- `HAVING` vs `WHERE`
- `COUNT(*)` vs `COUNT(column)`

---

### 🔗 **Jointures** (INNER JOIN, LEFT JOIN)
**Exercices du projet** : q03, q04, q08, q09, q11

**Ressources** :
- [SQLZoo Tutorial 6-7](https://sqlzoo.net/wiki/The_JOIN_operation)
- [MariaDB Joins Overview](https://mariadb.com/kb/en/joins-overview/)
- [Visual JOIN Guide](https://joins.spathon.com/)

**Concepts clés** :
- `INNER JOIN` (intersections)
- `LEFT JOIN` (tout à gauche + correspondances)
- `RIGHT JOIN` (tout à droite + correspondances)
- Jointures multiples
- Tables de liaison (many-to-many)

---

### 🪟 **Window Functions** (RANK, LAG, LEAD)
**Exercices du projet** : q05, q06, q07, q13, q18, q19

**Ressources** :
- [SQLZoo Tutorial 8+](https://sqlzoo.net/wiki/Window_functions)
- [MariaDB Window Functions](https://mariadb.com/kb/en/window-functions/)
- [windowfunctions.com](https://www.windowfunctions.com/) - Guide interactif

**Concepts clés** :
- `RANK()`, `DENSE_RANK()`, `ROW_NUMBER()`
- `PARTITION BY` (grouper sans perdre les lignes)
- `LAG()` et `LEAD()` (accéder aux lignes précédentes/suivantes)
- `OVER()` clause
- Window frames : `ROWS`, `RANGE`
- Moyennes mobiles (rolling averages)

---

### 📝 **CTEs (Common Table Expressions)**
**Exercices du projet** : q05, q06, q08, q10, q19

**Ressources** :
- [SQLZoo Tutorial 9](https://sqlzoo.net/wiki/Window_LAG)
- [MariaDB WITH clause](https://mariadb.com/kb/en/with/)
- [CTE Tutorial](https://learnsql.com/blog/what-is-common-table-expression/)

**Concepts clés** :
- Syntaxe `WITH nom AS (SELECT ...)`
- CTEs multiples
- CTEs récursives (avancé)
- Lisibilité vs sous-requêtes

---

### 🔍 **Sous-requêtes** (Subqueries)
**Exercices du projet** : q11

**Ressources** :
- [MariaDB Subqueries](https://mariadb.com/kb/en/subqueries/)
- [Subquery vs JOIN](https://learnsql.com/blog/subquery-vs-join/)

**Concepts clés** :
- Sous-requêtes scalaires (une valeur)
- Sous-requêtes dans `WHERE`
- Sous-requêtes corrélées
- `IN`, `EXISTS`, `ANY`, `ALL`

---

### 🔄 **UNION / UNION ALL**
**Exercices du projet** : q12, q15

**Ressources** :
- [MariaDB UNION](https://mariadb.com/kb/en/union/)
- [UNION vs UNION ALL](https://www.sqlshack.com/sql-union-vs-union-all/)

**Concepts clés** :
- Combiner des résultats homogènes
- `UNION` (élimine doublons) vs `UNION ALL` (garde tout)
- Colonnes alignées en nombre et type

---

### ⚡ **Optimisation & Index**
**Exercices du projet** : q16, q17

**Ressources** :
- [MariaDB Query Optimizations](https://mariadb.com/kb/en/query-optimizations/)
- [MariaDB EXPLAIN](https://mariadb.com/kb/en/explain/)
- [Index Optimization](https://mariadb.com/kb/en/optimization-and-indexes/)
- [Use The Index, Luke!](https://use-the-index-luke.com/) - Livre en ligne gratuit

**Concepts clés** :
- `EXPLAIN` pour analyser les requêtes
- Index : B-Tree, clés primaires, clés étrangères
- Sélectivité des filtres
- Éviter les full table scans
- Ordre des colonnes dans les index

---

### 🧹 **Data Quality**
**Exercices du projet** : q14, q15, q20

**Ressources** :
- [SQL Best Practices](https://www.sqlshack.com/sql-best-practices/)
- [Data Cleaning with SQL](https://mode.com/sql-tutorial/data-cleaning/)

**Concepts clés** :
- Détection de doublons (`GROUP BY` + `HAVING`)
- Gestion des `NULL`
- Contrôles de cohérence
- Percentiles et distributions

---

## 🛠️ Outils & Environnements de Pratique

### Environnements en ligne
- [SQL Fiddle](http://sqlfiddle.com/) - Testez vos requêtes en ligne
- [DB Fiddle](https://www.db-fiddle.com/) - Compatible MariaDB
- [SQLite Online](https://sqliteonline.com/) - SQLite dans le navigateur

### Extensions & IDE
- [DBeaver](https://dbeaver.io/) - Client SQL gratuit et complet
- [MySQL Workbench](https://www.mysql.com/products/workbench/) - Client officiel MySQL/MariaDB
- [VS Code extension](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) - SQLTools

---

## 📖 Cheatsheets & Références

### Cheatsheets SQL
- [SQL Cheat Sheet (PDF)](https://learnsql.com/blog/sql-basics-cheat-sheet/) - LearnSQL
- [SQL Commands Cheat Sheet](https://www.sqltutorial.org/sql-cheat-sheet/) - SQLTutorial
- [MariaDB Quick Reference](https://mariadb.com/kb/en/sql-statements/) - Documentation officielle

### Livres recommandés
- **SQL Queries for Mere Mortals** - John Viescas (débutant à intermédiaire)
- **The Art of SQL** - Stéphane Faroult (avancé)
- **SQL Performance Explained** - Markus Winand (optimisation)

### Vidéos & Cours
- [Khan Academy - Intro to SQL](https://www.khanacademy.org/computing/computer-programming/sql) - Gratuit, interactif
- [Codecademy SQL Course](https://www.codecademy.com/learn/learn-sql) - Cours structuré
- [SQL Tutorial - Full Database Course](https://www.youtube.com/watch?v=HXV3zeQKqGY) - YouTube (4h)

---

## 🏆 Plateformes d'Exercices

### Par difficulté croissante
1. **SQLZoo** ([sqlzoo.net](https://sqlzoo.net/)) - Le meilleur pour débuter, très progressif
2. **W3Schools SQL** ([w3schools.com/sql](https://www.w3schools.com/sql/)) - Exercices simples
3. **HackerRank SQL** ([hackerrank.com/domains/sql](https://www.hackerrank.com/domains/sql)) - Défis structurés
4. **LeetCode Database** ([leetcode.com/problemset/database](https://leetcode.com/problemset/database/)) - Style technique d'interview
5. **Mode Analytics SQL School** ([mode.com/sql-tutorial](https://mode.com/sql-tutorial/)) - Cas d'usage réels
6. **StrataScratch** ([stratascratch.com](https://www.stratascratch.com/)) - Questions d'entretien réelles

### Compétitions & Challenges
- [Advent of Code](https://adventofcode.com/) - Certains puzzles solvables en SQL
- [SQL Murder Mystery](https://mystery.knightlab.com/) - Enquête policière en SQL

---

## 🎯 Conseils pour Progresser

### Pour les débutants
1. ✅ Commencez par SQLZoo tutorials 0-3
2. ✅ Faites TOUS les exercices q00a-q00h de ce projet
3. ✅ Utilisez Adminer pour visualiser les données
4. ✅ N'hésitez pas à tester vos requêtes plusieurs fois
5. ✅ Lisez les messages d'erreur, ils sont instructifs

### Pour les intermédiaires
1. ✅ Maîtrisez GROUP BY et les jointures avant d'attaquer les window functions
2. ✅ Faites SQLZoo tutorials 5-9
3. ✅ Dessinez les schémas de jointure sur papier
4. ✅ Comprenez la différence entre RANK et DENSE_RANK
5. ✅ Utilisez des CTEs pour structurer vos requêtes complexes

### Pour les avancés
1. ✅ Utilisez EXPLAIN systématiquement
2. ✅ Comprenez les plans d'exécution
3. ✅ Lisez "Use The Index, Luke!"
4. ✅ Pratiquez les patterns avancés (Gaps & Islands, etc.)
5. ✅ Testez différentes approches et comparez les performances

---

## 🆘 Ressources de Débogage

### Erreurs courantes
- **Unknown column** → Vérifiez l'orthographe et les alias de tables
- **Ambiguous column** → Préfixez avec le nom de table (ex: `games.id`)
- **Column not in GROUP BY** → Ajoutez la colonne au GROUP BY ou utilisez un agrégat
- **Subquery returns more than 1 row** → Utilisez `IN` au lieu de `=`

### Où chercher de l'aide
- [Stack Overflow SQL](https://stackoverflow.com/questions/tagged/sql) - Q&A communautaire
- [MariaDB Knowledge Base](https://mariadb.com/kb/en/) - Documentation officielle
- [Database Administrators Stack Exchange](https://dba.stackexchange.com/) - Questions avancées

---

**💡 Astuce finale** : La meilleure façon d'apprendre SQL est de **pratiquer régulièrement** avec des données réelles. Ce projet vous donne exactement cela ! 🚀
