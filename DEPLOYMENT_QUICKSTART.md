# 🚀 Deployment Quickstart - Northflank H100

> **Ready to train your AI agent on H100 GPU? Follow these steps!**

## ⚡ Prerequisites (2 minutes)

- [x] Environment deployed on HuggingFace: ✅ https://mo35-code-refactor-gym.hf.space
- [x] Code on GitHub: ✅ https://github.com/muhammedehab35/CodeRefactor-Gym
- [ ] Northflank account with H100 GPU access
- [ ] (Optional) HuggingFace token for auto model upload

## 📋 Steps (Total: ~60 minutes)

### Step 1: Login to Northflank (1 minute)

1. Go to https://northflank.com
2. Login with your hackathon credentials
3. Navigate to your project dashboard

### Step 2: Create Service (3 minutes)

1. Click **"Create Service"** or **"Create Job"**
2. Select **"From Git Repository"**
3. Choose provider: **GitHub**
4. Repository: **muhammedehab35/CodeRefactor-Gym**
5. Branch: **main**

### Step 3: Configure Build (2 minutes)

```yaml
Build Type: Dockerfile
Dockerfile Path: Dockerfile.training
Build Context: / (root directory)
```

### Step 4: Configure Resources (2 minutes)

```yaml
GPU:
  Type: NVIDIA H100 (via CoreWeave)
  Count: 1

CPU: 8 cores (8000m)
Memory: 32 GB (32Gi)
Storage: 50 GB
```

### Step 5: Environment Variables (2 minutes)

**Required variables:**

```bash
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

**Optional (for auto HuggingFace upload):**

```bash
HF_TOKEN=your_huggingface_token_here
```

### Step 6: Launch! (1 minute)

1. Click **"Create Service"**
2. Northflank will:
   - Build Docker image (~15 min)
   - Start training automatically
   - Run for ~45-60 minutes

## 📊 What to Expect

### Build Phase (~15 minutes)

```
✓ Installing CUDA drivers
✓ Installing PyTorch
✓ Installing TRL, Unsloth, vLLM
✓ Copying training scripts
✓ Image built successfully
```

### Training Phase (~45-60 minutes)

```
Epoch 1/3:
  ✓ Average reward: 2.5 → 4.0
  ✓ Improvement: 35% → 45%

Epoch 2/3:
  ✓ Average reward: 4.5 → 6.5
  ✓ Improvement: 50% → 62%

Epoch 3/3:
  ✓ Average reward: 7.0 → 10.5
  ✓ Improvement: 68% → 78%

✓ Training complete!
✓ Model saved to /app/output/code-refactor-agent
```

## 📈 Monitoring Training

### In Northflank Dashboard:

1. **Logs tab**: See real-time training progress
2. **Metrics tab**: Monitor GPU utilization (~80-95%)
3. **Resources tab**: Check memory usage

### Key metrics to watch:

- **Reward trend**: Should steadily increase (2 → 4 → 6 → 10+)
- **Improvement %**: Should increase (30% → 50% → 70%+)
- **Syntax validity**: Should stay >95%
- **GPU utilization**: Should be 80-95%

## 🎯 Success Criteria

### ✅ Training successful if:

- [x] All 3 epochs complete without errors
- [x] Final average reward > 8.0
- [x] Final improvement score > 65%
- [x] Syntax validity > 95%
- [x] Model saved successfully

### ⚠️ Troubleshooting

**Problem: Out of Memory**

```bash
# Reduce these variables:
BATCH_SIZE=2
NUM_GENERATIONS=4
MAX_LENGTH=512
```

**Problem: GPU not available**

1. Check Northflank GPU credits
2. Try different region
3. Contact hackathon support

**Problem: Environment connection fails**

```bash
# Verify environment is running:
curl https://mo35-code-refactor-gym.hf.space/health
# Should return: {"status":"healthy"}
```

## 🎁 After Training

### Option A: Auto-upload to HuggingFace (if HF_TOKEN set)

Model automatically available at:
```
https://huggingface.co/mo35/code-refactor-agent
```

### Option B: Download from Northflank

1. Go to Northflank volumes
2. Download `/app/output/code-refactor-agent/`
3. Contains:
   - Model weights
   - Tokenizer files
   - Training config

## 🧪 Test Your Trained Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from openenv.client import Client
from code_refactor_gym.models import CodeRefactorGymAction

# Load trained model
model = AutoModelForCausalLM.from_pretrained("mo35/code-refactor-agent")
tokenizer = AutoTokenizer.from_pretrained("mo35/code-refactor-agent")

# Connect to environment
client = Client(base_url="https://mo35-code-refactor-gym.hf.space")
obs = client.reset()

# Generate refactoring
prompt = f"""Refactor this code:
{obs.legacy_code}

Refactored version:"""

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=512, temperature=0.7)
refactored = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Get reward
action = CodeRefactorGymAction(
    refactored_code=refactored.split("Refactored version:")[-1].strip(),
    reasoning="AI-generated refactoring"
)
result = client.step(action)

print(f"✓ Reward: {result.reward}")
print(f"✓ Improvement: {result.improvement_score}/100")
```

## 📝 Document Your Results

Create a results document with:

1. **Training Metrics**
   - Screenshots of Northflank logs
   - Reward progression graph
   - Final metrics summary

2. **Example Refactorings**
   - 3-5 before/after code examples
   - Rewards obtained
   - Improvement scores

3. **Performance Analysis**
   - Training time
   - GPU utilization
   - Cost (if tracked)

## 🏁 Next Steps for Hackathon

1. ✅ Complete training on Northflank
2. ✅ Download/verify trained model
3. ✅ Test model on new code examples
4. ✅ Document results with screenshots
5. ✅ Update README with final results
6. ✅ (Optional) Create demo video
7. ✅ Submit to hackathon!

## 📞 Need Help?

- **Detailed deployment guide**: [DEPLOY_NORTHFLANK_GUIDE.md](DEPLOY_NORTHFLANK_GUIDE.md)
- **Final checklist**: [FINAL_CHECKLIST.md](FINAL_CHECKLIST.md)
- **Next steps**: [NEXT_STEPS.md](NEXT_STEPS.md)
- **Discord**: #openenv-hackathon channel
- **Northflank docs**: https://northflank.com/docs

---

## ⏱️ Timeline Summary

| Phase | Duration | Status |
|-------|----------|--------|
| Setup Northflank | 10 min | Ready |
| Docker build | 15 min | Automated |
| Training (3 epochs) | 45-60 min | Automated |
| Model download | 5 min | Manual |
| Testing | 10 min | Manual |
| **TOTAL** | **~90 minutes** | |

---

**🚀 Ready? Start with Step 1 above!**

**Everything is already configured - just follow the steps! Good luck! 🍀**
