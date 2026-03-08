"""Quick test of the CodeRefactor Gym environment."""
import asyncio
from server.code_refactor_gym_environment import CodeRefactorGymEnvironment
from models import CodeRefactorGymAction


async def test_environment():
    """Test the environment locally."""
    env = CodeRefactorGymEnvironment()

    # Reset the environment
    print("=" * 60)
    print("RESET")
    print("=" * 60)
    obs = env.reset()
    print(f"Legacy Code:\n{obs.legacy_code}")
    print(f"\nBaseline Metrics: {obs.quality_metrics}")
    print(f"Reward: {obs.reward}")

    # Test with a good refactoring
    print("\n" + "=" * 60)
    print("STEP 1: Good Refactoring")
    print("=" * 60)

    refactored_code = """
from typing import List

def filter_values_above_threshold(values: List[float], threshold: float) -> List[float]:
    \"\"\"
    Filter values that exceed the given threshold.

    Args:
        values: List of numeric values to filter
        threshold: Minimum value threshold

    Returns:
        List of values greater than threshold
    \"\"\"
    return [value for value in values if value > threshold]
"""

    action = CodeRefactorGymAction(
        refactored_code=refactored_code,
        reasoning="Added type hints, docstring, descriptive names, and used list comprehension"
    )

    obs = env.step(action)
    print(f"Syntax Valid: {obs.syntax_valid}")
    print(f"Test Results: {obs.test_results}")
    print(f"New Metrics: {obs.quality_metrics}")
    print(f"Improvement Score: {obs.improvement_score}")
    print(f"Reward: {obs.reward}")
    print(f"Done: {obs.done}")

    # Test with syntax error
    print("\n" + "=" * 60)
    print("STEP 2: Syntax Error (New Episode)")
    print("=" * 60)

    env.reset()
    bad_code = "def bad syntax here"
    action = CodeRefactorGymAction(
        refactored_code=bad_code,
        reasoning="Testing error handling"
    )

    obs = env.step(action)
    print(f"Syntax Valid: {obs.syntax_valid}")
    print(f"Error Message: {obs.error_message}")
    print(f"Reward: {obs.reward}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_environment())
