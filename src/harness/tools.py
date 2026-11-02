"""Component 4: Tools / Runtime (Deterministic Business Logic)."""
from __future__ import annotations

import math
from typing import Any, Dict


def calculate_depreciated_refund(
    original_price: float,
    condition: str,
    has_original_tags: bool,
    days_since_delivery: int,
) -> Dict[str, Any]:
    """
    Deterministic calculation for refund depreciation based on policy rules.
    Prevents LLM math hallucinations and enforces strict business rules.

    Args:
        original_price: Original purchase price in EUR (> 0).
        condition: Observed condition of the returned item
                   ('intact_defect_origin', 'seam_tear_repairable',
                    'permanent_stain_or_fabric_tear', 'altered_or_tampered').
        has_original_tags: Whether original tags and hygiene seals are intact.
        days_since_delivery: Number of calendar days since delivery.

    Returns:
        Dict containing approved_refund, penalty_percentage, store_credit_eligible, and rationale.
    """
    if original_price <= 0:
        return {
            "approved_refund": 0.0,
            "penalty_percentage": 100.0,
            "status": "REJECTED",
            "reason": "Original purchase price must be greater than zero.",
        }

    # Rule 1: Outside return window
    if days_since_delivery > 45:
        return {
            "approved_refund": 0.0,
            "penalty_percentage": 100.0,
            "status": "REJECTED",
            "reason": f"Request received {days_since_delivery} days after delivery (limit: 45 days).",
        }

    late_penalty = 0.20 if days_since_delivery > 30 else 0.0

    # Rule 2: Hygiene seals and tags
    if not has_original_tags:
        return {
            "approved_refund": 0.0,
            "penalty_percentage": 100.0,
            "status": "REJECTED",
            "reason": "Original security/hygiene tags are missing or tampered.",
        }

    # Rule 3: Condition-based depreciation
    condition_penalties = {
        "intact_defect_origin": 0.0,          # 100% refund (factory defect)
        "seam_tear_repairable": 0.15,         # 85% refund for cash, or repairable
        "permanent_stain_or_fabric_tear": 0.40,  # 60% refund
        "altered_or_tampered": 1.0,           # 0% refund
    }

    base_penalty = condition_penalties.get(condition, 0.40)
    total_penalty = min(1.0, base_penalty + late_penalty)
    refund_factor = 1.0 - total_penalty

    approved_refund = round(original_price * refund_factor, 2)

    return {
        "original_price": round(original_price, 2),
        "approved_refund": approved_refund,
        "penalty_percentage": round(total_penalty * 100, 1),
        "status": "APPROVED" if approved_refund > 0 else "REJECTED",
        "condition_evaluated": condition,
        "reason": f"Evaluated condition '{condition}' with {total_penalty * 100:.0f}% total depreciation.",
    }


def generate_wms_return_label(
    order_id: str,
    warehouse_code: str,
    carrier: str = "DHL_EXPRESS",
) -> Dict[str, Any]:
    """
    Generates an official return shipping label in the Warehouse Management System (WMS).

    Args:
        order_id: Order or ticket identifier.
        warehouse_code: Destination WMS Hub code (e.g., 'WMS-MIL-01').
        carrier: Logistics carrier name.

    Returns:
        Dict with tracking number, return label URL, and routing info.
    """
    import hashlib
    hash_digest = hashlib.md5(f"{order_id}-{warehouse_code}".encode()).hexdigest()[:8].upper()
    tracking_number = f"RTN-{carrier[:3]}-{hash_digest}"
    label_url = f"https://wms.fashionhub.internal/labels/{tracking_number}.pdf"

    return {
        "status": "LABEL_GENERATED",
        "order_id": order_id,
        "destination_warehouse": warehouse_code,
        "carrier": carrier,
        "tracking_number": tracking_number,
        "label_url": label_url,
    }

