"""Component 5: Verify / Verifier (Output Schema & Business Contract Validation)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


@dataclass
class ReturnAuthorization:
    ticket_id: str
    action: str  # "REFUND", "REPLACE", "REJECT", "HITL_ESCALATION"
    approved_amount: float
    warehouse_code: str
    reason: str
    customs_declaration_required: bool = False
    customs_notes: Optional[str] = None


class VerificationError(Exception):
    """Raised when an agent output violates the schema or business constraints."""
    pass


class ReturnAuthorizationVerifier:
    """
    Validates that return authorization outputs strictly adhere to
    the JSON schema and business constraints (e.g. existing warehouse codes).
    """

    ALLOWED_ACTIONS = {"REFUND", "REPLACE", "REJECT", "HITL_ESCALATION"}

    def __init__(self, warehouses_path: Optional[Path] = None):
        if warehouses_path is None:
            warehouses_path = (
                Path(__file__).resolve().parent.parent.parent
                / "assets"
                / "data"
                / "warehouses.json"
            )
        self.warehouses_path = Path(warehouses_path)
        self._authorized_warehouses: Set[str] = self._load_warehouses()

    def _load_warehouses(self) -> Set[str]:
        if not self.warehouses_path.exists():
            return {"WMS-MIL-01", "WMS-PAR-04", "WMS-FRA-02", "WMS-LON-03"}
        try:
            data = json.loads(self.warehouses_path.read_text(encoding="utf-8"))
            return {item["code"] for item in data.get("authorized_warehouses", [])}
        except Exception:
            return {"WMS-MIL-01", "WMS-PAR-04", "WMS-FRA-02", "WMS-LON-03"}

    @property
    def authorized_warehouses(self) -> Set[str]:
        return set(self._authorized_warehouses)

    def verify(
        self,
        raw_output: Any,
        origin_country: Optional[str] = None,
    ) -> ReturnAuthorization:
        """
        Parses and verifies raw agent output (dict or JSON string).

        Raises:
            VerificationError: If parsing fails or business invariants are violated.
        """
        if isinstance(raw_output, str):
            try:
                # Strip markdown code blocks if the LLM returned ```json ... ```
                cleaned = raw_output.strip()
                if cleaned.startswith("```"):
                    lines = cleaned.splitlines()
                    cleaned = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
                data = json.loads(cleaned)
            except Exception as e:
                raise VerificationError(f"Output is not valid JSON: {e}") from e
        elif isinstance(raw_output, dict):
            data = raw_output
        else:
            raise VerificationError(f"Expected dict or JSON string, got {type(raw_output).__name__}")

        # Field validation
        ticket_id = data.get("ticket_id")
        action = data.get("action")
        amount = data.get("approved_amount")
        warehouse_code = data.get("warehouse_code")
        reason = data.get("reason", "")
        customs_declaration = bool(data.get("customs_declaration_required", False))
        customs_notes = data.get("customs_notes")

        if not ticket_id:
            raise VerificationError("Missing required field 'ticket_id'")

        if action not in self.ALLOWED_ACTIONS:
            raise VerificationError(
                f"Invalid action '{action}'. Allowed actions: {sorted(self.ALLOWED_ACTIONS)}"
            )

        if amount is None or not isinstance(amount, (int, float)) or amount < 0:
            raise VerificationError(f"Invalid approved_amount '{amount}'. Must be a non-negative number.")

        if not warehouse_code or warehouse_code not in self._authorized_warehouses:
            raise VerificationError(
                f"Unauthorized or unknown warehouse_code '{warehouse_code}'. "
                f"Authorized codes: {sorted(self._authorized_warehouses)}"
            )

        # Cross-border routing rules
        if origin_country and origin_country.upper() in {"UK", "GB"}:
            if warehouse_code != "WMS-LON-03":
                raise VerificationError(
                    f"UK returns must be routed exclusively to 'WMS-LON-03' (got '{warehouse_code}')."
                )
            if not customs_declaration:
                raise VerificationError("UK returns require 'customs_declaration_required=True'.")

        return ReturnAuthorization(
            ticket_id=str(ticket_id),
            action=str(action),
            approved_amount=float(amount),
            warehouse_code=str(warehouse_code),
            reason=str(reason),
            customs_declaration_required=customs_declaration,
            customs_notes=customs_notes,
        )

