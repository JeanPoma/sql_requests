# 🗺️ Parcours d'Apprentissage SQL

Ce document cartographie tous les exercices du projet avec les ressources SQLZoo correspondantes et les concepts SQL associés.

---

## 📋 Vue d'ensemble

| Niveau | Exercices | Durée estimée | Prérequis |
|--------|-----------|---------------|-----------|
| 🟢 Débutant | q00a → q00h | 2-3h | Aucun |
| 🟡 Intermédiaire | q01 → q10 | 4-6h | Niveau débutant |
| 🔴 Avancé | q11 → q20 + BONUS | 6-8h | Niveau intermédiaire |

**Durée totale estimée** : 12-17 heures de pratique

---

## 🟢 Niveau Débutant (2-3h)

### q00a : SELECT simple (toutes colonnes)
**Concepts** : `SELECT *`, `LIMIT`  
**SQLZoo** : [Tutorial 0 - SELECT basics](https://sqlzoo.net/wiki/SELECT_basics)  
**Prérequis** : Aucun  
**Objectif** : Comprendre la syntaxe de base de SELECT et limiter les résultats

---

### q00b : SELECT avec colonnes spécifiques
**Concepts** : `SELECT col1, col2`, choix de colonnes  
**SQLZoo** : [Tutorial 0 - SELECT basics](https://sqlzoo.net/wiki/SELECT_basics)  
**Prérequis** : q00a  
**Objectif** : Sélectionner uniquement les colonnes nécessaires

---

### q00c : WHERE simple (condition unique)
**Concepts** : `WHERE`, conditions de base (`=`, `>`, `<`)  
**SQLZoo** : [Tutorial 1 - SELECT names](https://sqlzoo.net/wiki/SELECT_names)  
**Prérequis** : q00b  
**Objectif** : Filtrer les résultats avec une condition simple

---

### q00d : WHERE avec AND/OR
**Concepts** : `AND`, `OR`, `IN`, conditions multiples  
**SQLZoo** : [Tutorial 1 - SELECT names](https://sqlzoo.net/wiki/SELECT_names)  
**Prérequis** : q00c  
**Objectif** : Combiner plusieurs conditions de filtrage

---

### q00e : ORDER BY (tri)
**Concepts** : `ORDER BY ASC/DESC`, tri multi-colonnes  
**SQLZoo** : [Tutorial 1 - SELECT names](https://sqlzoo.net/wiki/SELECT_names)  
**Prérequis** : q00d  
**Objectif** : Trier les résultats selon plusieurs critères

---

### q00f : LIMIT et OFFSET (pagination)
**Concepts** : `LIMIT`, `OFFSET`, pagination  
**SQLZoo** : [Tutorial 1 - SELECT names](https://sqlzoo.net/wiki/SELECT_names)  
**Prérequis** : q00e  
**Objectif** : Paginer les résultats pour afficher une partie des données

---

### q00g : COUNT (agrégat basique)
**Concepts** : `COUNT()`, agrégats simples  
**SQLZoo** : [Tutorial 2 - SELECT from World](https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial)  
**Prérequis** : q00f  
**Objectif** : Compter le nombre de lignes dans un résultat

---

### q00h : AVG, MIN, MAX (agrégats)
**Concepts** : `AVG()`, `MIN()`, `MAX()`, `ROUND()`  
**SQLZoo** : [Tutorial 2 - SELECT from World](https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial)  
**Prérequis** : q00g  
**Objectif** : Calculer des statistiques simples sur les données

---

## 🟡 Niveau Intermédiaire (4-6h)

### q01 : TOP N avec ORDER BY et LIMIT
**Concepts** : Tri complexe multi-colonnes, TOP N  
**SQLZoo** : [Tutorial 2 - SELECT from World](https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial)  
**Prérequis** : Niveau débutant complet  
**Objectif** : Obtenir le classement des N meilleurs éléments

**Compétences acquises** :
- Maîtriser les critères de tri multiples
- Gérer les égalités dans un classement

---

### q02 : Filtres multiples + tri
**Concepts** : Conditions combinées, `IS NOT NULL`  
**SQLZoo** : [Tutorial 2 - SELECT from World](https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial)  
**Prérequis** : q01  
**Objectif** : Filtrer sur plusieurs critères et trier

**Compétences acquises** :
- Combiner des filtres temporels et de qualité
- Exclure les valeurs nulles

---

### q03 : GROUP BY multi-colonnes
**Concepts** : `GROUP BY`, agrégats avec plusieurs dimensions, `HAVING`  
**SQLZoo** : [Tutorial 5 - SUM and COUNT](https://sqlzoo.net/wiki/SUM_and_COUNT)  
**Prérequis** : q02  
**Objectif** : Agréger des données selon plusieurs critères

**Compétences acquises** :
- Grouper par plusieurs colonnes
- Utiliser HAVING pour filtrer les agrégats
- Faire des jointures avec tables de liaison (many-to-many)

---

### q04 : GROUP BY avec agrégats multiples
**Concepts** : `COUNT()`, `AVG()`, groupe temporel (année)  
**SQLZoo** : [Tutorial 5 - SUM and COUNT](https://sqlzoo.net/wiki/SUM_and_COUNT)  
**Prérequis** : q03  
**Objectif** : Analyser la performance par groupes temporels

**Compétences acquises** :
- Combiner plusieurs métriques dans un GROUP BY
- Analyser des tendances temporelles

---

### q05 : Window Functions (RANK/DENSE_RANK)
**Concepts** : `RANK()`, `DENSE_RANK()`, `PARTITION BY`, `OVER()`  
**SQLZoo** : [Tutorial 8+ - Window Functions](https://sqlzoo.net/wiki/Window_functions)  
**Prérequis** : q04  
**Objectif** : Calculer des rangs à l'intérieur de groupes

**Compétences acquises** :
- Comprendre la différence entre GROUP BY et window functions
- Utiliser PARTITION BY pour créer des classements par groupe
- Filtrer sur le résultat d'une window function avec CTE

---

### q06 : Moyennes mobiles (Rolling averages)
**Concepts** : Window frames, `ROWS BETWEEN`, moyennes mobiles  
**SQLZoo** : [Tutorial 8+ - Window Functions](https://sqlzoo.net/wiki/Window_functions)  
**Prérequis** : q05  
**Objectif** : Calculer des moyennes glissantes sur plusieurs périodes

**Compétences acquises** :
- Maîtriser les window frames (ROWS vs RANGE)
- Créer des indicateurs mobiles (moving averages)
- Combiner agrégations et window functions

---

### q07 : RANK partitionné par groupe
**Concepts** : `RANK()` avec `PARTITION BY`, classement par catégorie  
**SQLZoo** : [Tutorial 8+ - Window Functions](https://sqlzoo.net/wiki/Window_functions)  
**Prérequis** : q06  
**Objectif** : Créer un TOP N par catégorie

**Compétences acquises** :
- Obtenir le classement de chaque élément dans sa catégorie
- Extraire le TOP N par groupe

---

### q08 : Jointures + agrégats + décades
**Concepts** : `FLOOR()`, calculs de dates, jointures, GROUP BY temporel  
**SQLZoo** : [Tutorial 5 - SUM and COUNT](https://sqlzoo.net/wiki/SUM_and_COUNT) + [Tutorial 6 - JOIN](https://sqlzoo.net/wiki/The_JOIN_operation)  
**Prérequis** : q07  
**Objectif** : Analyser l'évolution par décennie

**Compétences acquises** :
- Créer des groupes temporels (décennies)
- Combiner jointures et agrégations
- Analyser des tendances à long terme

---

### q09 : Jointures multiples (tags)
**Concepts** : Jointures en chaîne, tables de liaison  
**SQLZoo** : [Tutorial 6 - JOIN](https://sqlzoo.net/wiki/The_JOIN_operation)  
**Prérequis** : q08  
**Objectif** : Traverser plusieurs tables avec jointures

**Compétences acquises** :
- Joindre 3+ tables
- Naviguer dans un schéma many-to-many complexe

---

### q10 : CTE (Common Table Expressions)
**Concepts** : `WITH` clause, CTEs, structuration du code SQL  
**SQLZoo** : [Tutorial 9 - Window LAG](https://sqlzoo.net/wiki/Window_LAG)  
**Prérequis** : q09  
**Objectif** : Structurer une requête complexe avec des CTEs

**Compétences acquises** :
- Décomposer une requête en étapes nommées
- Améliorer la lisibilité du code SQL
- Préparer les requêtes vraiment complexes

---

## 🔴 Niveau Avancé (6-8h)

### q11 : Sous-requête vs JOIN (comparaison)
**Concepts** : Sous-requêtes corrélées, optimisation, comparaison de performances  
**SQLZoo** : Concepts avancés  
**Prérequis** : Niveau intermédiaire complet  
**Objectif** : Comprendre quand utiliser sous-requêtes ou jointures

**Compétences acquises** :
- Écrire des sous-requêtes corrélées
- Comparer les performances (sous-requête vs JOIN)
- Choisir la bonne approche selon le contexte

---

### q12 : UNION ALL (combiner datasets)
**Concepts** : `UNION`, `UNION ALL`, rapports comparatifs  
**SQLZoo** : Concepts avancés  
**Prérequis** : q11  
**Objectif** : Créer des rapports comparatifs en combinant des requêtes

**Compétences acquises** :
- Combiner des résultats homogènes
- Créer des rapports de comparaison
- Comprendre UNION vs UNION ALL

---

### q13 : Percentiles (distribution)
**Concepts** : `NTILE()`, percentiles, distribution statistique  
**SQLZoo** : [Tutorial 8+ - Window Functions](https://sqlzoo.net/wiki/Window_functions)  
**Prérequis** : q12  
**Objectif** : Analyser la distribution des données avec des percentiles

**Compétences acquises** :
- Calculer des percentiles (P90, médiane, etc.)
- Comprendre la distribution au-delà de la moyenne
- Utiliser NTILE pour découper en groupes

---

### q14 : Détection de doublons
**Concepts** : `GROUP BY` + `HAVING`, data quality, déduplication  
**SQLZoo** : [Tutorial 5 - SUM and COUNT](https://sqlzoo.net/wiki/SUM_and_COUNT)  
**Prérequis** : q13  
**Objectif** : Identifier et compter les doublons dans les données

**Compétences acquises** :
- Détecter des doublons par clé composite
- Analyser la qualité des données
- Préparer le nettoyage de données

---

### q15 : Contrôles qualité (data quality)
**Concepts** : `CASE WHEN`, calculs de pourcentages, UNION ALL, audits  
**SQLZoo** : Concepts avancés  
**Prérequis** : q14  
**Objectif** : Auditer la qualité d'un dataset

**Compétences acquises** :
- Calculer des métriques de complétude
- Analyser la distribution des valeurs
- Créer des rapports de qualité de données

---

### q16 : Sélectivité des index
**Concepts** : Index, `BETWEEN`, optimisation de requêtes  
**SQLZoo** : Optimisation (pas de tutorial spécifique)  
**Prérequis** : q15  
**Objectif** : Écrire des requêtes qui utilisent efficacement les index

**Compétences acquises** :
- Comprendre la sélectivité d'une requête
- Écrire des filtres "index-friendly"
- Tirer parti des index existants

---

### q17 : EXPLAIN (analyse de performance)
**Concepts** : `EXPLAIN`, plans d'exécution, optimisation  
**SQLZoo** : Optimisation (pas de tutorial spécifique)  
**Prérequis** : q16  
**Objectif** : Analyser comment MariaDB exécute une requête

**Compétences acquises** :
- Lire et interpréter un plan EXPLAIN
- Identifier les problèmes de performance
- Vérifier l'utilisation des index

---

### q18 : LEAD/LAG (fenêtres avancées)
**Concepts** : `LAG()`, `LEAD()`, comparaisons temporelles  
**SQLZoo** : [Tutorial 9 - Window LAG](https://sqlzoo.net/wiki/Window_LAG)  
**Prérequis** : q17  
**Objectif** : Comparer une valeur avec les valeurs précédentes/suivantes

**Compétences acquises** :
- Utiliser LAG pour accéder à la ligne précédente
- Utiliser LEAD pour accéder à la ligne suivante
- Analyser l'évolution dans le temps
- Calculer des différences entre périodes

---

### q19 : Gaps & Islands (séquences continues)
**Concepts** : `ROW_NUMBER()`, patterns avancés, séquences  
**SQLZoo** : Concepts avancés  
**Prérequis** : q18  
**Objectif** : Identifier des séquences continues dans les données

**Compétences acquises** :
- Résoudre le problème classique "Gaps and Islands"
- Détecter des séquences continues
- Identifier des trous dans les données
- Utiliser ROW_NUMBER() de manière créative

---

### q20 : Correction d'erreurs SQL courantes
**Concepts** : Debugging, jointures correctes, GROUP BY complet  
**SQLZoo** : Tous les concepts vus précédemment  
**Prérequis** : q19  
**Objectif** : Identifier et corriger des erreurs SQL typiques

**Compétences acquises** :
- Reconnaître les mauvaises jointures
- Corriger les GROUP BY incomplets
- Identifier les erreurs d'agrégation
- Appliquer les bonnes pratiques SQL

---

### BONUS : Création de vues (views)
**Concepts** : `CREATE VIEW`, réutilisation de requêtes  
**SQLZoo** : Concepts avancés  
**Prérequis** : Niveau avancé complet  
**Objectif** : Créer des vues pour simplifier les requêtes complexes

**Compétences acquises** :
- Créer et gérer des vues
- Comprendre quand utiliser une vue vs une table
- Optimiser la réutilisabilité du code SQL

---

## 🎯 Parcours Recommandés

### Parcours Express (Focus essentiel) - 6h
Pour ceux qui veulent l'essentiel rapidement :
1. **Débutant** : q00a, q00c, q00e, q00g, q00h (bases)
2. **Intermédiaire** : q01, q03, q04, q05, q08 (agrégats + window functions)
3. **Avancé** : q14, q16, q17 (qualité + performance)

### Parcours Complet (Maîtrise) - 12-17h
Pour une maîtrise complète :
1. **Semaine 1** : Niveau débutant (q00a→q00h) + q01→q04
2. **Semaine 2** : Window functions (q05→q07) + Jointures avancées (q08→q10)
3. **Semaine 3** : Optimisation et patterns (q11→q20 + BONUS)

### Parcours Data Analyst - 8h
Focus sur l'analyse de données :
1. **Bases** : q00a→q00h
2. **Agrégations** : q01→q04, q09
3. **Window functions** : q05→q07
4. **Data quality** : q14, q15

### Parcours Performance & Optimisation - 4h
Focus sur la performance :
1. **Prérequis** : Finir niveau intermédiaire
2. **Sous-requêtes** : q11
3. **Index** : q16, q17
4. **Patterns avancés** : q18, q19

---

## 📊 Matrice de Compétences

| Compétence | Exercices | Niveau requis |
|------------|-----------|---------------|
| SELECT de base | q00a-q00f | 🟢 Débutant |
| Agrégats simples | q00g-q00h | 🟢 Débutant |
| GROUP BY | q03-q04 | 🟡 Intermédiaire |
| Jointures | q03, q04, q08, q09 | 🟡 Intermédiaire |
| Window Functions | q05-q07, q13, q18, q19 | 🟡 Intermédiaire → 🔴 Avancé |
| CTEs | q05, q06, q08, q10, q19 | 🟡 Intermédiaire |
| Sous-requêtes | q11 | 🔴 Avancé |
| UNION | q12, q15 | 🔴 Avancé |
| Optimisation | q16, q17 | 🔴 Avancé |
| Data Quality | q14, q15, q20 | 🔴 Avancé |

---

## 💡 Conseils de Progression

### Stratégie d'apprentissage
1. **Ne sautez pas d'étapes** : Chaque exercice prépare au suivant
2. **Faites les exercices SQLZoo en parallèle** : Ils complètent parfaitement ce projet
3. **Testez dans Adminer** : Visualisez vos requêtes avant de les valider
4. **Lisez les erreurs** : Les messages d'erreur sont vos meilleurs professeurs
5. **Comprenez avant de copier** : Tapez le code au lieu de copier-coller

### Quand vous êtes bloqué
1. Relisez les consignes détaillées dans le fichier SQL
2. Consultez le tutoriel SQLZoo correspondant
3. Testez votre requête par parties dans Adminer
4. Vérifiez le schéma de la base dans `sql/schema/00_schema.sql`
5. Consultez `ressources.md` pour des guides spécifiques au concept

### Validation de votre progression
- ✅ **Un exercice = un test qui passe** : `pytest tests/test_XXX.py`
- ✅ **Tous les tests** : `docker exec -it vg-app pytest`
- ✅ **Vérifiez dans Adminer** : Regardez les résultats pour comprendre

---

## 🏁 Après avoir terminé

### Vous avez terminé le projet ? Bravo ! 🎉

Voici les prochaines étapes pour continuer à progresser :

1. **Refaites SQLZoo en entier** - Vous verrez votre progression !
2. **LeetCode SQL** - Pratiquez avec des problèmes de type interview
3. **Kaggle SQL Challenges** - Appliquez vos compétences sur de vrais datasets
4. **Contribuez au projet** - Proposez de nouveaux exercices
5. **Explorez d'autres SGBD** - PostgreSQL, SQLite, etc.

### Compétences acquises
À la fin de ce parcours, vous maîtriserez :
- ✅ Les bases du SQL (SELECT, WHERE, ORDER BY, LIMIT)
- ✅ Les agrégations (COUNT, AVG, MIN, MAX, GROUP BY, HAVING)
- ✅ Les jointures (INNER JOIN, LEFT JOIN, tables de liaison)
- ✅ Les window functions (RANK, LAG, LEAD, moyennes mobiles)
- ✅ Les CTEs pour structurer vos requêtes
- ✅ L'optimisation avec EXPLAIN et les index
- ✅ Les patterns avancés (Gaps & Islands, percentiles)
- ✅ La qualité de données et le débogage

**Vous êtes prêt pour des postes en Data Analytics, Business Intelligence, ou Data Engineering !** 🚀
