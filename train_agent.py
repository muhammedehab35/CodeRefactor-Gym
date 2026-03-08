#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Training script for CodeRefactor Gym using TRL GRPO on H100 GPU.

This script trains an LLM agent to refactor legacy code using:
- TRL (Transformer Reinforcement Learning) with GRPO
- OpenEnv CodeRefactor Gym environment
- Optional Unsloth optimization for 2x faster training
"""

import argparse
from datasets import Dataset
from trl import GRPOTrainer, GRPOConfig
from trl.trainer.grpo_trainer import generate_rollout_completions
from transformers import AutoTokenizer
from openenv.client import Client
import sys

# Import environment models
sys.path.append("code_refactor_gym")
from models import CodeRefactorGymAction, CodeRefactorGymObservation


def create_training_prompts():
    """Create diverse training prompts for code refactoring."""
    prompts = [
        "You are a senior software engineer specialized in code refactoring. Refactor the following legacy code to improve quality, add type hints, and follow best practices.\n\nLegacy code:",
        "As an expert Python developer, improve this code by adding type annotations, docstrings, and removing bad patterns.\n\nCode to refactor:",
        "Refactor this legacy Python code to be more maintainable, readable, and follow modern Python best practices.\n\nOriginal code:",
        "Transform this poorly written code into clean, well-documented Python with proper type hints and error handling.\n\nCode:",
        "Improve this code by: 1) Adding type hints, 2) Adding docstrings, 3) Removing globals, 4) Fixing magic numbers.\n\nLegacy code:",
    ]

    # Replicate prompts to create larger dataset
    return prompts * 16  # 80 training examples


def reward_from_env(completions, **kwargs):
    """
    Extract environment rewards from rollout function.

    The CodeRefactor Gym environment provides rewards based on:
    - Syntax validity (penalty -10 for errors)
    - Code quality improvements (+0 to +18 based on metrics)
    - Significant improvements bonus (+5 for score > 70)
    """
    env_rewards = kwargs.get("env_reward", [])
    return [float(reward) for reward in env_rewards] if env_rewards else [0.0] * len(completions)


def reward_syntax_bonus(completions, **kwargs):
    """Bonus reward for maintaining valid syntax."""
    syntax_valid = kwargs.get("syntax_valid", [])
    return [2.0 if valid else 0.0 for valid in syntax_valid] if syntax_valid else [0.0] * len(completions)


def reward_improvement_bonus(completions, **kwargs):
    """Bonus reward for achieving high improvement scores."""
    improvement_scores = kwargs.get("improvement_score", [])
    if not improvement_scores:
        return [0.0] * len(completions)

    return [
        5.0 if score > 80 else 3.0 if score > 60 else 1.0 if score > 40 else 0.0
        for score in improvement_scores
    ]


def rollout_func(prompts: list[str], trainer: GRPOTrainer, env_url: str):
    """
    Custom rollout function that:
    1. Generates code refactorings using the model
    2. Steps through CodeRefactor Gym environment
    3. Collects rewards and metrics
    """
    # Generate completions using TRL
    outputs = generate_rollout_completions(trainer, prompts)
    tokenizer = trainer.processing_class

    # Decode completions
    completions_text = [
        tokenizer.decode(out["completion_ids"], skip_special_tokens=True)
        for out in outputs
    ]

    # Connect to environment
    client = Client(base_url=env_url)

    # Collect environment rewards
    env_rewards = []
    syntax_valid_list = []
    improvement_scores = []

    for completion in completions_text:
        try:
            # Reset environment to get new legacy code
            obs = client.reset()
            legacy_code = obs.legacy_code

            # Extract refactored code from completion
            # The model should output the refactored code
            refactored_code = completion.strip()

            # Step through environment
            action = CodeRefactorGymAction(
                refactored_code=refactored_code,
                reasoning="AI refactoring"
            )
            result = client.step(action)

            # Collect metrics
            env_rewards.append(result.reward)
            syntax_valid_list.append(result.syntax_valid)
            improvement_scores.append(result.improvement_score)

        except Exception as e:
            print(f"Warning: Environment step failed: {e}")
            env_rewards.append(-5.0)  # Penalty for errors
            syntax_valid_list.append(False)
            improvement_scores.append(0.0)

    # Return outputs with environment metrics
    return {
        "prompt_ids": [out["prompt_ids"] for out in outputs],
        "completion_ids": [out["completion_ids"] for out in outputs],
        "logprobs": [out["logprobs"] for out in outputs],
        "env_reward": env_rewards,
        "syntax_valid": syntax_valid_list,
        "improvement_score": improvement_scores,
    }


def main():
    parser = argparse.ArgumentParser(description="Train CodeRefactor Gym agent with GRPO")

    # Model configuration
    parser.add_argument("--model-id", type=str, default="Qwen/Qwen2.5-1.5B-Instruct",
                        help="Base model to fine-tune")
    parser.add_argument("--use-unsloth", action="store_true",
                        help="Use Unsloth for 2x faster training")

    # Environment configuration
    parser.add_argument("--env-url", type=str,
                        default="https://mo35-code-refactor-gym.hf.space",
                        help="CodeRefactor Gym environment URL")

    # Training configuration
    parser.add_argument("--output-dir", type=str, default="./code-refactor-agent",
                        help="Output directory for trained model")
    parser.add_argument("--num-epochs", type=int, default=3,
                        help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=4,
                        help="Training batch size")
    parser.add_argument("--num-generations", type=int, default=8,
                        help="Number of generations per prompt")
    parser.add_argument("--max-length", type=int, default=1024,
                        help="Max completion length")
    parser.add_argument("--learning-rate", type=float, default=5e-6,
                        help="Learning rate")

    # vLLM configuration
    parser.add_argument("--use-vllm", action="store_true", default=True,
                        help="Use vLLM for faster inference")

    args = parser.parse_args()

    print("=" * 60)
    print("CodeRefactor Gym - GRPO Training")
    print("=" * 60)
    print(f"Model: {args.model_id}")
    print(f"Environment: {args.env_url}")
    print(f"Output: {args.output_dir}")
    print(f"Epochs: {args.num_epochs}")
    print(f"Batch size: {args.batch_size}")
    print(f"Use Unsloth: {args.use_unsloth}")
    print("=" * 60)

    # Load model and tokenizer
    if args.use_unsloth:
        try:
            from unsloth import FastLanguageModel
            print("Loading model with Unsloth optimization...")
            model, tokenizer = FastLanguageModel.from_pretrained(
                model_name=args.model_id,
                max_seq_length=args.max_length,
                dtype=None,  # Auto-detect
                load_in_4bit=True,  # 4-bit quantization
            )
            # Add LoRA adapters
            model = FastLanguageModel.get_peft_model(
                model,
                r=16,  # LoRA rank
                target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                                "gate_proj", "up_proj", "down_proj"],
                lora_alpha=16,
                lora_dropout=0,
                bias="none",
                use_gradient_checkpointing="unsloth",
                random_state=3407,
            )
        except ImportError:
            print("Warning: Unsloth not available, using standard loading")
            args.use_unsloth = False
            tokenizer = AutoTokenizer.from_pretrained(args.model_id)
            model = args.model_id
    else:
        tokenizer = AutoTokenizer.from_pretrained(args.model_id)
        model = args.model_id

    # Create dataset
    print("\nCreating training dataset...")
    prompts = create_training_prompts()
    dataset = Dataset.from_dict({"prompt": prompts})
    print(f"Dataset size: {len(dataset)} examples")

    # Configure GRPO training
    grpo_config = GRPOConfig(
        output_dir=args.output_dir,
        num_train_epochs=args.num_epochs,
        num_generations=args.num_generations,
        max_completion_length=args.max_length,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=2,
        learning_rate=args.learning_rate,
        use_vllm=args.use_vllm,
        vllm_mode="colocate" if args.use_vllm else None,
        logging_steps=10,
        save_steps=100,
        save_total_limit=3,
        push_to_hub=False,
    )

    # Initialize trainer
    print("\nInitializing GRPO trainer...")
    trainer = GRPOTrainer(
        model=model,
        processing_class=tokenizer,
        reward_funcs=[
            reward_from_env,          # Primary reward from environment
            reward_syntax_bonus,       # Bonus for valid syntax
            reward_improvement_bonus,  # Bonus for high improvement
        ],
        train_dataset=dataset,
        args=grpo_config,
        rollout_func=lambda prompts, trainer: rollout_func(
            prompts, trainer, args.env_url
        ),
    )

    # Train
    print("\n" + "=" * 60)
    print("Starting training...")
    print("=" * 60 + "\n")

    trainer.train()

    print("\n" + "=" * 60)
    print("Training complete!")
    print(f"Model saved to: {args.output_dir}")
    print("=" * 60)

    # Save final model
    if args.use_unsloth:
        model.save_pretrained(args.output_dir)
        tokenizer.save_pretrained(args.output_dir)


if __name__ == "__main__":
    main()
