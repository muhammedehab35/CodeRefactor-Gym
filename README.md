# CodeRefactor Gym - OpenEnv Hackathon 2025

> A reinforcement learning environment that teaches LLMs to refactor legacy code into modern and maintainable code.

[![Environment](https://img.shields.io/badge/HuggingFace-Deployed-blue)](https://huggingface.co/spaces/mo35/code-refactor-gym)
[![API](https://img.shields.io/badge/API-Live-green)](https://mo35-code-refactor-gym.hf.space)
[![License](https://img.shields.io/badge/License-BSD-yellow)](LICENSE)

---

## 🎯 What is CodeRefactor Gym?

**CodeRefactor Gym** is an innovative OpenEnv environment that teaches AI agents to:
- ✅ Improve Python code quality
- ✅ Add type hints and docstrings
- ✅ Eliminate anti-patterns (globals, magic numbers)
- ✅ Reduce cyclomatic complexity
- ✅ Transform legacy code into maintainable code

## 🏆 Results

### Deployed Environment

- **HuggingFace Space**: https://huggingface.co/spaces/mo35/code-refactor-gym
- **API Endpoint**: https://mo35-code-refactor-gym.hf.space
- **Status**: ✅ Online and functional

### Local Tests

```
Test with good refactoring:
✓ Reward: +13.0
✓ Improvement Score: 80/100
✓ Type hints added
✓ Docstrings added
✓ Magic numbers eliminated
```

## 🚀 Quick Start

### Test the Environment

```python
from openenv.client import Client
from code_refactor_gym.models import CodeRefactorGymAction

# Connect
client = Client(base_url="https://mo35-code-refactor-gym.hf.space")

# Get legacy code
obs = client.reset()
print(f"Code to refactor:\n{obs.legacy_code}")

# Submit refactoring
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

### Train an Agent

```bash
# Installation
pip install -r requirements-training.txt

# Training on H100 GPU (Northflank)
# See: DEPLOY_NORTHFLANK_GUIDE.md
python train_agent.py \
  --model-id Qwen/Qwen2.5-1.5B-Instruct \
  --env-url https://mo35-code-refactor-gym.hf.space \
  --num-epochs 3
```

## 📁 Project Structure

```
CodeRefactor-Gym/
├── code_refactor_gym/              # OpenEnv Environment
│   ├── models.py                   # Actions, Observations, State
│   ├── server/
│   │   ├── app.py                  # FastAPI API
│   │   └── code_refactor_gym_environment.py  # RL Logic
│   └── test_env.py                 # Local tests
│
├── train_agent.py                  # GRPO/TRL training script
├── Dockerfile.training             # Northflank H100 Docker
├── requirements-training.txt       # Dependencies
│
└── Documentation/
    ├── README_HACKATHON.md         # Complete documentation
    ├── DEPLOY_NORTHFLANK_GUIDE.md  # Deployment guide
    ├── FINAL_CHECKLIST.md          # Final checklist
    └── NEXT_STEPS.md               # Next steps
```

## 💡 How does it work?

### 1. The environment provides legacy code

```python
def f(x, y):
    result = []
    for i in range(len(x)):
        if x[i] > y:
            result.append(x[i])
    return result
```

**Problems**: Bad naming, no type hints, inefficient loop

### 2. The agent submits refactored code

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

### 3. The environment evaluates and rewards

```
Calculated metrics:
✓ Type hints: Added (+15 points)
✓ Docstring: Added (+10 points)
✓ Code conciseness: Improved (+5 points)
✓ Descriptive names: Improved
✓ List comprehension: Used

Total Reward: +13.0
Improvement Score: 80/100
```

## 🎮 Reward System

| Improvement | Points |
|-------------|---------|
| Invalid syntax | -10 |
| Type hints added | +15 |
| Docstrings added | +10 |
| Globals eliminated | +15 |
| Magic numbers fixed | +10 |
| Complexity reduced | +10 |
| Improvement bonus >70% | +5 |

**Maximum possible**: ~+18 points

## 🛠️ Technologies

- **OpenEnv** - RL environment framework
- **TRL** - Transformer Reinforcement Learning (GRPO)
- **Unsloth** - 2x faster optimization
- **vLLM** - Fast inference
- **FastAPI** - API server
- **HuggingFace Spaces** - Hosting
- **Northflank + CoreWeave** - H100 GPU

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [DEPLOY_NORTHFLANK_GUIDE.md](DEPLOY_NORTHFLANK_GUIDE.md) | Step-by-step H100 GPU deployment guide |
| [FINAL_CHECKLIST.md](FINAL_CHECKLIST.md) | Final checklist before submission |
| [NEXT_STEPS.md](NEXT_STEPS.md) | Detailed next steps |

## 🚀 Deployment on Northflank H100 GPU

### Quick Deploy (5 minutes setup)

1. **Login to Northflank**: https://northflank.com
2. **Create new Service**:
   - Source: GitHub → `muhammedehab35/CodeRefactor-Gym`
   - Branch: `main`
3. **Configure Build**:
   - Build Type: Dockerfile
   - Dockerfile Path: `Dockerfile.training`
4. **Set Resources**:
   - GPU: `NVIDIA H100` (1x)
   - RAM: `32 GB`
   - CPU: `8 cores`
5. **Add Environment Variables**:
   ```bash
   MODEL_ID=Qwen/Qwen2.5-1.5B-Instruct
   ENV_URL=https://mo35-code-refactor-gym.hf.space
   NUM_EPOCHS=3
   BATCH_SIZE=4
   ```
6. **Deploy** → Training starts automatically!

**📖 Detailed guide**: See [DEPLOY_NORTHFLANK_GUIDE.md](DEPLOY_NORTHFLANK_GUIDE.md)

**⏱️ Total time**: ~60 minutes (build: 15 min + training: 45 min)

## 📊 Expected Results

With H100 GPU (3 epochs):

| Metric | Epoch 1 | Epoch 2 | Epoch 3 |
|----------|---------|---------|---------|
| Average reward | 2-4 | 4-6 | 8-12 |
| Improvement | 30-40% | 50-60% | 70-80% |
| Syntax valid | >95% | >97% | >98% |
| Type hints | >70% | >80% | >90% |

## 🎯 Why is it innovative?

1. **First RL environment for code refactoring**
   - No similar environment exists in OpenEnv

2. **Real and measurable problem**
   - Refactoring is a daily challenge for developers
   - Objective metrics (complexity, type hints, etc.)

3. **Progressive learning**
   - From simple improvements to complex refactorings
   - Immediate feedback via rewards

4. **Immediately applicable**
   - Can be used on real legacy code
   - Trained model deployable in production

## 📞 Contact & Links

- **Participant**: mo35
- **HuggingFace**: [@mo35](https://huggingface.co/mo35)
- **Space**: [code-refactor-gym](https://huggingface.co/spaces/mo35/code-refactor-gym)
- **GitHub**: [CodeRefactor-Gym](https://github.com/muhammedehab35/CodeRefactor-Gym)

## 📄 License

Copyright (c) Meta Platforms, Inc. and affiliates.
BSD-style license (see OpenEnv project)

---

<div align="center">

**Made with ❤️ for OpenEnv Hackathon 2025**

[🚀 Deploy](DEPLOY_NORTHFLANK_GUIDE.md) • [✅ Checklist](FINAL_CHECKLIST.md) • [📋 Next Steps](NEXT_STEPS.md)

</div>
