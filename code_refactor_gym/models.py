# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Data models for the Code Refactor Gym Environment.

The code_refactor_gym environment teaches agents to refactor legacy code into modern,
maintainable code with improved quality metrics.
"""

from pydantic import Field

from openenv.core.env_server.types import Action, Observation


class CodeRefactorGymAction(Action):
    """Action for the Code Refactor Gym environment - refactored code submission."""

    refactored_code: str = Field(..., description="The refactored version of the legacy code")
    reasoning: str = Field(default="", description="Explanation of refactoring changes made")


class CodeRefactorGymObservation(Observation):
    """Observation from the Code Refactor Gym environment - feedback on refactoring."""

    legacy_code: str = Field(default="", description="The original legacy code to refactor")
    test_results: dict = Field(default_factory=dict, description="Test execution results")
    quality_metrics: dict = Field(default_factory=dict, description="Code quality metrics")
    syntax_valid: bool = Field(default=True, description="Whether the refactored code has valid syntax")
    error_message: str = Field(default="", description="Error message if syntax is invalid")
    improvement_score: float = Field(default=0.0, description="Overall improvement score (0-100)")
