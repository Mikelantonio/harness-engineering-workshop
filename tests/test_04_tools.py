"""Tests for Component 4: Tools / Runtime (Deterministic Business Logic)."""
from __future__ import annotations

import unittest
from src.harness.tools import calculate_depreciated_refund, generate_wms_return_label
from src.harness.agent import root_agent


class TestToolsRuntime(unittest.TestCase):
    def test_tools_registered_in_adk_agent(self):
        """Verifies that deterministic tools are registered with the ADK agent."""
        tool_names = [t.__name__ for t in root_agent.tools]
        self.assertIn("calculate_depreciated_refund", tool_names)
        self.assertIn("generate_wms_return_label", tool_names)
    def test_factory_defect_full_refund(self):
        """Factory defects with tags within 30 days receive 100% refund."""
        res = calculate_depreciated_refund(
            original_price=200.0,
            condition="intact_defect_origin",
            has_original_tags=True,
            days_since_delivery=10,
        )
        self.assertEqual(res["status"], "APPROVED")
        self.assertEqual(res["approved_refund"], 200.0)
        self.assertEqual(res["penalty_percentage"], 0.0)

    def test_repairable_seam_tear_depreciation(self):
        """Repairable seam tears incur a deterministic 15% depreciation (85% refund)."""
        res = calculate_depreciated_refund(
            original_price=100.0,
            condition="seam_tear_repairable",
            has_original_tags=True,
            days_since_delivery=14,
        )
        self.assertEqual(res["status"], "APPROVED")
        self.assertEqual(res["approved_refund"], 85.0)
        self.assertEqual(res["penalty_percentage"], 15.0)

    def test_late_return_additional_penalty(self):
        """Returns between 31 and 45 days incur an additional 20% penalty."""
        res = calculate_depreciated_refund(
            original_price=100.0,
            condition="seam_tear_repairable",  # 15% + 20% = 35% total penalty
            has_original_tags=True,
            days_since_delivery=35,
        )
        self.assertEqual(res["approved_refund"], 65.0)
        self.assertEqual(res["penalty_percentage"], 35.0)

    def test_return_outside_window_rejected(self):
        """Returns past 45 days are rejected with zero refund."""
        res = calculate_depreciated_refund(
            original_price=150.0,
            condition="intact_defect_origin",
            has_original_tags=True,
            days_since_delivery=48,
        )
        self.assertEqual(res["status"], "REJECTED")
        self.assertEqual(res["approved_refund"], 0.0)

    def test_missing_tags_rejected(self):
        """Hygiene seal / tags missing leads to rejection."""
        res = calculate_depreciated_refund(
            original_price=100.0,
            condition="intact_defect_origin",
            has_original_tags=False,
            days_since_delivery=5,
        )
        self.assertEqual(res["status"], "REJECTED")
        self.assertEqual(res["approved_refund"], 0.0)

    def test_wms_return_label_generation(self):
        """Generates tracking code and return label URL for authorized warehouse."""
        label = generate_wms_return_label(
            order_id="ORD-9912",
            warehouse_code="WMS-MIL-01",
            carrier="DHL_EXPRESS",
        )
        self.assertEqual(label["status"], "LABEL_GENERATED")
        self.assertEqual(label["destination_warehouse"], "WMS-MIL-01")
        self.assertTrue(label["tracking_number"].startswith("RTN-DHL-"))
        self.assertTrue(label["label_url"].endswith(".pdf"))


if __name__ == "__main__":
    unittest.main()

