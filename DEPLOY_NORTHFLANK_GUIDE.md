# Northflank Deployment Guide - Step by Step

## ✅ Prerequisites

1. ✅ Environment deployed: https://mo35-code-refactor-gym.hf.space
2. ✅ Code ready to be pushed to GitHub
3. ⏳ Northflank account with H100 GPU access
4. ⏳ HuggingFace token (for automatic model upload)

---

## STEP 1: Push Code to GitHub

### Option A: Via automatic script

```bash
# Double-click on:
PUSH_TO_GITHUB.bat
```

### Option B: Manually

```bash
cd "D:\Northflank + openv"

git init
git add .
git commit -m "Complete OpenEnv Hackathon setup"
git remote add origin https://github.com/muhammedehab35/CodeRefactor-Gym.git
git branch -M main
git push -u origin main --force
```

**✅ Verification**: Visit https://github.com/muhammedehab35/CodeRefactor-Gym

---

## STEP 2: Connect to Northflank

1. Go to https://northflank.com
2. Login with your hackathon account
3. You should see a dashboard

---

## STEP 3: Create a New Service/Job

### 3.1 Create the Service

1. Click on **"Create Service"** or **"Create Job"**
2. Select **"From Git Repository"**
3. Connect your GitHub account if not already done

### 3.2 Configure the Repository

- **Repository**: `muhammedehab35/CodeRefactor-Gym`
- **Branch**: `main`
- **Build Type**: `Dockerfile`
- **Dockerfile Path**: `Dockerfile.training`
- **Build Context**: `/` (root)

### 3.3 Name the Service

- **Service Name**: `code-refactor-training`
- **Description**: `CodeRefactor Gym GRPO Training with H100`

---

## STEP 4: Configure GPU Resources

### 4.1 Select the GPU

In the **"Resources"** section:

- **GPU Type**: `NVIDIA H100` (via CoreWeave)
- **GPU Count**: `1`
- **CPU**: `8 cores` (8000m)
- **Memory**: `32 GB` (32Gi)
- **Storage**: `50 GB`

### 4.2 Check Availability

⚠️ **Important**: There are 120 H100 GPUs total, 1 per team
- If "H100" doesn't appear, contact hackathon support
- Verify that your account has GPU credit access

---

## STEP 5: Environment Variables

Add these variables in **"Environment Variables"**:

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

### 5.2 (Optional) HuggingFace Token

For automatic upload of trained model:

```
HF_TOKEN=your_huggingface_token_here
```

### 5.3 (Optional) Weights & Biases

For advanced monitoring:

```
WANDB_API_KEY=your_wandb_key
WANDB_PROJECT=code-refactor-gym
```

---

## STEP 6: Advanced Configuration (Optional)

### 6.1 Persistent Volumes

To save the model:

- **Volume Name**: `model-output`
- **Mount Path**: `/app/output`
- **Size**: `20 GB`

### 6.2 Ports

If you want to expose TensorBoard:

- **Port Name**: `tensorboard`
- **Port**: `6006`
- **Protocol**: `HTTP`

---

## STEP 7: Launch Build & Deployment

1. Click **"Create Service"** at the bottom
2. Northflank will:
   - Clone your GitHub repo
   - Build Docker image (Dockerfile.training)
   - Pull CUDA base image
   - Install dependencies
   - ⏱️ This takes ~10-15 minutes

### 7.1 Monitor the Build

- Go to **"Builds"** tab
- You'll see real-time logs:
  ```
  ✓ Pulling base image nvidia/cuda:12.1.0
  ✓ Installing Python 3.11
  ✓ Installing PyTorch with CUDA
  ✓ Installing TRL, transformers, vLLM
  ✓ Copying training script
  ```

---

## STEP 8: Launch Training

Once the build is complete:

1. Container starts automatically
2. `train_agent.py` script executes
3. Training begins

### 8.1 View Logs

Go to **"Logs"** to see:

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

## STEP 9: Monitoring

### 9.1 Northflank Metrics

In the Northflank dashboard:
- **GPU Utilization**: Should be ~80-95%
- **Memory Usage**: ~25-28 GB / 32 GB
- **CPU Usage**: ~60-70%

### 9.2 Training Logs

Monitor these metrics in the logs:
- **Average reward**: Should increase (2→4→6→8→10+)
- **Improvement score**: Should increase (30%→50%→70%+)
- **Syntax valid rate**: Should be >95%

### 9.3 Estimated Duration

With H100 + vLLM:
- **Epoch 1**: ~15-20 minutes
- **Epoch 2**: ~15-20 minutes
- **Epoch 3**: ~15-20 minutes
- **Total**: ~45-60 minutes

---

## STEP 10: Retrieve the Model

### Option A: Persistent Volume

If you configured a volume:
1. Go to **"Files"** > **"Volumes"**
2. Download `/app/output/code-refactor-agent/`

### Option B: HuggingFace Hub (Recommended)

If HF_TOKEN configured, model is uploaded automatically:
- URL: https://huggingface.co/mo35/code-refactor-agent

Verify with:
```python
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained("mo35/code-refactor-agent")
```

### Option C: Logs

The model path is displayed in the final logs:
```
Training complete!
Model saved to: /app/output/code-refactor-agent
```

---

## STEP 11: Test the Trained Model

After retrieving the model:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from openenv.client import Client

# Load the model
model = AutoModelForCausalLM.from_pretrained("mo35/code-refactor-agent")
tokenizer = AutoTokenizer.from_pretrained("mo35/code-refactor-agent")

# Connect to environment
client = Client(base_url="https://mo35-code-refactor-gym.hf.space")
obs = client.reset()

# Test refactoring
legacy_code = obs.legacy_code
prompt = f"Refactor this code:\n{legacy_code}\n\nRefactored version:"

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=512, temperature=0.7)
refactored = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("Legacy Code:")
print(legacy_code)
print("\nRefactored Code:")
print(refactored)

# Evaluate in environment
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

## 🚨 Troubleshooting

### Error: "No GPU available"

**Solution**: Check with hackathon support that your account has H100 GPU access

### Error: "Out of memory"

**Solutions**:
```bash
# Reduce batch size
BATCH_SIZE=2
NUM_GENERATIONS=4

# Or activate Unsloth in train_agent.py
--use-unsloth
```

### Error: "Cannot connect to environment"

**Solution**: Verify that the environment is accessible:
```bash
curl https://mo35-code-refactor-gym.hf.space/health
# Should return: {"status":"healthy"}
```

### Build fails

**Solution**: Check build logs in Northflank > Builds > Logs

---

## 📊 Expected Results

### Performance Metrics

With H100:
- **Throughput**: ~100-150 tokens/sec
- **GPU Memory**: ~25-30 GB / 80 GB
- **Training Speed**: ~2-3 min/epoch

### Quality Metrics

After 3 epochs:
- **Average reward**: 8-12
- **Improvement score**: 60-80%
- **Syntax valid**: >98%
- **Type hints added**: >85%
- **Docstrings added**: >75%

---

## ✅ Final Checklist

- [ ] Code pushed to GitHub
- [ ] Northflank service created
- [ ] H100 GPU configured
- [ ] Environment variables set
- [ ] Build successful
- [ ] Training launched
- [ ] Logs monitored
- [ ] Model retrieved
- [ ] Model tested
- [ ] Results documented

---

## 🎯 Next Step

After successful training:
1. Document your results
2. Create refactoring examples
3. Prepare your hackathon submission!

**Good luck! 🚀**
