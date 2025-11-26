# 🎮 Cours SQL + TDD (MariaDB + Python) — Dataset RAWG (Kaggle)

Ce projet propose une progression TDD pour apprendre SQL avec des **données réelles** (dataset RAWG par jummyegg).

## 📑 Table des matières

- [🎯 Objectifs](#-objectifs)
- [🎓 Parcours d'apprentissage](#-parcours-dapprentissage)
- [📚 Avant de commencer](#-avant-de-commencer)
- [⚙️ Installation](#️-installation)
- [🚀 Utilisation](#-utilisation)
- [🎮 Explorer la base avec Adminer](#-explorer-la-base-avec-adminer)
- [📊 Suivre votre progression](#-suivre-votre-progression)
- [💡 Conseils pédagogiques](#-conseils-pédagogiques)
- [🔧 Dépannage](#-dépannage)
- [📄 Licence & Données](#-licence--données)

---

## 🎯 Objectifs

Ce projet vise à s'entraîner sur les requêtes SQL à partir de données réelles issues du monde du jeu vidéo.

**Pourquoi ce projet ?**
- Apprendre SQL avec une approche **Test-Driven Development (TDD)**
- Travailler sur un dataset **réel et normalisé** (6 tables avec relations)
- Progresser du niveau débutant aux concepts avancés (fenêtres, CTEs, optimisation)
- Valider automatiquement vos requêtes avec pytest

**Avant de vous lancer**, nous recommandons de réaliser au minimum les exercices **0, 1, 2 & 3** du site [SQL Zoo](https://sqlzoo.net/wiki/SQL_Tutorial) pour vous familiariser avec la syntaxe SQL de base.

---

## 🎓 Parcours d'apprentissage

Le projet propose **3 niveaux de difficulté** pour une progression adaptée :

### 🟢 **Niveau Débutant** (environ 2-3h)
**Objectif** : Maîtriser les bases du SQL (SELECT, WHERE, ORDER BY, agrégats simples)

| Exercice | Concepts clés | Prérequis SQLZoo |
|----------|---------------|------------------|
| **q00a** | SELECT simple (toutes colonnes) | [Tutorial 0](https://sqlzoo.net/wiki/SELECT_basics) |
| **q00b** | SELECT avec colonnes spécifiques | [Tutorial 0](https://sqlzoo.net/wiki/SELECT_basics) |
| **q00c** | WHERE simple (condition unique) | [Tutorial 1](https://sqlzoo.net/wiki/SELECT_names) |
| **q00d** | WHERE avec AND/OR | [Tutorial 1](https://sqlzoo.net/wiki/SELECT_names) |
| **q00e** | ORDER BY (ASC/DESC) | [Tutorial 1](https://sqlzoo.net/wiki/SELECT_names) |
| **q00f** | LIMIT (pagination) | [Tutorial 1](https://sqlzoo.net/wiki/SELECT_names) |
| **q00g** | COUNT (agrégat basique) | [Tutorial 2](https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial) |
| **q00h** | AVG, MIN, MAX (agrégats) | [Tutorial 2](https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial) |

### 🟡 **Niveau Intermédiaire** (environ 4-6h)
**Objectif** : Agrégations, jointures, GROUP BY et introduction aux fenêtres

| Exercice | Concepts clés | Prérequis SQLZoo |
|----------|---------------|------------------|
| **q01** | TOP N avec ORDER BY et LIMIT | [Tutorial 2](https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial) |
| **q02** | Filtres multiples + tri | [Tutorial 2](https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial) |
| **q03** | GROUP BY multi-colonnes | [Tutorial 5](https://sqlzoo.net/wiki/SUM_and_COUNT) |
| **q04** | GROUP BY avec agrégats | [Tutorial 5](https://sqlzoo.net/wiki/SUM_and_COUNT) |
| **q05** | Window Functions (RANK/DENSE_RANK) | [Tutorial 8+](https://sqlzoo.net/wiki/Window_functions) |
| **q06** | Fenêtres avec moyennes mobiles | [Tutorial 8+](https://sqlzoo.net/wiki/Window_functions) |
| **q07** | RANK partitionné par groupe | [Tutorial 8+](https://sqlzoo.net/wiki/Window_functions) |
| **q08** | Jointures + agrégats + décades | [Tutorial 6](https://sqlzoo.net/wiki/The_JOIN_operation) |
| **q09** | Jointures multiples (tags) | [Tutorial 6](https://sqlzoo.net/wiki/The_JOIN_operation) |
| **q10** | CTE (Common Table Expressions) | [Tutorial 9](https://sqlzoo.net/wiki/Window_LAG) |

### 🔴 **Niveau Avancé** (environ 6-8h)
**Objectif** : Optimisation, sous-requêtes complexes, analyse de performance

| Exercice | Concepts clés |
|----------|---------------|
| **q11** | Subquery vs JOIN (comparaison) |
| **q12** | UNION ALL (combiner datasets) |
| **q13** | Percentiles avec fonctions de fenêtre |
| **q14** | Détection de doublons |
| **q15** | Contrôles qualité (data quality) |
| **q16** | Sélectivité des index |
| **q17** | EXPLAIN pour analyse de requêtes |
| **q18** | LEAD/LAG (fenêtres avancées) |
| **q19** | Gaps & Islands (séquences) |
| **q20** | Erreurs SQL courantes à corriger |
| **BONUS** | Création de vues (views) |

---

## 📚 Avant de commencer

### 🗂️ Schéma de la base de données

Le dataset RAWG est organisé en **6 tables principales** avec des relations many-to-many :

```
games (table centrale)
├── id, rawg_id, name, released, year
├── metacritic, rating, ratings_count
├── playtime, esrb
└── Index : idx_games_year, idx_games_name

platforms                 genres                    publishers
├── id, code             ├── id, name              ├── id, name
└── (PC, PS5, Xbox...)   └── (Action, RPG...)      └── (Activision...)

developers                tags
├── id, name             ├── id, name
└── (Valve...)           └── (Multiplayer...)

Tables de liaison (many-to-many) :
├── game_platforms (game_id, platform_id)
├── game_genres (game_id, genre_id)
├── game_publishers (game_id, publisher_id)
├── game_developers (game_id, developer_id)
└── game_tags (game_id, tag_id)
```

**Exemples de données** :
- ~850 000 jeux avec leurs métadonnées
- Scores Metacritic (0-100)
- Plateformes multiples par jeu (PC, consoles, mobile)
- Genres, éditeurs, développeurs, tags variés

### 🔍 Commandes utiles pour explorer

Une fois la base installée, vous pouvez explorer avec :
```sql
-- Compter le nombre de jeux
SELECT COUNT(*) FROM games;

-- Voir les 10 premiers jeux
SELECT * FROM games LIMIT 10;

-- Voir les genres disponibles
SELECT * FROM genres;

-- Jeux avec leurs genres (jointure)
SELECT g.name, gr.name as genre
FROM games g
JOIN game_genres gg ON g.id = gg.game_id
JOIN genres gr ON gg.genre_id = gr.id
LIMIT 10;
```

---

## ⚙️ Installation

### Prérequis
- Docker / Docker Compose installé sur votre poste
- Données :
  - Téléchargez le [RAWG Game Dataset](https://www.kaggle.com/datasets/jummyegg/rawg-game-dataset)
  - Placez `rawg_games.csv` dans le dossier `data/` (dézippé)

### Étapes d'installation

1. **Démarrer la base de données et Adminer**
   ```bash
   docker compose up -d mariadb
   docker compose up -d adminer
   ```

2. **Installer les dépendances Python**
   ```bash
   docker compose run -d --name vg-app app bash -lc "pip install -r requirements.txt && tail -f /dev/null"
   ```

3. **Charger le dataset dans MariaDB**
   ```bash
   docker exec -it vg-app python scripts/load_rawg_csv.py
   ```
   ⏱️ Cette étape peut prendre 5-10 minutes selon votre machine.

4. **Vérifier l'installation avec les tests**
   ```bash
   docker exec -it vg-app pytest -q
   ```

---

## 🚀 Utilisation

### Workflow de travail

1. **📝 Éditer votre requête SQL**
   - Ouvrez un fichier dans `sql/queries/` (ex: `q00a_select_all_games.sql`)
   - Lisez les consignes en commentaire
   - Remplacez les consignes par votre requête SQL

2. **✅ Tester votre requête**
   ```bash
   docker exec -it vg-app pytest tests/test_00a_select_all_games.py -v
   ```
   - ✅ **Test passé** → Bravo ! Passez au suivant
   - ❌ **Test échoué** → Lisez le message d'erreur et ajustez

3. **🔄 Itérer jusqu'à validation**
   - Modifiez votre requête
   - Relancez le test
   - Répétez jusqu'à ce que le test passe

4. **📊 Vérifier votre progression globale**
   ```bash
   docker exec -it vg-app pytest -q
   ```

### Où écrire le SQL ?

- Les **requêtes à implémenter** sont dans `sql/queries/*.sql`
- Chaque fichier contient des **consignes en commentaire**
- **Remplacez les consignes** par votre requête SQL (une seule par fichier)
- Les tests correspondants sont dans `tests/test_*.py`

**⚠️ Important** :
- Un fichier = une seule requête SQL
- Pas besoin de point-virgule final (`;`)
- Testez régulièrement avec pytest

---

## 🎮 Explorer la base avec Adminer

**Adminer** est une interface web pour explorer et tester vos requêtes SQL directement.

### Accès
1. Ouvrez votre navigateur : **http://localhost:8080**
2. Connectez-vous avec :
   - **Système** : MySQL
   - **Serveur** : mariadb
   - **Utilisateur** : root
   - **Mot de passe** : rootpwd
   - **Base de données** : vg

### Utilisation
- **Onglet "SQL"** : Testez vos requêtes en temps réel
- **Tables** : Explorez la structure et les données
- **Sélectionner** : Visualisez les données de chaque table
- **Schéma** : Voyez les relations entre tables

💡 **Astuce** : Testez d'abord vos requêtes dans Adminer avant de les mettre dans les fichiers `.sql` !


## 📊 Suivre votre progression

### Vérifier rapidement vos tests

Pour voir l'état de tous vos exercices d'un coup d'œil :

```bash
# Tous les tests avec résumé
docker exec -it vg-app pytest --tb=no -q

# Tests avec barre de progression
docker exec -it vg-app pytest --tb=line

# Uniquement les exercices débutants
docker exec -it vg-app pytest tests/test_00*.py -v

# Uniquement les exercices intermédiaires
docker exec -it vg-app pytest tests/test_0[1-9]*.py tests/test_10*.py -v

# Uniquement les exercices avancés
docker exec -it vg-app pytest tests/test_1[1-9]*.py tests/test_20*.py -v
```

### Script de visualisation de progression

Un script Python est disponible pour visualiser votre progression de manière plus agréable :

```bash
# Afficher votre progression avec des barres colorées
docker exec -it vg-app python scripts/show_progress.py
```

Ce script affiche :
- ✅ Nombre d'exercices complétés par niveau
- 📊 Barre de progression visuelle
- 🎯 Prochains exercices recommandés
- 🏆 Badges de compétences débloqués

### Badges de compétences

Au fur et à mesure de votre progression, vous débloquerez des badges :

| Badge | Condition | Compétences |
|-------|-----------|-------------|
| 🌱 **Bases SQL** | 8/8 exercices débutants | SELECT, WHERE, ORDER BY, LIMIT |
| 🔢 **Agrégation** | q00g, q00h, q03, q04 | COUNT, AVG, GROUP BY, HAVING |
| 🔗 **Jointures** | q03, q04, q08, q09 | INNER JOIN, LEFT JOIN, many-to-many |
| 🪟 **Window Functions** | q05, q06, q07 | RANK, PARTITION BY, OVER |
| 📝 **CTEs** | q05, q10 | WITH clause, sous-requêtes nommées |
| ⚡ **Optimisation** | q16, q17 | EXPLAIN, index, performance |
| 🎓 **Maître SQL** | Tous les exercices | Toutes les compétences ! |

### Consulter le parcours détaillé

Pour une vue d'ensemble de tous les exercices et leur cartographie avec SQLZoo :

```bash
cat PARCOURS.md
```

Ce fichier contient :
- 🗺️ Cartographie complète des exercices
- 🔗 Liens directs vers les tutoriels SQLZoo
- 📋 Parcours recommandés selon vos objectifs
- 💡 Conseils de progression

---


---

## 💡 Conseils pédagogiques

### Pour bien progresser
- ✅ **Travaillez en binôme** : l'un lit les tests, l'autre propose une requête
- ✅ **Commencez par le début** : respectez l'ordre des exercices (q00a → q00h → q01 → q20)
- ✅ **Utilisez Adminer** : testez et visualisez vos requêtes avant de valider
- ✅ **Consultez les ressources** : le fichier `ressources.md` contient des liens utiles
- ✅ **Faites les exercices SQLZoo** : ils complètent parfaitement ce projet

### Approche TDD (Test-Driven Development)
1. Lisez le test pour comprendre ce qui est attendu
2. Écrivez la requête la plus simple qui fonctionne
3. Lancez le test
4. Si ❌ : analysez l'erreur et ajustez
5. Si ✅ : passez au suivant !

### Pour les niveaux avancés
- **Fenêtres** : Maîtrisez LEAD/LAG, RANK, DENSE_RANK
- **Optimisation** : Utilisez EXPLAIN pour analyser vos requêtes
- **CTEs** : Décomposez les requêtes complexes en sous-requêtes nommées
- **Index** : Comprenez comment MariaDB utilise les index

---

## 🔧 Dépannage

### La table `games` est vide
- Vérifiez que `data/rawg_games.csv` existe
- Relancez le script : `docker exec -it vg-app python scripts/load_rawg_csv.py`

### Les tests de fenêtres échouent
- Assurez-vous d'utiliser **MariaDB ≥ 10.5**
- Vérifiez avec : `docker exec -it mariadb mysql --version`

### EXPLAIN n'utilise pas l'index
- Rendez la clause WHERE plus sélective
- Vérifiez que l'index existe : `SHOW INDEX FROM games;`

### Erreur de connexion Docker
- Vérifiez que les conteneurs tournent : `docker compose ps`
- Redémarrez : `docker compose restart`

### Réinitialiser complètement le projet
```bash
docker compose down -v
docker compose up -d mariadb adminer
# Puis refaire les étapes d'installation
```

---

## 📄 Licence & Données

- **Dataset** : RAWG (agrégé par jummyegg sur Kaggle)
- Respectez les conditions d'usage de la source
- Ce projet est à but pédagogique uniquement

---

**🚀 Bon apprentissage du SQL !**

Pour toute question, consultez le fichier `ressources.md` ou les tutoriels [SQL Zoo](https://sqlzoo.net/wiki/SQL_Tutorial).
