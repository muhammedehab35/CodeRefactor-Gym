#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Deploy script with proper encoding handling for Windows."""
import sys
import os
import subprocess

# Set UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Change to the correct directory
os.chdir(r"D:\Northflank + openv\code_refactor_gym")

# Run openenv push
try:
    result = subprocess.run(
        ['openenv', 'push'],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
