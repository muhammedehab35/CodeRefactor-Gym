# Déploiement sur Northflank avec GPU H100

Ce guide explique comment déployer l'entraînement CodeRefactor Gym sur Northflank avec un GPU H100.

## Prérequis

1. Compte Northflank avec accès au hackathon OpenEnv
2. GPU H100 alloué (1 GPU par équipe)
3. Environnement déployé sur HuggingFace Spaces: `https://mo35-code-refactor-gym.hf.space`

## Étape 1: Se connecter à Northflank

1. Aller sur https://northflank.com
2. Se connecter avec ton compte du hackathon
3. Vérifier que tu as accès au GPU H100

## Étape 2: Créer un nouveau Job/Service

### Option A: Via l'interface Northflank

1. Cliquer sur "Create Service" ou "Create Job"
2. Sélectionner "Docker"
3. Configurer:
   - **Name**: `code-refactor-training`
   - **Build Type**: Dockerfile
   - **Dockerfile path**: `Dockerfile.training`
   - **Context**: Repository root

4. Configurer les ressources:
   - **GPU**: 1x NVIDIA H100 (via CoreWeave)
   - **CPU**: 8 cores
   - **RAM**: 32 GB
   - **Storage**: 50 GB

5. Variables d'environnement:
   ```
   MODEL_ID=Qwen/Qwen2.5-1.5B-Instruct
   ENV_URL=https://mo35-code-refactor-gym.hf.space
   NUM_EPOCHS=3
   BATCH_SIZE=4
   OUTPUT_DIR=/app/output/code-refactor-agent
   ```

### Option B: Via northflank.yaml (recommandé)

Créer un fichier `northflank.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: code-refactor-training
spec:
  dockerfile: Dockerfile.training
  buildArguments: []

  resources:
    gpu:
      type: H100
      count: 1
    cpu: 8000m  # 8 cores
    memory: 32Gi
    storage: 50Gi

  env:
    - name: MODEL_ID
      value: "Qwen/Qwen2.5-1.5B-Instruct"
    - name: ENV_URL
      value: "https://mo35-code-refactor-gym.hf.space"
    - name: NUM_EPOCHS
      value: "3"
    - name: BATCH_SIZE
      value: "4"
    - name: USE_VLLM
      value: "true"

  ports:
    - name: metrics
      port: 6006
      protocol: HTTP

  healthcheck:
    path: /health
    port: 8000
```

## Étape 3: Pousser le code

```bash
# Créer un repo Git pour Northflank
cd "D:\Northflank + openv"
git init
git add train_agent.py requirements-training.txt Dockerfile.training
git commit -m "Add training pipeline for CodeRefactor Gym"

# Pousser vers Northflank ou GitHub
# Northflank peut se connecter à GitHub/GitLab
```

## Étape 4: Configurer le build

Dans Northflank:

1. Connecter le repository GitHub
2. Sélectionner la branche (ex: `main`)
3. Vérifier le Dockerfile: `Dockerfile.training`
4. Build automatiquement sur push

## Étape 5: Lancer l'entraînement

### Méthode 1: Via l'interface

1. Cliquer sur "Deploy" ou "Run Job"
2. Vérifier les logs en temps réel
3. L'entraînement commence automatiquement

### Méthode 2: Via CLI

```bash
# Installer Northflank CLI
npm install -g @northflank/cli

# Se connecter
northflank login

# Déployer
northflank job create \
  --name code-refactor-training \
  --image-source dockerfile \
  --dockerfile-path Dockerfile.training \
  --gpu-type H100 \
  --gpu-count 1 \
  --cpu 8000m \
  --memory 32Gi
```

## Étape 6: Monitorer l'entraînement

### Logs en temps réel

Dans Northflank:
- Aller dans "Logs" pour voir les sorties
- Surveiller les métriques de reward
- Vérifier l'utilisation du GPU

### TensorBoard (optionnel)

Si configuré dans le script:

```bash
# Le port 6006 expose TensorBoard
# URL: https://your-service.northflank.app:6006
```

### Weights & Biases (optionnel)

Ajouter dans `train_agent.py`:

```python
import wandb

wandb.init(
    project="code-refactor-gym",
    name="grpo-training",
    config=vars(args)
)
```

Puis ajouter variable d'environnement:
```
WANDB_API_KEY=your_wandb_key
```

## Étape 7: Récupérer le modèle entraîné

### Option 1: Volumes persistants

Configurer un volume dans Northflank:
```yaml
volumes:
  - name: model-output
    mountPath: /app/output
    size: 20Gi
```

### Option 2: Upload vers HuggingFace Hub

Modifier `train_agent.py` pour pusher automatiquement:

```python
# À la fin de main()
if args.push_to_hub:
    model.push_to_hub("mo35/code-refactor-agent")
    tokenizer.push_to_hub("mo35/code-refactor-agent")
```

Ajouter variable d'environnement:
```
HF_TOKEN=your_huggingface_token
```

## Optimisations Performance

### Utiliser Unsloth (2x plus rapide)

```bash
# Dans Dockerfile.training, décommenter:
RUN pip install "unsloth[cu121] @ git+https://github.com/unslothai/unsloth.git"
```

Puis lancer avec:
```bash
python train_agent.py --use-unsloth
```

Avantages:
- 2x plus rapide
- 70% moins de mémoire
- 4-bit quantization + LoRA

### Ajuster batch size

Pour GPU H100 (80GB VRAM):
```bash
--batch-size 8          # Plus rapide
--num-generations 16    # Plus d'échantillons
```

### vLLM pour inférence rapide

Déjà activé par défaut:
```bash
--use-vllm
```

## Coûts et limites

- **GPU H100**: Gratuit pendant le hackathon (1 GPU/équipe)
- **Durée**: Pas de limite de temps
- **Storage**: 50GB inclus
- **Bande passante**: Illimitée vers HuggingFace

## Dépannage

### Erreur: Out of memory

Réduire:
```bash
--batch-size 2
--num-generations 4
--max-length 512
```

### Erreur: Cannot connect to environment

Vérifier que l'environnement est déployé:
```bash
curl https://mo35-code-refactor-gym.hf.space/health
```

### Build échoue

Vérifier les logs dans Northflank > Build Logs

## Résumé des commandes

```bash
# 1. Préparer le code
cd "D:\Northflank + openv"

# 2. Build Docker local (test)
docker build -f Dockerfile.training -t code-refactor-training .

# 3. Test local (si GPU disponible)
docker run --gpus all code-refactor-training

# 4. Déployer sur Northflank
# Via l'interface web ou CLI

# 5. Monitorer
# Via logs Northflank ou TensorBoard
```

## Prochaines étapes

Après l'entraînement:
1. Télécharger le modèle entraîné
2. Tester sur de nouveaux exemples de code legacy
3. Évaluer les métriques de qualité
4. Soumettre au hackathon OpenEnv!
