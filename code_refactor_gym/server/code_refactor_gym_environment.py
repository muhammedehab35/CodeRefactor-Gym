# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Code Refactor Gym Environment Implementation.

An environment that teaches agents to refactor legacy code into modern,
maintainable code with improved quality metrics.
"""

import ast
import random
from typing import Dict, Any
from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from models import CodeRefactorGymAction, CodeRefactorGymObservation


# Legacy code samples for refactoring
LEGACY_CODE_SAMPLES = [
    # Sample 1: Poor naming, no type hints, complex logic
    """
def f(x, y):
    result = []
    for i in range(len(x)):
        if x[i] > y:
            result.append(x[i])
    return result
""",
    # Sample 2: Global variables, poor structure
    """
total = 0
def add(x):
    global total
    total = total + x
    return total
""",
    # Sample 3: Nested conditions, poor readability
    """
def check(data):
    if data != None:
        if len(data) > 0:
            if type(data) == list:
                return True
    return False
""",
    # Sample 4: No error handling, magic numbers
    """
def process(items):
    result = []
    for i in items:
        if i % 2 == 0:
            result.append(i * 3.14159)
    return result
""",
    # Sample 5: Repetitive code, no abstraction
    """
def calc1(x):
    return x * 2 + 10

def calc2(x):
    return x * 3 + 10

def calc3(x):
    return x * 4 + 10
""",
]


class CodeRefactorGymEnvironment(Environment):
    """
    Environment for learning code refactoring.

    The agent receives legacy code and must refactor it to improve:
    - Code readability (naming, structure)
    - Type safety (type hints)
    - Best practices (avoiding globals, proper error handling)
    - Code metrics (complexity, maintainability)

    Rewards are based on improvement in code quality metrics and syntax validity.
    """

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        """Initialize the code_refactor_gym environment."""
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._current_legacy_code = ""
        self._baseline_metrics = {}

    def reset(self) -> CodeRefactorGymObservation:
        """
        Reset the environment with a new legacy code sample.

        Returns:
            CodeRefactorGymObservation with the legacy code to refactor
        """
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._current_legacy_code = random.choice(LEGACY_CODE_SAMPLES)
        self._baseline_metrics = self._calculate_metrics(self._current_legacy_code)

        return CodeRefactorGymObservation(
            legacy_code=self._current_legacy_code,
            test_results={},
            quality_metrics=self._baseline_metrics,
            syntax_valid=True,
            error_message="",
            improvement_score=0.0,
            done=False,
            reward=0.0,
        )

    def step(self, action: CodeRefactorGymAction) -> CodeRefactorGymObservation:  # type: ignore[override]
        """
        Evaluate the refactored code.

        Args:
            action: CodeRefactorGymAction containing the refactored code

        Returns:
            CodeRefactorGymObservation with evaluation results
        """
        self._state.step_count += 1
        refactored_code = action.refactored_code

        # Check syntax validity
        syntax_valid, error_message = self._check_syntax(refactored_code)

        if not syntax_valid:
            return CodeRefactorGymObservation(
                legacy_code=self._current_legacy_code,
                test_results={"syntax_check": "failed"},
                quality_metrics={},
                syntax_valid=False,
                error_message=error_message,
                improvement_score=0.0,
                done=False,
                reward=-10.0,  # Penalty for syntax errors
                metadata={"step": self._state.step_count, "reasoning": action.reasoning},
            )

        # Calculate quality metrics
        new_metrics = self._calculate_metrics(refactored_code)
        improvement_score = self._calculate_improvement(self._baseline_metrics, new_metrics)

        # Calculate reward based on improvement
        reward = improvement_score / 10.0  # Scale to reasonable range

        # Bonus for significant improvements
        if improvement_score > 70:
            reward += 5.0

        # Episode ends after one refactoring attempt
        done = True

        return CodeRefactorGymObservation(
            legacy_code=self._current_legacy_code,
            test_results={"syntax_check": "passed", "metrics_improved": improvement_score > 0},
            quality_metrics=new_metrics,
            syntax_valid=True,
            error_message="",
            improvement_score=improvement_score,
            done=done,
            reward=reward,
            metadata={
                "step": self._state.step_count,
                "reasoning": action.reasoning,
                "baseline_metrics": self._baseline_metrics,
                "improvement_details": {
                    "lines_change": new_metrics.get("lines", 0) - self._baseline_metrics.get("lines", 0),
                    "complexity_change": new_metrics.get("complexity", 0) - self._baseline_metrics.get("complexity", 0),
                },
            },
        )

    def _check_syntax(self, code: str) -> tuple[bool, str]:
        """Check if the code has valid Python syntax."""
        try:
            ast.parse(code)
            return True, ""
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, f"Parse error: {str(e)}"

    def _calculate_metrics(self, code: str) -> Dict[str, Any]:
        """
        Calculate code quality metrics.

        Metrics include:
        - lines: Number of non-empty lines
        - complexity: Cyclomatic complexity estimate
        - has_type_hints: Whether type hints are present
        - has_docstring: Whether docstring is present
        - avg_line_length: Average line length
        """
        lines = [line for line in code.strip().split('\n') if line.strip()]
        num_lines = len(lines)

        # Simple complexity estimate: count control flow statements
        complexity = code.count('if ') + code.count('for ') + code.count('while ') + code.count('except')

        # Check for type hints
        has_type_hints = '->' in code or ': ' in code

        # Check for docstring
        has_docstring = '"""' in code or "'''" in code

        # Average line length
        avg_line_length = sum(len(line) for line in lines) / max(num_lines, 1)

        # Check for bad patterns
        has_globals = 'global ' in code
        has_magic_numbers = any(c.isdigit() for c in code if c not in ['0', '1'])

        return {
            "lines": num_lines,
            "complexity": complexity,
            "has_type_hints": has_type_hints,
            "has_docstring": has_docstring,
            "avg_line_length": avg_line_length,
            "has_globals": has_globals,
            "has_magic_numbers": has_magic_numbers,
        }

    def _calculate_improvement(self, baseline: Dict[str, Any], new: Dict[str, Any]) -> float:
        """
        Calculate improvement score (0-100) based on metric changes.

        Higher score = better refactoring.
        """
        score = 50.0  # Start at neutral

        # Penalize if code gets longer (should be more concise)
        if new.get("lines", 0) > baseline.get("lines", 0):
            score -= 5
        elif new.get("lines", 0) < baseline.get("lines", 0):
            score += 5

        # Penalize increased complexity
        if new.get("complexity", 0) > baseline.get("complexity", 0):
            score -= 10
        elif new.get("complexity", 0) < baseline.get("complexity", 0):
            score += 10

        # Reward adding type hints
        if new.get("has_type_hints") and not baseline.get("has_type_hints"):
            score += 15

        # Reward adding docstrings
        if new.get("has_docstring") and not baseline.get("has_docstring"):
            score += 10

        # Reward removing globals
        if baseline.get("has_globals") and not new.get("has_globals"):
            score += 15

        # Reward fixing magic numbers
        if baseline.get("has_magic_numbers") and not new.get("has_magic_numbers"):
            score += 10

        # Ensure score is in valid range
        return max(0.0, min(100.0, score))

    @property
    def state(self) -> State:
        """Get the current environment state."""
        return self._state
