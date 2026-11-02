"""Component 3: Policy Gate (Human-In-The-Loop Guardrails)."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PolicyGateDecision(str, Enum):
    APPROVED = "APPROVED"
    ESCALATED_TO_HITL = "ESCALATED_TO_HITL"
    BLOCKED_FRAUD = "BLOCKED_FRAUD"


@dataclass
class PolicyGateResult:
    decision: PolicyGateDecision
    is_blocked: bool
    requires_human_approval: bool
    reason: str
    amount_requested: float
    supervisor_ticket_id: Optional[str] = None


class PolicyGate:
    """
    Evaluates business policy boundaries before autonomous actions are finalized.
    Enforces Human-In-The-Loop (HITL) for high financial exposure or security risks.
    """

    def __init__(
        self,
        refund_threshold: float = 500.0,
        fraud_risk_threshold: int = 70,
    ):
        self.refund_threshold = refund_threshold
        self.fraud_risk_threshold = fraud_risk_threshold

    def evaluate(
        self,
        ticket_id: str,
        refund_amount: float,
        fraud_risk_score: int = 0,
        customer_id: str = "",
    ) -> PolicyGateResult:
        """
        Intercepts proposed refund actions against safety and fraud policies.

        Returns:
            PolicyGateResult indicating whether the action is permitted or blocked for HITL review.
        """
        # Check 1: Fraud risk score threshold
        if fraud_risk_score > self.fraud_risk_threshold:
            escalation_id = f"HITL-FRD-{uuid.uuid4().hex[:8].upper()}"
            return PolicyGateResult(
                decision=PolicyGateDecision.BLOCKED_FRAUD,
                is_blocked=True,
                requires_human_approval=True,
                amount_requested=refund_amount,
                supervisor_ticket_id=escalation_id,
                reason=(
                    f"Customer {customer_id} has a Fraud Risk Score of {fraud_risk_score}/100 "
                    f"(exceeds threshold of {self.fraud_risk_threshold}). Payout halted for human fraud review."
                ),
            )

        # Check 2: High value refund threshold (> 500 €)
        if refund_amount > self.refund_threshold:
            escalation_id = f"HITL-VAL-{uuid.uuid4().hex[:8].upper()}"
            return PolicyGateResult(
                decision=PolicyGateDecision.ESCALATED_TO_HITL,
                is_blocked=True,
                requires_human_approval=True,
                amount_requested=refund_amount,
                supervisor_ticket_id=escalation_id,
                reason=(
                    f"Requested refund amount €{refund_amount:.2f} exceeds the autonomous threshold "
                    f"of €{self.refund_threshold:.2f}. Halted for human manager sign-off."
                ),
            )

        # Passed all policy checks
        return PolicyGateResult(
            decision=PolicyGateDecision.APPROVED,
            is_blocked=False,
            requires_human_approval=False,
            amount_requested=refund_amount,
            supervisor_ticket_id=None,
            reason=f"Refund of €{refund_amount:.2f} complies with autonomous processing policies.",
        )

