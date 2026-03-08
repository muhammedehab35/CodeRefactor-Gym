# CodeRefactor Gym - OpenEnv Hackathon

Un environnement OpenEnv innovant qui apprend aux agents RL à refactoriser du code legacy en code moderne et maintenable.

## 🎯 Concept

**CodeRefactor Gym** est un environnement d'apprentissage par renforcement où un agent LLM apprend à:
- Améliorer la qualité du code
- Ajouter des type hints et docstrings
- Éliminer les mauvaises pratiques (globals, magic numbers)
- Réduire la complexité cyclomatique
- Produire du code Python moderne et maintenable

## 🏆 Pourquoi c'est innovant

1. **Problème réel**: Le refactoring de code legacy est un défi quotidien pour les développeurs
2. **Récompenses mesurables**: Métriques objectives (complexité, type hints, qualité)
3. **Feedback immédiat**: Validation de syntaxe + scoring de qualité
4. **Apprentissage progressif**: De simples améliorations aux refactorings complexes

## 📊 Résultats des tests

```
Test local réussi:
✓ Code legacy fourni avec métriques de base
✓ Agent soumet du code refactorisé
✓ Amélioration: 80/100 points
✓ Récompense: +13.0
✓ Type hints ajoutés ✓
✓ Docstrings ajoutés ✓
✓ Magic numbers éliminés ✓
```

## 🏗️ Architecture

### Environnement (HuggingFace Spaces)
- **URL**: https://huggingface.co/spaces/mo35/code-refactor-gym
- **API**: https://mo35-code-refactor-gym.hf.space
- **Tech**: OpenEnv + FastAPI + Docker

### Agent d'entraînement (Northflank H100)
- **Framework**: TRL (GRPO - Group Relative Policy Optimization)
- **Modèle**: Qwen/Qwen2.5-1.5B-Instruct
- **Optimisation**: Unsloth (2x plus rapide, 70% moins de mémoire)
- **GPU**: NVIDIA H100 80GB via CoreWeave

## 📁 Structure du projet

```
.
├── code_refactor_gym/          # Environnement OpenEnv
│   ├── models.py               # Actions, Observations, State
│   ├── server/
│   │   ├── app.py              # FastAPI entry point
│   │   └── code_refactor_gym_environment.py  # Logique RL
│   └── test_env.py             # Tests locaux
│
├── train_agent.py              # Script d'entraînement GRPO
├── requirements-training.txt   # Dépendances training
├── Dockerfile.training         # Docker pour Northflank
└── NORTHFLANK_DEPLOYMENT.md    # Guide de déploiement
```

## 🚀 Déploiement

### 1. Environnement déployé ✅

```bash
Space URL: https://huggingface.co/spaces/mo35/code-refactor-gym
API URL: https://mo35-code-refactor-gym.hf.space
Status: ✅ DEPLOYED
```

### 2. Entraînement sur Northflank

Voir le guide complet: [NORTHFLANK_DEPLOYMENT.md](NORTHFLANK_DEPLOYMENT.md)

**Commande rapide:**
```bash
python train_agent.py \
  --model-id Qwen/Qwen2.5-1.5B-Instruct \
  --env-url https://mo35-code-refactor-gym.hf.space \
  --num-epochs 3 \
  --batch-size 4 \
  --use-vllm \
  --output-dir ./code-refactor-agent
```

## 🎮 Utilisation

### Test l'environnement manuellement

```python
from openenv.client import Client
from code_refactor_gym.models import CodeRefactorGymAction

# Connecter à l'environnement
client = Client(base_url="https://mo35-code-refactor-gym.hf.space")

# Reset pour obtenir du code legacy
obs = client.reset()
print(f"Code legacy:\n{obs.legacy_code}")
print(f"Métriques de base: {obs.quality_metrics}")

# Soumettre du code refactorisé
refactored = """
from typing import List

def filter_above_threshold(values: List[float], threshold: float) -> List[float]:
    '''Filter values greater than threshold.'''
    return [v for v in values if v > threshold]
"""

action = CodeRefactorGymAction(
    refactored_code=refactored,
    reasoning="Added type hints, docstring, descriptive names"
)

result = client.step(action)
print(f"Reward: {result.reward}")
print(f"Improvement: {result.improvement_score}/100")
```

### Entraîner un agent

