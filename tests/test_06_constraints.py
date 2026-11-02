"""Tests for Component 6: Constraints (Decision Steps & Anti-Loop Budgets)."""
from __future__ import annotations

import unittest
from src.harness.constraints import ConstraintManager, ConstraintExceededError


class TestConstraints(unittest.TestCase):
    def test_normal_execution_within_step_budget(self):
        """Allows execution when within the configured 3-step budget."""
        manager = ConstraintManager(max_steps=3)
        self.assertEqual(manager.record_step("step_1"), 1)
        self.assertEqual(manager.record_step("step_2"), 2)
        self.assertEqual(manager.record_step("step_3"), 3)

    def test_triggers_anti_loop_halt_on_exceeded_steps(self):
        """Halts the agent immediately if it loops past max_steps."""
        manager = ConstraintManager(max_steps=3)
        manager.record_step("step_1")
        manager.record_step("step_2")
        manager.record_step("step_3")

        with self.assertRaises(ConstraintExceededError) as ctx:
            manager.record_step("step_4_runaway_loop")

        self.assertIn("exceeded maximum allowed decision steps (4/3)", str(ctx.exception))

    def test_token_budget_constraint(self):
        """Halts the agent if token expenditure exceeds safety limits."""
        manager = ConstraintManager(max_tokens=1000)
        manager.record_tokens(500)
        with self.assertRaises(ConstraintExceededError) as ctx:
            manager.record_tokens(600)  # Total 1100 > 1000
        self.assertIn("token budget exceeded (1100/1000)", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

