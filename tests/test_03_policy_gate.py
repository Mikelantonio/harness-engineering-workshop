"""Tests for Component 3: Policy Gate (Human-In-The-Loop Guardrails)."""
from __future__ import annotations

import unittest
from src.harness.policy_gate import PolicyGate, PolicyGateDecision


class TestPolicyGate(unittest.TestCase):
    def setUp(self):
        self.gate = PolicyGate(refund_threshold=500.0, fraud_risk_threshold=70)

    def test_standard_refund_passes_autonomous_gate(self):
        """A €180 refund with low fraud risk is approved autonomously."""
        res = self.gate.evaluate(
            ticket_id="TICK-101",
            refund_amount=180.0,
            fraud_risk_score=15,
            customer_id="CUST-GOOD-01",
        )
        self.assertEqual(res.decision, PolicyGateDecision.APPROVED)
        self.assertFalse(res.is_blocked)
        self.assertFalse(res.requires_human_approval)
        self.assertIsNone(res.supervisor_ticket_id)

    def test_high_value_refund_escalates_to_human_supervisor(self):
        """A €650 refund exceeds €500 threshold and triggers HITL review."""
        res = self.gate.evaluate(
            ticket_id="TICK-202",
            refund_amount=650.0,
            fraud_risk_score=20,
            customer_id="CUST-LUX-02",
        )
        self.assertEqual(res.decision, PolicyGateDecision.ESCALATED_TO_HITL)
        self.assertTrue(res.is_blocked)
        self.assertTrue(res.requires_human_approval)
        self.assertIsNotNone(res.supervisor_ticket_id)
        self.assertTrue(res.supervisor_ticket_id.startswith("HITL-VAL-"))
        self.assertIn("exceeds the autonomous threshold of €500.00", res.reason)

    def test_fraud_risk_triggers_security_block(self):
        """A suspicious customer (score 85 > 70) is blocked regardless of amount."""
        res = self.gate.evaluate(
            ticket_id="TICK-303",
            refund_amount=75.0,  # low amount, but high risk
            fraud_risk_score=85,
            customer_id="CUST-SUSPECT-77",
        )
        self.assertEqual(res.decision, PolicyGateDecision.BLOCKED_FRAUD)
        self.assertTrue(res.is_blocked)
        self.assertTrue(res.requires_human_approval)
        self.assertIsNotNone(res.supervisor_ticket_id)
        self.assertTrue(res.supervisor_ticket_id.startswith("HITL-FRD-"))
        self.assertIn("Fraud Risk Score of 85/100", res.reason)


if __name__ == "__main__":
    unittest.main()

