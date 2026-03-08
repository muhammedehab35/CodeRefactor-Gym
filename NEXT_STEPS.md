# Next Steps - CodeRefactor Gym Hackathon

## ✅ What's Done

1. **OpenEnv Environment Created** ✅
   - 5 different legacy code types
   - Complete quality metrics system
   - Improvement-based rewards
   - AST syntax validation

2. **Deployed on HuggingFace Spaces** ✅
   - URL: https://huggingface.co/spaces/mo35/code-refactor-gym
   - API: https://mo35-code-refactor-gym.hf.space
   - Successful tests with +13.0 reward for good refactoring

3. **Training Pipeline Prepared** ✅
   - train_agent.py script with GRPO/TRL
   - Unsloth support for 2x faster
   - vLLM support for fast inference
   - Dockerfile for Northflank H100

4. **Complete Documentation** ✅
   - README.md (main documentation)
   - DEPLOY_NORTHFLANK_GUIDE.md (deployment guide)
   - FINAL_CHECKLIST.md (submission checklist)

## 🎯 What Remains to be Done

### Step 1: Deploy on Northflank (PRIORITY)

You must now deploy the training on Northflank with the H100 GPU.

**Option A: Via Northflank web interface**

1. Go to https://northflank.com
2. Login with your hackathon account
3. Create a new "Job" or "Service"
4. Configure:
   - Repository: Push code to GitHub
   - Dockerfile: `Dockerfile.training`
   - GPU: NVIDIA H100 (1x)
   - RAM: 32GB
   - CPU: 8 cores

5. Environment variables:
   ```
   MODEL_ID=Qwen/Qwen2.5-1.5B-Instruct
   ENV_URL=https://mo35-code-refactor-gym.hf.space
   NUM_EPOCHS=3
   BATCH_SIZE=4
   ```

6. Launch build and deployment

**Option B: Push to GitHub then connect to Northflank**

```bash
# 1. Create a GitHub repo
cd "D:\Northflank + openv"
git init
git add .
git commit -m "CodeRefactor Gym - OpenEnv Hackathon"

# 2. Create repo on GitHub
# Go to github.com/new
# Name: openenv-hackathon-code-refactor

# 3. Push
git remote add origin https://github.com/YOUR-USERNAME/openenv-hackathon-code-refactor.git
git branch -M main
git push -u origin main

# 4. In Northflank, connect this repo
# Northflank > Create Service > From Git Repository
```

### Step 2: Launch Training

Once deployed on Northflank:

1. Container starts automatically
2. Training begins (3 epochs ≈ 30-60 minutes with H100)
3. Monitor logs in Northflank:
   - Average reward per epoch
   - Improvement scores
   - GPU utilization

### Step 3: Retrieve Trained Model

**Option 1: Persistent volume**

Configure a volume in Northflank:
```yaml
volumes:
  - name: model-output
    mountPath: /app/output
    size: 20Gi
```

**Option 2: Auto upload to HuggingFace**

Modify `train_agent.py` line ~270:

```python
# At the end of main(), add:
print("\nUploading model to HuggingFace Hub...")
model.push_to_hub("mo35/code-refactor-agent")
tokenizer.push_to_hub("mo35/code-refactor-agent")
print("Model uploaded to: https://huggingface.co/mo35/code-refactor-agent")
```

Then add environment variable in Northflank:
```
HF_TOKEN=your_huggingface_token_here
```

### Step 4: Evaluate the Model

After training, test the model:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load trained model
model = AutoModelForCausalLM.from_pretrained("mo35/code-refactor-agent")
tokenizer = AutoTokenizer.from_pretrained("mo35/code-refactor-agent")

# Test on new legacy code
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

### Step 5: Hackathon Submission

1. **Final README**: Add screenshots/results
2. **Demo video** (optional): Show environment + training
3. **Metrics**: Document results:
   - Average reward before/after training
   - Average improvement score
   - Examples of successful refactorings

4. **Submit via hackathon form**

## 🚀 Quick Commands

### Local environment test
```bash
cd "D:\Northflank + openv\code_refactor_gym"
python test_env.py
```

### Verify environment is accessible
```bash
curl https://mo35-code-refactor-gym.hf.space/health
```

### Local Docker build (test)
```bash
cd "D:\Northflank + openv"
docker build -f Dockerfile.training -t code-refactor-training .
```

### Local training test (if GPU)
```bash
python train_agent.py \
  --model-id Qwen/Qwen2.5-0.5B-Instruct \
  --num-epochs 1 \
  --batch-size 2
```

## 📊 Possible Optimizations

### If training is too slow:

```bash
# Use Unsloth
python train_agent.py --use-unsloth

# Reduce batch size
python train_agent.py --batch-size 2

# Use smaller model
python train_agent.py --model-id Qwen/Qwen2.5-0.5B-Instruct
```

### If Out of Memory:

```bash
python train_agent.py \
  --batch-size 2 \
  --num-generations 4 \
  --max-length 512 \
  --use-unsloth
```

## 🎯 Performance Goals

With H100 + Unsloth:

- **Speed**: ~2-3 minutes per epoch
- **Reward target**:
  - Epoch 1: average reward ~2-4
  - Epoch 2: average reward ~6-8
  - Epoch 3: average reward ~10-12

- **Improvement target**:
  - Epoch 1: ~30-40% improvement
  - Epoch 2: ~50-60% improvement
  - Epoch 3: ~70-80% improvement

## ❓ FAQ

**Q: How long does training take?**
A: With H100 + Unsloth: ~30-45 minutes for 3 epochs

**Q: Can I use a larger model?**
A: Yes! Try `Qwen/Qwen2.5-3B-Instruct` or `Qwen/Qwen2.5-7B-Instruct`

**Q: How to monitor in real-time?**
A: Via Northflank logs or add Weights & Biases

**Q: What if the environment crashes?**
A: Check HuggingFace Spaces logs, restart if necessary

## 📞 Support

**Official Documentation:**
- OpenEnv: https://github.com/meta-pytorch/OpenEnv
- TRL: https://huggingface.co/docs/trl
- Northflank: https://northflank.com/docs

**Discord Hackathon:**
- Look in #support or #openenv

---

**Good luck with the hackathon! 🚀**
