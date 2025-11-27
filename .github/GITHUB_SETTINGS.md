# Configuration GitHub Recommandée

Ce document décrit les paramètres GitHub recommandés pour ce repository afin de maintenir la séparation entre les branches `main` (MariaDB) et `postgresql` (PostgreSQL).

## 🛡️ Protection Automatique (Déjà en Place)

✅ **Workflow GitHub Actions** : `.github/workflows/prevent-cross-branch-prs.yml`
- Ferme automatiquement les PRs de `postgresql` → `main`
- Ferme automatiquement les PRs de `main` → `postgresql`
- Ajoute un commentaire explicatif

## ⚙️ Configuration Manuelle (Settings GitHub)

### 1. Default Branch

**Chemin** : Settings → General → Default branch

**Configuration Recommandée** :
- **Default branch** : `main`
- **Raison** : La version MariaDB est la plus commune pour les développeurs web

### 2. Branch Protection Rules (Optionnel)

**Chemin** : Settings → Branches → Branch protection rules

#### Protection pour `main`

Cliquez sur "Add rule" et configurez :
- **Branch name pattern** : `main`
- ✅ **Require a pull request before merging**
- ✅ **Require approvals** : 1 (si vous travaillez en équipe)
- ✅ **Dismiss stale pull request approvals when new commits are pushed**
- ⚠️ **Do not allow bypassing the above settings**

#### Protection pour `postgresql`

Cliquez sur "Add rule" et configurez :
- **Branch name pattern** : `postgresql`
- ✅ **Require a pull request before merging**
- ✅ **Require approvals** : 1 (si vous travaillez en équipe)
- ✅ **Dismiss stale pull request approvals when new commits are pushed**
- ⚠️ **Do not allow bypassing the above settings**

### 3. Pull Request Settings

**Chemin** : Settings → General → Pull Requests

**Configuration Recommandée** :
- ✅ **Allow squash merging**
  - Default message : "Default to pull request title and description"
- ✅ **Allow merge commits**
- ❌ **Allow rebase merging** (désactivé pour éviter confusion)
- ✅ **Automatically delete head branches**

### 4. Repository Topics

**Chemin** : About → Settings (roue dentée) → Topics

**Topics Recommandés** :
- `sql`
- `postgresql`
- `mariadb`
- `mysql`
- `learning`
- `tdd`
- `data-science`
- `tutorial`
- `python`

### 5. About Section

**Chemin** : About → Settings (roue dentée)

**Description Recommandée** :
```
📚 Cours SQL avec TDD et données réelles (RAWG dataset).
Disponible en 2 versions : MariaDB (main) et PostgreSQL (postgresql).
38 exercices du débutant à l'expert.
```

**Website** : (votre URL de documentation si applicable)

✅ **Include in the home page** :
- [x] Releases
- [x] Packages
- [x] Deployments

## 🏷️ Labels Recommandés

**Chemin** : Issues → Labels → New label

Créez les labels suivants pour faciliter la gestion :

| Label | Couleur | Description |
|-------|---------|-------------|
| `mariadb` | `#0052CC` | Spécifique à la version MariaDB (branche main) |
| `postgresql` | `#336791` | Spécifique à la version PostgreSQL (branche postgresql) |
| `common` | `#7057FF` | Affecte les deux versions |
| `documentation` | `#0075CA` | Améliorations de la documentation |
| `exercise` | `#008672` | Lié aux exercices SQL |
| `test` | `#FBCA04` | Tests et validation |
| `bug-mariadb` | `#D73A4A` | Bug dans la version MariaDB |
| `bug-postgresql` | `#D73A4A` | Bug dans la version PostgreSQL |

## 📋 Pull Request Template (Optionnel)

Si vous souhaitez ajouter un template de PR, créez le fichier `.github/pull_request_template.md` :

```markdown
## Type de modification

- [ ] 🐛 Bug fix (MariaDB)
- [ ] 🐛 Bug fix (PostgreSQL)
- [ ] ✨ Nouvelle fonctionnalité (MariaDB)
- [ ] ✨ Nouvelle fonctionnalité (PostgreSQL)
- [ ] 📝 Documentation
- [ ] 🧪 Tests
- [ ] 🔄 Modification commune (affecte les deux versions)

## Branche cible

**⚠️ ATTENTION** : Les branches `main` et `postgresql` ne doivent PAS être mergées entre elles.

- [ ] Je confirme que cette PR ne tente pas de merger `postgresql` dans `main`
- [ ] Je confirme que cette PR ne tente pas de merger `main` dans `postgresql`
- [ ] J'ai lu `.github/BRANCH_STRATEGY.md`

## Description

<!-- Décrivez vos modifications -->

## Tests effectués

- [ ] Tests unitaires passent (`pytest -q`)
- [ ] Exercices concernés fonctionnent correctement
- [ ] Documentation mise à jour si nécessaire

## Checklist

- [ ] Mon code suit les conventions du projet
- [ ] J'ai testé mes modifications localement
- [ ] J'ai mis à jour la documentation si nécessaire
- [ ] Si modification commune, j'ai créé une issue pour l'appliquer sur l'autre branche
```

## 🤝 Collaboration

### Pour les Contributeurs Externes

Si vous acceptez des contributions externes, configurez :

**Chemin** : Settings → Collaborators and teams

- Ajoutez les règles de contribution dans `CONTRIBUTING.md`
- Configurez les permissions appropriées

### Code Owners (Optionnel)

Créez `.github/CODEOWNERS` pour définir les responsables :

```
# Global owners
* @JeanPoma

# Documentation
*.md @JeanPoma
docs/ @JeanPoma

# MariaDB specific
/sql/ @JeanPoma
/scripts/ @JeanPoma

# Tests
/tests/ @JeanPoma
```

## 🔔 Notifications

**Chemin** : Settings → Notifications

Configurez vos préférences de notification pour :
- Pull requests
- Issues
- Actions (workflow failures)

## ✅ Vérification de la Configuration

Une fois configuré, vérifiez :
- [ ] Le workflow Actions fonctionne (créez une PR test postgresql→main pour vérifier)
- [ ] Les branch protection rules sont actives
- [ ] Les labels sont créés
- [ ] La description du repository est claire

## 📞 Support

Pour toute question sur la configuration, consultez :
- [GitHub Docs - Managing Branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository)
- [GitHub Docs - Actions](https://docs.github.com/en/actions)
