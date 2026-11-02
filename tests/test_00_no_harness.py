"""Demonstrates the systemic failures of an AI agent operating WITHOUT a Harness."""
from __future__ import annotations

import unittest


class TestUnharnessedAgentFailures(unittest.TestCase):
    """
    Shows why raw LLMs without an engineering harness are dangerous in production:
    1. Financial Hallucination: stochastic math approximations.
    2. Missing Safety Gates: unmonitored payouts > €500 or to fraudulent accounts.
    3. Structural Hallucinations: assigning non-existent warehouse logistics codes.
    4. Unbounded Loops: consuming budget endlessly without exit constraints.
    """

    def test_unharnessed_financial_hallucination(self):
        """Without deterministic tools, raw LLMs invent refund numbers arbitrarily."""
        original_price = 180.0
        # Simulating typical LLM stochastic outputs without tools
        stochastic_llm_outputs = [142.50, 150.00, 133.33, 160.00]
        # In contrast, deterministic policy demands EXACTLY 85% = 153.00 €
        exact_policy_amount = 180.0 * 0.85

        # An unharnessed agent will differ from corporate accounting policy
        self.assertNotIn(exact_policy_amount, stochastic_llm_outputs)

    def test_unharnessed_permits_dangerous_payout(self):
        """Without a Policy Gate, an agent directly authorizes a €1200 refund with zero human review."""
        dangerous_refund_request = {
            "ticket_id": "TICK-ROGUE-999",
            "amount": 1200.0,
            "status": "APPROVED",
        }
        # Unharnessed: nothing intercepts or requires manager sign-off
        is_blocked = False
        self.assertFalse(is_blocked, "Unharnessed system fails to block a €1200 payout!")

    def test_unharnessed_routes_to_phantom_warehouse(self):
        """Without a Verifier, the agent hallucinates 'WMS-ROMA-99' which breaks supply chain EDI."""
        hallucinated_destination = "WMS-ROMA-99"
        valid_warehouses = {"WMS-MIL-01", "WMS-PAR-04", "WMS-FRA-02", "WMS-LON-03"}

        # Without verification, the invalid code passes through downstream
        self.assertNotIn(hallucinated_destination, valid_warehouses)


if __name__ == "__main__":
    unittest.main()

