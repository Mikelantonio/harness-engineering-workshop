"""Component 7: Observability (Telemetry, Token Economics & Prompt Cache Tracking)."""
from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger("harness.observability")


@dataclass
class ExecutionTelemetry:
    ticket_id: str
    duration_ms: float
    prompt_tokens: int
    output_tokens: int
    cached_content_tokens: int
    total_tokens: int
    cache_hit_rate: float
    estimated_cost_usd: float
    estimated_savings_usd: float
    policy_gate_triggered: bool
    status: str


class HarnessTelemetry:
    """
    Tracks runtime telemetry, prompt caching metrics, and computational economics.
    Demonstrates the concrete financial benefits of harness engineering (Stable Zone caching).
    """

    # Gemini 2.5 Flash typical pricing reference (USD per million tokens)
    PRICE_INPUT_UNCACHED = 0.075 / 1_000_000
    PRICE_INPUT_CACHED = 0.01875 / 1_000_000  # ~75% discount
    PRICE_OUTPUT = 0.30 / 1_000_000

    def __init__(self):
        self.history: List[ExecutionTelemetry] = []

    def record_execution(
        self,
        ticket_id: str,
        start_time: float,
        prompt_tokens: int,
        output_tokens: int,
        cached_content_tokens: int,
        policy_gate_triggered: bool = False,
        status: str = "SUCCESS",
    ) -> ExecutionTelemetry:
        """
        Calculates and logs execution telemetry and cache savings.
        """
        duration_ms = round((time.time() - start_time) * 1000, 2)
        uncached_prompt_tokens = max(0, prompt_tokens - cached_content_tokens)
        total_tokens = prompt_tokens + output_tokens

        cache_hit_rate = (
            round((cached_content_tokens / prompt_tokens) * 100, 2)
            if prompt_tokens > 0
            else 0.0
        )

        # Actual cost vs theoretical uncached cost
        actual_cost = (
            (cached_content_tokens * self.PRICE_INPUT_CACHED)
            + (uncached_prompt_tokens * self.PRICE_INPUT_UNCACHED)
            + (output_tokens * self.PRICE_OUTPUT)
        )
        uncached_cost = (
            (prompt_tokens * self.PRICE_INPUT_UNCACHED)
            + (output_tokens * self.PRICE_OUTPUT)
        )
        estimated_savings = max(0.0, uncached_cost - actual_cost)

        telemetry = ExecutionTelemetry(
            ticket_id=ticket_id,
            duration_ms=duration_ms,
            prompt_tokens=prompt_tokens,
            output_tokens=output_tokens,
            cached_content_tokens=cached_content_tokens,
            total_tokens=total_tokens,
            cache_hit_rate=cache_hit_rate,
            estimated_cost_usd=round(actual_cost, 6),
            estimated_savings_usd=round(estimated_savings, 6),
            policy_gate_triggered=policy_gate_triggered,
            status=status,
        )

        self.history.append(telemetry)
        logger.info(
            "TELEMETRY: %s",
            json.dumps(asdict(telemetry)),
        )
        return telemetry

