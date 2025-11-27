## ⚠️ Vérification de la Branche Cible

**IMPORTANT** : Ce repository utilise deux branches parallèles qui ne doivent JAMAIS être mergées entre elles :
- 🔵 `main` : Version MariaDB
- 🟣 `postgresql` : Version PostgreSQL

**Cochez pour confirmer** :
- [ ] Je confirme que cette PR ne tente **PAS** de merger `postgresql` dans `main`
- [ ] Je confirme que cette PR ne tente **PAS** de merger `main` dans `postgresql`
- [ ] J'ai lu [`.github/BRANCH_STRATEGY.md`](.github/BRANCH_STRATEGY.md)

---

## Type de Modification

Sélectionnez le type de modification :

- [ ] 🐛 **Bug fix** (correction d'un bug)
- [ ] ✨ **Feature** (nouvelle fonctionnalité ou exercice)
- [ ] 📝 **Documentation** (amélioration de la documentation)
- [ ] 🧪 **Tests** (ajout ou modification de tests)
- [ ] ♻️ **Refactoring** (réorganisation du code sans changement de fonctionnalité)
- [ ] 🎨 **Style** (formatage, indentation, etc.)

## Version Concernée

- [ ] 🔵 **MariaDB uniquement** (branche `main`)
- [ ] 🟣 **PostgreSQL uniquement** (branche `postgresql`)
- [ ] 🔄 **Commune aux deux versions** (documentation générale, structure projet, etc.)

## Description

<!-- Décrivez clairement vos modifications -->

### Qu'est-ce qui a changé ?


### Pourquoi ce changement ?


### Comment l'avez-vous testé ?


## Tests Effectués

- [ ] `docker compose up -d` démarre correctement
- [ ] `pytest -q` : Tous les tests passent
- [ ] Les exercices concernés fonctionnent correctement
- [ ] Testé avec Adminer (si applicable)

## Checklist Avant Merge

- [ ] Mon code suit les conventions du projet
- [ ] J'ai testé mes modifications localement avec Docker
- [ ] J'ai mis à jour la documentation si nécessaire
- [ ] Les liens vers la documentation officielle sont corrects
- [ ] Pas de secrets ou informations sensibles dans le commit
- [ ] Les messages de commit sont clairs et descriptifs

## Notes Additionnelles

<!-- Ajoutez toute information supplémentaire utile pour les reviewers -->

## Si Modification Commune

Si cette modification affecte les deux versions (MariaDB et PostgreSQL) :

- [ ] J'ai créé une issue pour tracker l'application sur l'autre branche
- [ ] J'ai documenté les adaptations nécessaires pour l'autre SGBD
- [ ] Numéro de l'issue : #___

---

📚 **Ressources** :
- [Stratégie de Branches](.github/BRANCH_STRATEGY.md)
- [Guide MariaDB vs PostgreSQL](docs/MARIADB_VS_POSTGRESQL.md)
- [Configuration GitHub](.github/GITHUB_SETTINGS.md)
