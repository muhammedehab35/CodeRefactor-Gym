# Prochaines étapes - CodeRefactor Gym Hackathon

## ✅ Ce qui est fait

1. **Environnement OpenEnv créé** ✅
   - 5 types de code legacy différents
   - Système de métriques de qualité complet
   - Récompenses basées sur amélioration
   - Validation syntaxe AST

2. **Déployé sur HuggingFace Spaces** ✅
   - URL: https://huggingface.co/spaces/mo35/code-refactor-gym
   - API: https://mo35-code-refactor-gym.hf.space
   - Tests réussis avec reward +13.0 pour bon refactoring

3. **Pipeline d'entraînement préparé** ✅
   - Script train_agent.py avec GRPO/TRL
   - Support Unsloth pour 2x plus rapide
   - Support vLLM pour inférence rapide
   - Dockerfile pour Northflank H100

4. **Documentation complète** ✅
   - README_HACKATHON.md
   - NORTHFLANK_DEPLOYMENT.md
   - Guide de déploiement détaillé

## 🎯 Ce qu'il reste à faire

### Étape 1: Déployer sur Northflank (PRIORITÉ)

Tu dois maintenant déployer le training sur Northflank avec le GPU H100.

**Option A: Via l'interface web Northflank**

1. Va sur https://northflank.com
2. Connecte-toi avec ton compte hackathon
3. Crée un nouveau "Job" ou "Service"
4. Configure:
   - Repository: Pousse le code sur GitHub
   - Dockerfile: `Dockerfile.training`
   - GPU: NVIDIA H100 (1x)
   - RAM: 32GB
   - CPU: 8 cores

5. Variables d'environnement:
   ```
   MODEL_ID=Qwen/Qwen2.5-1.5B-Instruct
   ENV_URL=https://mo35-code-refactor-gym.hf.space
   NUM_EPOCHS=3
   BATCH_SIZE=4
   ```

6. Lance le build et le déploiement

**Option B: Push vers GitHub puis connect à Northflank**

```bash
# 1. Créer un repo GitHub
cd "D:\Northflank + openv"
git init
git add .
git commit -m "CodeRefactor Gym - OpenEnv Hackathon"

# 2. Créer repo sur GitHub
# Aller sur github.com/new
# Nom: openenv-hackathon-code-refactor

# 3. Pousser
git remote add origin https://github.com/TON-USERNAME/openenv-hackathon-code-refactor.git
git branch -M main
git push -u origin main

# 4. Dans Northflank, connecter ce repo
# Northflank > Create Service > From Git Repository
```

### Étape 2: Lancer l'entraînement

Une fois déployé sur Northflank:

1. Le container démarre automatiquement
2. L'entraînement commence (3 epochs ≈ 30-60 minutes avec H100)
3. Surveille les logs dans Northflank:
   - Reward moyen par epoch
   - Improvement scores
   - GPU utilization

### Étape 3: Récupérer le modèle entraîné

**Option 1: Volume persistant**

Configure un volume dans Northflank:
```yaml
volumes:
  - name: model-output
    mountPath: /app/output
    size: 20Gi
```

**Option 2: Upload auto vers HuggingFace**

Modifie `train_agent.py` ligne ~270:

```python
# À la fin de main(), ajoute:
print("\nUploading model to HuggingFace Hub...")
model.push_to_hub("mo35/code-refactor-agent")
tokenizer.push_to_hub("mo35/code-refactor-agent")
print("Model uploaded to: https://huggingface.co/mo35/code-refactor-agent")
```

Puis ajoute variable d'environnement dans Northflank:
```
HF_TOKEN=your_huggingface_token_here
```

### Étape 4: Évaluer le modèle

Après l'entraînement, teste le modèle:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Charger le modèle entraîné
model = AutoModelForCausalLM.from_pretrained("mo35/code-refactor-agent")
tokenizer = AutoTokenizer.from_pretrained("mo35/code-refactor-agent")

# Test sur nouveau code legacy
legacy_code = """
def calc(x, y):
    if x > 0:
        if y > 0:
            return x + y
"""

prompt = f"Refactor this code:\n{legacy_code}\n\nRefactored version:"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=512)
refactored = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(refactored)
```

### Étape 5: Soumission au hackathon

1. **README final**: Ajoute screenshots/résultats
2. **Vidéo démo** (optionnel): Montre l'environnement + training
3. **Métriques**: Documente les résultats:
   - Reward moyen avant/après training
   - Improvement score moyen
   - Exemples de refactoring réussis

4. **Soumets via le formulaire du hackathon**

## 🚀 Commandes rapides

### Test local de l'environnement
```bash
cd "D:\Northflank + openv\code_refactor_gym"
python test_env.py
```

### Vérifier que l'environnement est accessible
```bash
curl https://mo35-code-refactor-gym.hf.space/health
```

### Build Docker local (test)
```bash
cd "D:\Northflank + openv"
docker build -f Dockerfile.training -t code-refactor-training .
```

### Test training local (si GPU)
```bash
python train_agent.py \
  --model-id Qwen/Qwen2.5-0.5B-Instruct \
  --num-epochs 1 \
  --batch-size 2
```

## 📊 Optimisations possibles

### Si l'entraînement est trop lent:

```bash
# Utilise Unsloth
python train_agent.py --use-unsloth

# Réduis batch size
python train_agent.py --batch-size 2

# Utilise modèle plus petit
python train_agent.py --model-id Qwen/Qwen2.5-0.5B-Instruct
```

### Si Out of Memory:

```bash
python train_agent.py \
  --batch-size 2 \
  --num-generations 4 \
  --max-length 512 \
  --use-unsloth
```

## 🎯 Objectifs de performance

Avec H100 + Unsloth:

- **Vitesse**: ~2-3 minutes par epoch
- **Reward cible**:
  - Epoch 1: reward moyen ~2-4
  - Epoch 2: reward moyen ~6-8
  - Epoch 3: reward moyen ~10-12

- **Improvement cible**:
  - Epoch 1: ~30-40% improvement
  - Epoch 2: ~50-60% improvement
  - Epoch 3: ~70-80% improvement

## ❓ FAQ

**Q: Combien de temps prend l'entraînement?**
A: Avec H100 + Unsloth: ~30-45 minutes pour 3 epochs

**Q: Puis-je utiliser un modèle plus gros?**
A: Oui! Essaye `Qwen/Qwen2.5-3B-Instruct` ou `Qwen/Qwen2.5-7B-Instruct`

**Q: Comment monitorer en temps réel?**
A: Via les logs Northflank ou ajoute Weights & Biases

**Q: Et si l'environnement crash?**
A: Vérifie les logs HuggingFace Spaces, restart si nécessaire

## 📞 Support

**Documentation officielle:**
- OpenEnv: https://github.com/meta-pytorch/OpenEnv
- TRL: https://huggingface.co/docs/trl
- Northflank: https://northflank.com/docs

**Discord Hackathon:**
- Cherche dans #support ou #openenv

---

**Bonne chance pour le hackathon! 🚀**
