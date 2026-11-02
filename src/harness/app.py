"""Application Entrypoint for Google ADK Web UI & CLI Execution."""
import os
import sys
from pathlib import Path

# Ensure package root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.harness.agent import root_agent, ReverseLogisticsHarness
from src.harness.context import CustomerTicket


def run_interactive_demo():
    print("=" * 70)
    print(" DEV FEST WORKSHOP: HARNESS ENGINEERING IN PRATICA")
    print(" Fashion Reverse Logistics & Exception Refunds")
    print("=" * 70)

    harness = ReverseLogisticsHarness()

    # Case 1: Standard compliant return (Italy, Leather jacket, 180 €)
    ticket_std = CustomerTicket(
        ticket_id="TICK-IT-101",
        customer_id="CUST-4421",
        country="IT",
        item_category="leather",
        item_description="Giacca in pelle marrone taglia M",
        purchase_price=180.0,
        days_since_delivery=12,
        complaint_text="Cucitura della tasca destra leggermente scucita.",
        has_original_tags=True,
        fraud_risk_score=15,
    )

    print("\n--- TEST CASE 1: Standard Compliant Return (Within Policy) ---")
    res1 = harness.execute_ticket(ticket_std)
    print(f"Action: {res1['authorization'].action}")
    print(f"Amount Approved: €{res1['authorization'].approved_amount:.2f}")
    print(f"Warehouse: {res1['authorization'].warehouse_code}")
    print(f"Gate Triggered: {res1['gate_result'].is_blocked}")
    print(f"Telemetry: {res1['telemetry'].duration_ms}ms, Cache Hit: {res1['telemetry'].cache_hit_rate}%")

    # Case 2: High value refund (> 500 €) -> Must trigger Policy Gate HITL
    ticket_hitl = CustomerTicket(
        ticket_id="TICK-FR-202",
        customer_id="CUST-8899",
        country="FR",
        item_category="luxury",
        item_description="Cappotto in Cashmere Loro Piana",
        purchase_price=850.0,
        days_since_delivery=10,
        complaint_text="Difetto nella fodera interna.",
        has_original_tags=True,
        fraud_risk_score=20,
    )

    print("\n--- TEST CASE 2: High-Value Return (> €500 -> Policy Gate HITL) ---")
    res2 = harness.execute_ticket(ticket_hitl)
    print(f"Action: {res2['authorization'].action}")
    print(f"Amount Requested: €{res2['authorization'].approved_amount:.2f}")
    print(f"HITL Blocked: {res2['gate_result'].is_blocked}")
    print(f"Supervisor Ticket: {res2['gate_result'].supervisor_ticket_id}")
    print(f"Reason: {res2['gate_result'].reason}")


if __name__ == "__main__":
    run_interactive_demo()

