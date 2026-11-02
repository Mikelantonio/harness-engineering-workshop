"""Deterministic, offline-testable workshop tool functions."""

def estimate_lab_time(participants: int, steps: int) -> dict:
    """Estimate lab duration in minutes for participants and exercise steps.

    Args:
        participants: Number of attendees (1 to 200).
        steps: Number of steps in the lab (1 to 20).

    Returns:
        A structured result containing total_minutes and assumptions.
    """
    if not isinstance(participants, int) or isinstance(participants, bool) or not 1 <= participants <= 200:
        return {"status": "error", "message": "participants must be between 1 and 200"}
    if not isinstance(steps, int) or isinstance(steps, bool) or not 1 <= steps <= 20:
        return {"status": "error", "message": "steps must be between 1 and 20"}
    # Teaching heuristic, not a statistical prediction.
    base = steps * 4
    coordination = 10 if participants > 30 else 5 if participants > 15 else 0
    return {
        "status": "success",
        "total_minutes": base + coordination,
        "assumptions": "4 minutes per step plus a group-size coordination buffer",
    }
