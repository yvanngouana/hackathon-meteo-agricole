# Guide de Contribution

## Workflow Git

### 1. Créer une branche feature

```bash
git checkout -b feature/nom-de-la-feature
```

Convention de nommage :
- `feature/` : Nouvelle fonctionnalité
- `fix/` : Correction de bug
- `docs/` : Documentation
- `refactor/` : Refactorisation code

### 2. Développer

- Écrire du code propre et commenté
- Suivre les conventions PEP 8 (Python)
- Ajouter des tests si applicable

### 3. Formater le code

```bash
# Auto-formatage
black src/
isort src/

# Vérification
flake8 src/ --max-line-length=120
```

### 4. Tester

```bash
pytest tests/ -v
```

### 5. Commit

Convention Conventional Commits :

```bash
git commit -m "feat: Ajout endpoint prédictions irrigation"
git commit -m "fix: Correction calcul ET0"
git commit -m "docs: Mise à jour README"
```

Types de commits :
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction bug
- `docs`: Documentation
- `test`: Tests
- `refactor`: Refactorisation
- `chore`: Tâches maintenance

### 6. Push

```bash
git push origin feature/nom-de-la-feature
```

### 7. Pull Request

- Créer PR sur GitHub
- Décrire les changements
- Référencer issues si applicable
- Attendre review d'un membre

## Standards de Code

### Python

```python
# Bonnes pratiques
- Type hints
- Docstrings (Google style)
- Noms explicites
- Fonctions courtes (< 50 lignes)

# Exemple
def calculate_irrigation_need(
    evapotranspiration_mm: float,
    rainfall_mm: float
) -> float:
    """
    Calcule le besoin en irrigation.

    Args:
        evapotranspiration_mm: Évapotranspiration en mm
        rainfall_mm: Pluie en mm

    Returns:
        Besoin en irrigation en mm (>= 0)
    """
    return max(0, evapotranspiration_mm - rainfall_mm)
```

### Tests

```python
# Nommer tests clairement
def test_calculate_irrigation_need_with_sufficient_rain():
    result = calculate_irrigation_need(et0=10, rain=15)
    assert result == 0

def test_calculate_irrigation_need_with_insufficient_rain():
    result = calculate_irrigation_need(et0=10, rain=5)
    assert result == 5
```

## Structure PR

```markdown
## Description
Brève description des changements

## Type de changement
- [ ] Feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Refactoring

## Checklist
- [ ] Code formaté (black, isort)
- [ ] Tests ajoutés/passent
- [ ] Documentation mise à jour
- [ ] Testé localement

## Screenshots (si applicable)
```

## Communication

- Slack/Discord : Discussion quotidienne
- GitHub Issues : Bugs et features
- GitHub Discussions : Questions techniques
- Daily Standup : 15 min/jour

## Questions ?

Contacter l'équipe sur [canal communication]
