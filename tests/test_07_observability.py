"""Tests for Component 7: Observability (Telemetry & Prompt Cache Economics)."""
from __future__ import annotations

import time
import unittest
from src.harness.observability import HarnessTelemetry


class TestObservability(unittest.TestCase):
    def setUp(self):
        self.telemetry = HarnessTelemetry()

    def test_record_execution_telemetry_with_prompt_caching(self):
        """Measures execution duration, cache hit rate, and financial savings."""
        start_time = time.time() - 0.25  # 250ms duration simulation

        # In this ticket: 2000 prompt tokens, with 1600 tokens coming from cached policy
        t = self.telemetry.record_execution(
            ticket_id="TICK-OBS-01",
            start_time=start_time,
            prompt_tokens=2000,
            output_tokens=150,
            cached_content_tokens=1600,
            policy_gate_triggered=False,
            status="SUCCESS",
        )

        self.assertEqual(t.ticket_id, "TICK-OBS-01")
        self.assertGreaterEqual(t.duration_ms, 200.0)
        self.assertEqual(t.cache_hit_rate, 80.0)  # 1600 / 2000 = 80%
        self.assertEqual(t.total_tokens, 2150)
        # Cost savings must be positive due to prompt caching discount
        self.assertGreater(t.estimated_savings_usd, 0.0)
        self.assertLess(t.estimated_cost_usd, (2000 * HarnessTelemetry.PRICE_INPUT_UNCACHED + 150 * HarnessTelemetry.PRICE_OUTPUT))

    def test_telemetry_history_aggregation(self):
        """Verifies that multiple ticket executions are logged in history."""
        self.telemetry.record_execution(
            ticket_id="T1", start_time=time.time(), prompt_tokens=1000,
            output_tokens=50, cached_content_tokens=800,
        )
        self.telemetry.record_execution(
            ticket_id="T2", start_time=time.time(), prompt_tokens=1000,
            output_tokens=50, cached_content_tokens=800,
        )
        self.assertEqual(len(self.telemetry.history), 2)


if __name__ == "__main__":
    unittest.main()

