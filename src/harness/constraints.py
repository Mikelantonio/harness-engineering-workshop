"""Component 6: Constraints (Decision Step Budgets & Anti-Loop Guardrails)."""
from __future__ import annotations


class ConstraintExceededError(Exception):
    """Raised when an agent execution exceeds safety budgets or resource constraints."""
    pass


class ConstraintManager:
    """
    Enforces operational boundaries and prevents runaway agent loops.
    Limits maximum decision steps, tool calls, or retry attempts.
    """

    def __init__(self, max_steps: int = 3, max_tokens: int = 4096):
        self.max_steps = max_steps
        self.max_tokens = max_tokens
        self.current_step = 0
        self.total_tokens_consumed = 0

    def record_step(self, step_name: str = "decision_step") -> int:
        """
        Increments and checks the execution step counter.

        Raises:
            ConstraintExceededError: If the maximum allowed steps are exceeded.
        """
        self.current_step += 1
        if self.current_step > self.max_steps:
            raise ConstraintExceededError(
                f"Agent halted by constraint: exceeded maximum allowed decision steps "
                f"({self.current_step}/{self.max_steps}). Anti-loop triggered."
            )
        return self.current_step

    def record_tokens(self, tokens: int) -> int:
        """Tracks token expenditure and protects against token blowouts."""
        self.total_tokens_consumed += tokens
        if self.total_tokens_consumed > self.max_tokens:
            raise ConstraintExceededError(
                f"Agent halted: token budget exceeded ({self.total_tokens_consumed}/{self.max_tokens})."
            )
        return self.total_tokens_consumed

    def reset(self) -> None:
        """Resets counters for a new ticket execution."""
        self.current_step = 0
        self.total_tokens_consumed = 0

