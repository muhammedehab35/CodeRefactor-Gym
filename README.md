# CodeRefactor Gym - OpenEnv Hackathon 2025

> Un environnement d'apprentissage par renforcement qui enseigne aux LLMs à refactoriser du code legacy en code moderne et maintenable.

[![Environment](https://img.shields.io/badge/HuggingFace-Deployed-blue)](https://huggingface.co/spaces/mo35/code-refactor-gym)
[![API](https://img.shields.io/badge/API-Live-green)](https://mo35-code-refactor-gym.hf.space)
[![License](https://img.shields.io/badge/License-BSD-yellow)](LICENSE)

---

## 🎯 Qu'est-ce que CodeRefactor Gym?

**CodeRefactor Gym** est un environnement OpenEnv innovant qui apprend aux agents d'IA à:
- ✅ Améliorer la qualité du code Python
- ✅ Ajouter des type hints et docstrings
- ✅ Éliminer les anti-patterns (globals, magic numbers)
- ✅ Réduire la complexité cyclomatique
- ✅ Transformer du code legacy en code maintenable

## 🏆 Résultats

### Environnement Déployé

- **HuggingFace Space**: https://huggingface.co/spaces/mo35/code-refactor-gym
- **API Endpoint**: https://mo35-code-refactor-gym.hf.space
- **Status**: ✅ En ligne et fonctionnel

### Tests Locaux

```
Test avec bon refactoring:
✓ Reward: +13.0
✓ Improvement Score: 80/100
✓ Type hints ajoutés
✓ Docstrings ajoutés
✓ Magic numbers éliminés
```

## 🚀 Quick Start

### Tester l'Environnement

```python
from openenv.client import Client
from code_refactor_gym.models import CodeRefactorGymAction

# Se connecter
client = Client(base_url="https://mo35-code-refactor-gym.hf.space")

# Obtenir du code legacy
obs = client.reset()
print(f"Code à refactoriser:\n{obs.legacy_code}")

# Soumettre refactoring
action = CodeRefactorGymAction(
    refactored_code="""
from typing import List

def filter_values(values: List[float], threshold: float) -> List[float]:
    '''Filter values greater than threshold.'''
    return [v for v in values if v > threshold]
""",
    reasoning="Added type hints, docstring, descriptive names"
)

result = client.step(action)
print(f"Reward: {result.reward}")
print(f"Improvement: {result.improvement_score}/100")
```

### Entraîner un Agent

```bash
# Installation
pip install -r requirements-training.txt

# Entraînement sur GPU H100 (Northflank)
# Voir: DEPLOY_NORTHFLANK_GUIDE.md
python train_agent.py \
  --model-id Qwen/Qwen2.5-1.5B-Instruct \
  --env-url https://mo35-code-refactor-gym.hf.space \
  --num-epochs 3
```

## 📁 Structure du Projet

```
CodeRefactor-Gym/
├── code_refactor_gym/              # Environnement OpenEnv
│   ├── models.py                   # Actions, Observations, State
│   ├── server/
│   │   ├── app.py                  # API FastAPI
│   │   └── code_refactor_gym_environment.py  # Logique RL
│   └── test_env.py                 # Tests locaux
│
├── train_agent.py                  # Script entraînement GRPO/TRL
├── Dockerfile.training             # Docker Northflank H100
├── requirements-training.txt       # Dépendances
│
└── Documentation/
    ├── README_HACKATHON.md         # Doc complète
    ├── DEPLOY_NORTHFLANK_GUIDE.md  # Guide déploiement
    ├── FINAL_CHECKLIST.md          # Checklist finale
    └── NEXT_STEPS.md               # Prochaines étapes
```

## 💡 Comment ça marche?

### 1. L'environnement fournit du code legacy

```python
def f(x, y):
    result = []
    for i in range(len(x)):
        if x[i] > y:
            result.append(x[i])
    return result
```

**Problèmes**: Mauvais nommage, pas de type hints, boucle inefficace

### 2. L'agent soumet du code refactorisé

```python
from typing import List

def filter_values_above_threshold(
    values: List[float],
    threshold: float
) -> List[float]:
    """
    Filter values that exceed the threshold.

    Args:
        values: List of numeric values
        threshold: Minimum value threshold

    Returns:
        List of values greater than threshold
    """
    return [value for value in values if value > threshold]
```

### 3. L'environnement évalue et récompense

```
Métriques calculées:
✓ Type hints: Added (+15 points)
✓ Docstring: Added (+10 points)
✓ Code conciseness: Improved (+5 points)
✓ Descriptive names: Improved
✓ List comprehension: Used

Total Reward: +13.0
Improvement Score: 80/100
```

## 🎮 Système de Récompenses

| Amélioration | Points |
|-------------|---------|
| Syntaxe invalide | -10 |
| Type hints ajoutés | +15 |
| Docstrings ajoutés | +10 |
| Globals éliminés | +15 |
| Magic numbers fixés | +10 |
| Complexité réduite | +10 |
| Bonus amélioration >70% | +5 |

**Maximum possible**: ~+18 points

## 🛠️ Technologies

- **OpenEnv** - Framework environnement RL
- **TRL** - Transformer Reinforcement Learning (GRPO)
- **Unsloth** - Optimisation 2x plus rapide
- **vLLM** - Inférence rapide
- **FastAPI** - API server
- **HuggingFace Spaces** - Hébergement
- **Northflank + CoreWeave** - GPU H100

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README_HACKATHON.md](README_HACKATHON.md) | Documentation complète du projet |
| [DEPLOY_NORTHFLANK_GUIDE.md](DEPLOY_NORTHFLANK_GUIDE.md) | Guide déploiement GPU H100 étape par étape |
| [FINAL_CHECKLIST.md](FINAL_CHECKLIST.md) | Checklist finale avant soumission |
| [NEXT_STEPS.md](NEXT_STEPS.md) | Prochaines étapes détaillées |
| [SUMMARY.txt](SUMMARY.txt) | Récapitulatif rapide |

## 🚀 Déploiement

### Northflank H100 GPU

Le projet est prêt pour déploiement sur Northflank avec GPU H100:

1. **Lire le guide**: [DEPLOY_NORTHFLANK_GUIDE.md](DEPLOY_NORTHFLANK_GUIDE.md)
2. **Connecter le repo GitHub** sur Northflank
3. **Configurer GPU H100** et variables d'environnement
4. **Lancer le build** et l'entraînement (~45-60 min)

Configuration fournie:
- ✅ `Dockerfile.training`
- ✅ `northflank.json`
- ✅ Guide étape par étape

## 📊 Résultats Attendus

Avec GPU H100 (3 epochs):

| Métrique | Epoch 1 | Epoch 2 | Epoch 3 |
|----------|---------|---------|---------|
| Reward moyen | 2-4 | 4-6 | 8-12 |
| Improvement | 30-40% | 50-60% | 70-80% |
| Syntax valid | >95% | >97% | >98% |
| Type hints | >70% | >80% | >90% |

## 🎯 Pourquoi c'est innovant?

1. **Premier environnement RL pour refactoring de code**
   - Aucun environnement similaire n'existe dans OpenEnv

2. **Problème réel et mesurable**
   - Le refactoring est un défi quotidien pour les développeurs
   - Métriques objectives (complexité, type hints, etc.)

3. **Apprentissage progressif**
   - De simples améliorations aux refactorings complexes
   - Feedback immédiat via rewards

4. **Applicable immédiatement**
   - Peut être utilisé sur vrai code legacy
   - Modèle entraîné déployable en production

## 📞 Contact & Liens

- **Participant**: mo35
- **HuggingFace**: [@mo35](https://huggingface.co/mo35)
- **Space**: [code-refactor-gym](https://huggingface.co/spaces/mo35/code-refactor-gym)
- **GitHub**: [CodeRefactor-Gym](https://github.com/muhammedehab35/CodeRefactor-Gym)

## 📄 License

Copyright (c) Meta Platforms, Inc. and affiliates.
BSD-style license (see OpenEnv project)

---

<div align="center">

**Fait avec ❤️ pour l'OpenEnv Hackathon 2025**

[📖 Documentation](README_HACKATHON.md) • [🚀 Déployer](DEPLOY_NORTHFLANK_GUIDE.md) • [✅ Checklist](FINAL_CHECKLIST.md)

</div>
