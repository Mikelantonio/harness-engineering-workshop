"""Tests for Component 5: Verify (Output Schema & Business Invariants)."""
from __future__ import annotations

import unittest
from src.harness.verifier import ReturnAuthorizationVerifier, VerificationError


class TestVerifier(unittest.TestCase):
    def setUp(self):
        self.verifier = ReturnAuthorizationVerifier()

    def test_valid_authorization_payload(self):
        """A properly formed JSON payload passes verification."""
        valid_payload = {
            "ticket_id": "TICK-IT-101",
            "action": "REFUND",
            "approved_amount": 153.0,
            "warehouse_code": "WMS-MIL-01",
            "reason": "Approved seam repair depreciation.",
            "customs_declaration_required": False,
        }
        auth = self.verifier.verify(valid_payload, origin_country="IT")
        self.assertEqual(auth.ticket_id, "TICK-IT-101")
        self.assertEqual(auth.action, "REFUND")
        self.assertEqual(auth.approved_amount, 153.0)
        self.assertEqual(auth.warehouse_code, "WMS-MIL-01")

    def test_rejects_hallucinated_warehouse_code(self):
        """Catches and rejects non-existent warehouse codes like 'WMS-ROMA-99'."""
        invalid_payload = {
            "ticket_id": "TICK-FAIL-01",
            "action": "REFUND",
            "approved_amount": 100.0,
            "warehouse_code": "WMS-ROMA-99",  # Hallucinated!
            "reason": "Test",
        }
        with self.assertRaises(VerificationError) as ctx:
            self.verifier.verify(invalid_payload)
        self.assertIn("Unauthorized or unknown warehouse_code 'WMS-ROMA-99'", str(ctx.exception))

    def test_enforces_uk_customs_and_dedicated_hub(self):
        """UK returns must route exclusively to WMS-LON-03 with customs declaration."""
        # Case A: UK return routed incorrectly to Milano
        uk_wrong_hub = {
            "ticket_id": "TICK-UK-01",
            "action": "REFUND",
            "approved_amount": 120.0,
            "warehouse_code": "WMS-MIL-01",
            "customs_declaration_required": True,
        }
        with self.assertRaises(VerificationError) as ctx:
            self.verifier.verify(uk_wrong_hub, origin_country="UK")
        self.assertIn("UK returns must be routed exclusively to 'WMS-LON-03'", str(ctx.exception))

        # Case B: UK return to London hub but missing customs declaration
        uk_missing_customs = {
            "ticket_id": "TICK-UK-02",
            "action": "REFUND",
            "approved_amount": 120.0,
            "warehouse_code": "WMS-LON-03",
            "customs_declaration_required": False,
        }
        with self.assertRaises(VerificationError) as ctx:
            self.verifier.verify(uk_missing_customs, origin_country="UK")
        self.assertIn("require 'customs_declaration_required=True'", str(ctx.exception))

    def test_rejects_negative_or_corrupted_amount(self):
        """Catches negative amounts or invalid action verbs."""
        bad_amount = {
            "ticket_id": "TICK-03",
            "action": "REFUND",
            "approved_amount": -50.0,
            "warehouse_code": "WMS-MIL-01",
        }
        with self.assertRaises(VerificationError):
            self.verifier.verify(bad_amount)


if __name__ == "__main__":
    unittest.main()