```bash
# Installation
pip install -r requirements-training.txt

# Entraînement local (si GPU disponible)
python train_agent.py

# Ou sur Northflank H100
# Voir NORTHFLANK_DEPLOYMENT.md
```

## 📈 Système de récompenses

### Récompenses de base
- **Syntaxe invalide**: -10 points
- **Amélioration 0-40**: +0 à +4 points
- **Amélioration 40-70**: +4 à +7 points
- **Amélioration 70-100**: +7 à +10 points

### Bonus
- **Amélioration > 70%**: +5 points
- **Type hints ajoutés**: +15 points (dans le score)
- **Docstrings ajoutés**: +10 points
- **Globals éliminés**: +15 points
- **Magic numbers fixés**: +10 points

### Pénalités
- **Complexité augmentée**: -10 points
- **Code plus long**: -5 points

## 🔬 Exemples de code legacy

L'environnement contient 5 types de code legacy:

1. **Mauvais nommage + logique complexe**
```python
def f(x, y):
    result = []
    for i in range(len(x)):
        if x[i] > y:
            result.append(x[i])
    return result
```

2. **Variables globales**
```python
total = 0
def add(x):
    global total
    total = total + x
    return total
```

3. **Conditions imbriquées**
```python
def check(data):
    if data != None:
        if len(data) > 0:
            if type(data) == list:
                return True
    return False
```

4. **Magic numbers + pas de gestion d'erreurs**
```python
def process(items):
    result = []
    for i in items:
        if i % 2 == 0:
            result.append(i * 3.14159)
    return result
```

5. **Code répétitif**
```python
def calc1(x): return x * 2 + 10
def calc2(x): return x * 3 + 10
def calc3(x): return x * 4 + 10
```

## 🧪 Métriques de qualité

L'environnement calcule automatiquement:

- **Lines**: Nombre de lignes (moins = mieux)
- **Complexity**: Complexité cyclomatique (moins = mieux)
- **Type hints**: Présence d'annotations de type
- **Docstrings**: Documentation du code
- **Globals**: Utilisation de variables globales (à éviter)
- **Magic numbers**: Nombres hardcodés (à éviter)

## 🎓 Apprentissage progressif

L'agent apprend à:

**Phase 1 - Fondamentaux (Epochs 1-2)**
- Maintenir la syntaxe valide
- Comprendre la structure du code
- Identifier les améliorations simples

**Phase 2 - Qualité (Epochs 3-5)**
- Ajouter type hints systématiquement
- Écrire des docstrings claires
- Utiliser des noms descriptifs

**Phase 3 - Expertise (Epochs 6+)**
- Éliminer les patterns anti-patterns
- Réduire la complexité
- Appliquer les best practices Python

## 🏅 Soumission Hackathon

### Checklist

- ✅ Environnement OpenEnv créé
- ✅ Déployé sur HuggingFace Spaces
- ✅ Tests réussis localement
- ✅ Script d'entraînement GRPO/TRL
- ✅ Configuration Northflank H100
- ⏳ Entraînement en cours
- ⏳ Évaluation finale
- ⏳ Documentation complète

### Critères d'évaluation

1. **Originalité**: ✅ Premier environnement de refactoring de code
2. **Utilité**: ✅ Problème réel pour tous les développeurs
3. **Implémentation**: ✅ Métriques objectives + feedback clair
4. **Performance**: ✅ Optimisé avec Unsloth + vLLM
5. **Documentation**: ✅ README + guides de déploiement

## 🛠️ Technologies utilisées

- **OpenEnv**: Framework environnement RL
- **TRL**: Transformer Reinforcement Learning (GRPO)
- **Unsloth**: Optimisation 2x plus rapide
- **vLLM**: Inférence rapide
- **FastAPI**: Serveur API
- **Docker**: Containerisation
- **HuggingFace Spaces**: Hébergement environnement
- **Northflank + CoreWeave**: GPU H100
- **Qwen 2.5**: Modèle de base

## 📞 Contact

- **Participant**: mo35
- **HuggingFace**: https://huggingface.co/mo35
- **Space**: https://huggingface.co/spaces/mo35/code-refactor-gym

## 📄 License

Copyright (c) Meta Platforms, Inc. and affiliates.
BSD-style license (see OpenEnv project)

---

**Fait avec ❤️ pour l'OpenEnv Hackathon 2025**
