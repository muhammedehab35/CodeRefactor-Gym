# Guide de Déploiement Northflank - Étape par Étape

## ✅ Prérequis

1. ✅ Environnement déployé: https://mo35-code-refactor-gym.hf.space
2. ✅ Code prêt à être poussé sur GitHub
3. ⏳ Compte Northflank avec accès GPU H100
4. ⏳ HuggingFace token (pour upload automatique du modèle)

---

## ÉTAPE 1: Pousser le code sur GitHub

### Option A: Via le script automatique

```bash
# Double-cliquer sur:
PUSH_TO_GITHUB.bat
```

### Option B: Manuellement

```bash
cd "D:\Northflank + openv"

git init
git add .
git commit -m "Complete OpenEnv Hackathon setup"
git remote add origin https://github.com/muhammedehab35/CodeRefactor-Gym.git
git branch -M main
git push -u origin main --force
```

**✅ Vérification**: Visite https://github.com/muhammedehab35/CodeRefactor-Gym

---

## ÉTAPE 2: Se connecter à Northflank

1. Va sur https://northflank.com
2. Connecte-toi avec ton compte hackathon
3. Tu devrais voir un dashboard

---

## ÉTAPE 3: Créer un nouveau Service/Job

### 3.1 Créer le Service

1. Clique sur **"Create Service"** ou **"Create Job"**
2. Sélectionne **"From Git Repository"**
3. Connecte ton compte GitHub si pas déjà fait

### 3.2 Configurer le Repository

- **Repository**: `muhammedehab35/CodeRefactor-Gym`
- **Branch**: `main`
- **Build Type**: `Dockerfile`
- **Dockerfile Path**: `Dockerfile.training`
- **Build Context**: `/` (root)

### 3.3 Nommer le Service

- **Service Name**: `code-refactor-training`
- **Description**: `CodeRefactor Gym GRPO Training with H100`

---

## ÉTAPE 4: Configurer les Ressources GPU

### 4.1 Sélectionner le GPU

Dans la section **"Resources"**:

- **GPU Type**: `NVIDIA H100` (via CoreWeave)
- **GPU Count**: `1`
- **CPU**: `8 cores` (8000m)
- **Memory**: `32 GB` (32Gi)
- **Storage**: `50 GB`

### 4.2 Vérifier la disponibilité

⚠️ **Important**: Il y a 120 GPUs H100 total, 1 par équipe
- Si "H100" n'apparaît pas, contacte le support hackathon
- Vérifie que ton compte a l'accès au crédit GPU

---

## ÉTAPE 5: Variables d'Environnement

Ajoute ces variables dans **"Environment Variables"**:

```
MODEL_ID=Qwen/Qwen2.5-1.5B-Instruct
ENV_URL=https://mo35-code-refactor-gym.hf.space
NUM_EPOCHS=3
BATCH_SIZE=4
NUM_GENERATIONS=8
MAX_LENGTH=1024
LEARNING_RATE=5e-6
OUTPUT_DIR=/app/output/code-refactor-agent
USE_VLLM=true
PYTHONUNBUFFERED=1
```

### 5.2 (Optionnel) HuggingFace Token

Pour upload automatique du modèle entraîné:

```
HF_TOKEN=your_huggingface_token_here
```

### 5.3 (Optionnel) Weights & Biases

Pour monitoring avancé:

```
WANDB_API_KEY=ton_wandb_key
WANDB_PROJECT=code-refactor-gym
```

---

## ÉTAPE 6: Configuration Avancée (Optionnel)

### 6.1 Volumes Persistants

Pour sauvegarder le modèle:

- **Volume Name**: `model-output`
- **Mount Path**: `/app/output`
- **Size**: `20 GB`

### 6.2 Ports

Si tu veux exposer TensorBoard:

- **Port Name**: `tensorboard`
- **Port**: `6006`
- **Protocol**: `HTTP`

---

## ÉTAPE 7: Lancer le Build & Déploiement

1. Clique sur **"Create Service"** en bas
2. Northflank va:
   - Clone ton repo GitHub
   - Build l'image Docker (Dockerfile.training)
   - Pull CUDA base image
   - Install dependencies
   - ⏱️ Cela prend ~10-15 minutes

### 7.1 Surveiller le Build

- Va dans l'onglet **"Builds"**
- Tu verras les logs en temps réel:
  ```
  ✓ Pulling base image nvidia/cuda:12.1.0
  ✓ Installing Python 3.11
  ✓ Installing PyTorch with CUDA
  ✓ Installing TRL, transformers, vLLM
  ✓ Copying training script
  ```

---

## ÉTAPE 8: Lancer l'Entraînement

Une fois le build terminé:

1. Le container démarre automatiquement
2. Le script `train_agent.py` s'exécute
3. L'entraînement commence

### 8.1 Voir les Logs

Va dans **"Logs"** pour voir:

