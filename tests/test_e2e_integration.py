"""End-to-End Integration Test for the complete 7-Component Harness."""
from __future__ import annotations

import unittest
from src.harness.agent import ReverseLogisticsHarness
from src.harness.context import CustomerTicket
from src.harness.policy_gate import PolicyGateDecision


class TestEndToEndHarnessIntegration(unittest.TestCase):
    def setUp(self):
        self.harness = ReverseLogisticsHarness()

    def test_standard_ticket_full_pipeline_success(self):
        """Tests standard compliant return: Context -> Tool -> PolicyGate -> Verifier -> Observability."""
        ticket = CustomerTicket(
            ticket_id="TICK-E2E-01",
            customer_id="CUST-100",
            country="IT",
            item_category="leather",
            item_description="Giacca in pelle con strappo cucitura",
            purchase_price=200.0,
            days_since_delivery=10,
            complaint_text="Cucitura strappata sulla tasca.",
            has_original_tags=True,
            fraud_risk_score=10,
        )

        res = self.harness.execute_ticket(ticket)

        # 1. Verification of output
        auth = res["authorization"]
        self.assertEqual(auth.ticket_id, "TICK-E2E-01")
        self.assertEqual(auth.action, "REFUND")
        # 15% depreciation on 200 € = 170 €
        self.assertEqual(auth.approved_amount, 170.0)
        self.assertEqual(auth.warehouse_code, "WMS-MIL-01")

        # 2. Policy Gate status
        gate = res["gate_result"]
        self.assertEqual(gate.decision, PolicyGateDecision.APPROVED)
        self.assertFalse(gate.is_blocked)

        # 3. Telemetry status
        tel = res["telemetry"]
        self.assertEqual(tel.ticket_id, "TICK-E2E-01")
        self.assertGreater(tel.cached_content_tokens, 0)
        self.assertEqual(tel.status, "COMPLETED")

    def test_high_value_ticket_full_pipeline_hitl_escalation(self):
        """Tests luxury return > €500: passes through harness and safely halts for human supervisor."""
        ticket = CustomerTicket(
            ticket_id="TICK-E2E-LUX",
            customer_id="CUST-LUX-55",
            country="FR",
            item_category="luxury",
            item_description="Pelliccia ecologica sartoriale",
            purchase_price=800.0,
            days_since_delivery=5,
            complaint_text="Cucitura manica strappata.",
            has_original_tags=True,
            fraud_risk_score=15,
        )

        res = self.harness.execute_ticket(ticket)

        # Approved amount is 85% of 800 € = 680 € (> 500 € threshold)
        self.assertEqual(res["authorization"].approved_amount, 680.0)
        self.assertEqual(res["authorization"].action, "HITL_ESCALATION")

        # Policy Gate must have escalated
        gate = res["gate_result"]
        self.assertEqual(gate.decision, PolicyGateDecision.ESCALATED_TO_HITL)
        self.assertTrue(gate.is_blocked)
        self.assertTrue(gate.supervisor_ticket_id.startswith("HITL-VAL-"))
        self.assertEqual(res["telemetry"].status, "HITL_ESCALATED")


if __name__ == "__main__":
    unittest.main()

