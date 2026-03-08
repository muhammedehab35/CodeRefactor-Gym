@echo off
REM Script pour pousser le code vers GitHub

echo ========================================
echo Push CodeRefactor Gym vers GitHub
echo ========================================

cd "D:\Northflank + openv"

echo.
echo [1/6] Initialisation Git...
git init

echo.
echo [2/6] Ajout de tous les fichiers...
git add .

echo.
echo [3/6] Commit...
git commit -m "Complete OpenEnv Hackathon setup: Environment + Training pipeline - CodeRefactor Gym environment (5 legacy code types) - TRL/GRPO training script with Unsloth support - Northflank H100 deployment configuration - Complete documentation and guides - Environment deployed at: https://mo35-code-refactor-gym.hf.space"

echo.
echo [4/6] Configuration remote GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/muhammedehab35/CodeRefactor-Gym.git

echo.
echo [5/6] Set branch to main...
git branch -M main

echo.
echo [6/6] Push vers GitHub...
git push -u origin main --force

echo.
echo ========================================
echo TERMINÉ! Code poussé vers:
echo https://github.com/muhammedehab35/CodeRefactor-Gym
echo ========================================
echo.
pause