```
========================================
CodeRefactor Gym - GRPO Training
========================================
Model: Qwen/Qwen2.5-1.5B-Instruct
Environment: https://mo35-code-refactor-gym.hf.space
Output: /app/output/code-refactor-agent
Epochs: 3
Batch size: 4
Use Unsloth: False
========================================

Loading model...
Creating training dataset...
Dataset size: 80 examples

Initializing GRPO trainer...

========================================
Starting training...
========================================

Epoch 1/3:
  Step 10: reward=2.3, improvement=35.2
  Step 20: reward=3.1, improvement=42.8
  ...
```

---

## ÉTAPE 9: Monitoring

### 9.1 Métriques Northflank

Dans le dashboard Northflank:
- **GPU Utilization**: Doit être ~80-95%
- **Memory Usage**: ~25-28 GB / 32 GB
- **CPU Usage**: ~60-70%

### 9.2 Logs de Training

Surveille ces métriques dans les logs:
- **Reward moyen**: Doit augmenter (2→4→6→8→10+)
- **Improvement score**: Doit augmenter (30%→50%→70%+)
- **Syntax valid rate**: Doit être >95%

### 9.3 Durée Estimée

Avec H100 + vLLM:
- **Epoch 1**: ~15-20 minutes
- **Epoch 2**: ~15-20 minutes
- **Epoch 3**: ~15-20 minutes
- **Total**: ~45-60 minutes

---

## ÉTAPE 10: Récupérer le Modèle

### Option A: Volume Persistant

Si tu as configuré un volume:
1. Va dans **"Files"** > **"Volumes"**
2. Télécharge `/app/output/code-refactor-agent/`

### Option B: HuggingFace Hub (Recommandé)

Si HF_TOKEN configuré, le modèle est uploadé automatiquement:
- URL: https://huggingface.co/mo35/code-refactor-agent

Vérifie avec:
```python
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained("mo35/code-refactor-agent")
```

### Option C: Logs

Le chemin du modèle est affiché dans les logs finaux:
```
Training complete!
Model saved to: /app/output/code-refactor-agent
```

---

## ÉTAPE 11: Test du Modèle Entraîné

Après récupération du modèle:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from openenv.client import Client

# Charger le modèle
model = AutoModelForCausalLM.from_pretrained("mo35/code-refactor-agent")
tokenizer = AutoTokenizer.from_pretrained("mo35/code-refactor-agent")

# Connecter à l'environnement
client = Client(base_url="https://mo35-code-refactor-gym.hf.space")
obs = client.reset()

# Tester le refactoring
legacy_code = obs.legacy_code
prompt = f"Refactor this code:\n{legacy_code}\n\nRefactored version:"

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=512, temperature=0.7)
refactored = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("Legacy Code:")
print(legacy_code)
print("\nRefactored Code:")
print(refactored)

# Évaluer dans l'environnement
from code_refactor_gym.models import CodeRefactorGymAction
action = CodeRefactorGymAction(
    refactored_code=refactored.split("Refactored version:")[-1].strip(),
    reasoning="AI refactoring"
)
result = client.step(action)
print(f"\nReward: {result.reward}")
print(f"Improvement: {result.improvement_score}/100")
```

---

## 🚨 Dépannage

### Erreur: "No GPU available"

**Solution**: Vérifie avec le support hackathon que ton compte a accès au GPU H100

### Erreur: "Out of memory"

**Solutions**:
```bash
# Réduire batch size
BATCH_SIZE=2
NUM_GENERATIONS=4

# Ou activer Unsloth dans train_agent.py
--use-unsloth
```

### Erreur: "Cannot connect to environment"

**Solution**: Vérifie que l'environnement est accessible:
```bash
curl https://mo35-code-refactor-gym.hf.space/health
# Doit retourner: {"status":"healthy"}
```

### Build échoue

**Solution**: Regarde les logs de build dans Northflank > Builds > Logs

---

## 📊 Résultats Attendus

### Métriques de Performance

Avec H100:
- **Throughput**: ~100-150 tokens/sec
- **GPU Memory**: ~25-30 GB / 80 GB
- **Training Speed**: ~2-3 min/epoch

### Métriques de Qualité

Après 3 epochs:
- **Reward moyen**: 8-12
- **Improvement score**: 60-80%
- **Syntax valid**: >98%
- **Type hints ajoutés**: >85%
- **Docstrings ajoutés**: >75%

---

## ✅ Checklist Finale

- [ ] Code poussé sur GitHub
- [ ] Service Northflank créé
- [ ] GPU H100 configuré
- [ ] Variables d'environnement set
- [ ] Build réussi
- [ ] Training lancé
- [ ] Logs surveillés
- [ ] Modèle récupéré
- [ ] Modèle testé
- [ ] Résultats documentés

---

## 🎯 Prochaine Étape

Après l'entraînement réussi:
1. Documente tes résultats
2. Crée des exemples de refactoring
3. Prépare ta soumission au hackathon!

**Bon courage! 🚀**
