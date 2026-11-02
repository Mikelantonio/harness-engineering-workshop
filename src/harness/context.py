"""Component 1: Context Builder (Stable Zone vs Volatile Zone)."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class CustomerTicket:
    """Represents a customer's return and refund request."""
    ticket_id: str
    customer_id: str
    country: str
    item_category: str
    item_description: str
    purchase_price: float
    days_since_delivery: int
    complaint_text: str
    has_original_tags: bool = True
    fraud_risk_score: int = 10
    image_paths: List[str] = field(default_factory=list)


class ContextBuilder:
    """
    Constructs the LLM context separating the Stable Zone (policies)
    from the Volatile Zone (ticket payload) to optimize prompt caching.
    """

    def __init__(self, policy_path: Optional[Path] = None):
        if policy_path is None:
            policy_path = (
                Path(__file__).resolve().parent.parent.parent
                / "assets"
                / "policies"
                / "return_policy_global.md"
            )
        self.policy_path = Path(policy_path)
        self._cached_policy: Optional[str] = None

    def get_stable_policy(self) -> str:
        """Loads and caches the immutable international return policy."""
        if self._cached_policy is None:
            if self.policy_path.exists():
                self._cached_policy = self.policy_path.read_text(encoding="utf-8")
            else:
                self._cached_policy = "# DEFAULT RETURN POLICY\nStandard 30-day return policy applies."
        return self._cached_policy

    def build_system_instruction(self) -> str:
        """Returns the base system instruction for the fashion reverse logistics agent."""
        return (
            "Sei un assistente per la logistica inversa fashion. Valuta i resi e reclami cliente. "
            "Usa SEMPRE 'calculate_depreciated_refund' per calcolare l'importo corretto del rimborso. "
            "Usa 'generate_wms_return_label' per emettere l'etichetta verso un magazzino autorizzato. "
            "Rispetta sempre le soglie di policy e le regole doganali."
        )

    def build_volatile_context(self, ticket: CustomerTicket) -> str:
        """Formats the mutable ticket information."""
        return (
            f"=== VOLATILE CONTEXT: TICKET #{ticket.ticket_id} ===\n"
            f"- Customer ID: {ticket.customer_id} (Fraud Risk Score: {ticket.fraud_risk_score}/100)\n"
            f"- Country of Origin: {ticket.country}\n"
            f"- Item Category: {ticket.item_category}\n"
            f"- Description: {ticket.item_description}\n"
            f"- Original Purchase Price: €{ticket.purchase_price:.2f}\n"
            f"- Days Since Delivery: {ticket.days_since_delivery}\n"
            f"- Original Tags Present: {'Yes' if ticket.has_original_tags else 'No'}\n"
            f"- Customer Complaint: \"{ticket.complaint_text}\"\n"
            f"- Attached Photos: {', '.join(ticket.image_paths) if ticket.image_paths else 'None'}\n"
        )

    def build_prompt(self, ticket: CustomerTicket) -> str:
        """
        Combines Stable Zone (prefix) and Volatile Zone (suffix).
        The stable policy stays identical across all requests, enabling LLM Prompt Caching.
        """
        stable_zone = (
            "=== STABLE CONTEXT: GLOBAL RETURN POLICIES & CUSTOMS EXCEPTIONS ===\n"
            f"{self.get_stable_policy()}\n\n"
        )
        volatile_zone = self.build_volatile_context(ticket)
        task_instruction = (
            "\n=== TASK ===\n"
            "Valuta la richiesta di reso. Determina l'azione da intraprendere (REFUND, REPLACE, REJECT o ESCALATE), "
            "calcola l'importo corretto usando i tool deterministici e assegna il magazzino WMS di destinazione conforme."
        )
        return stable_zone + volatile_zone + task_instruction

