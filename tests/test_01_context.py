"""Tests for Component 1: Context Builder (Stable Zone vs Volatile Zone)."""
from __future__ import annotations

import unittest
from src.harness.context import ContextBuilder, CustomerTicket


class TestContextBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = ContextBuilder()

    def test_stable_zone_contains_international_customs_policy(self):
        """Validates that the policy includes Schengen, UK, and customs regulations."""
        policy = self.builder.get_stable_policy()
        self.assertIn("WMS-MIL-01", policy)
        self.assertIn("WMS-LON-03", policy)
        self.assertIn("CN22/CN23", policy)
        self.assertIn("Schengen", policy)

    def test_stable_zone_is_exact_prefix_for_prompt_caching(self):
        """
        Validates that two different tickets share the exact same policy prefix,
        allowing the LLM provider (Gemini) to reuse cached tokens.
        """
        ticket1 = CustomerTicket(
            ticket_id="T1", customer_id="C1", country="IT", item_category="shoes",
            item_description="Sneakers", purchase_price=100.0, days_since_delivery=5,
            complaint_text="Too small"
        )
        ticket2 = CustomerTicket(
            ticket_id="T2", customer_id="C2", country="FR", item_category="denim",
            item_description="Jeans", purchase_price=80.0, days_since_delivery=10,
            complaint_text="Zipper stuck"
        )

        prompt1 = self.builder.build_prompt(ticket1)
        prompt2 = self.builder.build_prompt(ticket2)

        # The stable section must be identical
        stable_marker = "=== STABLE CONTEXT: GLOBAL RETURN POLICIES & CUSTOMS EXCEPTIONS ==="
        self.assertTrue(prompt1.startswith(stable_marker))
        self.assertTrue(prompt2.startswith(stable_marker))

        policy_text = self.builder.get_stable_policy()
        self.assertIn(policy_text, prompt1)
        self.assertIn(policy_text, prompt2)

    def test_volatile_context_correctly_embeds_ticket_metadata(self):
        """Validates that ticket details are formatted into the volatile payload."""
        ticket = CustomerTicket(
            ticket_id="TICK-TEST-99",
            customer_id="CUST-1234",
            country="IT",
            item_category="leather",
            item_description="Borsa a tracolla",
            purchase_price=250.0,
            days_since_delivery=8,
            complaint_text="Tracolla difettosa.",
            has_original_tags=True,
            fraud_risk_score=12,
        )
        volatile = self.builder.build_volatile_context(ticket)
        self.assertIn("TICK-TEST-99", volatile)
        self.assertIn("CUST-1234", volatile)
        self.assertIn("€250.00", volatile)
        self.assertIn("Tracolla difettosa.", volatile)

    def test_system_instruction_provides_agent_role(self):
        """Validates that ContextBuilder defines the formal system instruction for the agent."""
        sys_inst = self.builder.build_system_instruction()
        self.assertIn("logistica inversa fashion", sys_inst)
        self.assertIn("calculate_depreciated_refund", sys_inst)
        self.assertIn("generate_wms_return_label", sys_inst)


if __name__ == "__main__":
    unittest.main()

