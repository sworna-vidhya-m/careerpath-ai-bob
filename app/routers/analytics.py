"""Analytics router — intelligent endpoints reserved for IBM Bob.

This module is intentionally a stub. The following endpoints will be
implemented during the hackathon by IBM Bob:

  - GET /analytics/skill-gap/{employee_id}
  - GET /analytics/career-recommendations/{employee_id}
  - POST /analytics/trigger-bench-learning
  - GET /analytics/industry-trends/{business_unit_id}
  - GET /analytics/skill-heatmap

Until then, this router exposes a single health probe so the route is
registered and the smoke test can verify wiring.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/health")
def analytics_health() -> dict[str, str]:
    """Health probe confirming the analytics router is mounted."""
    return {"status": "ok", "module": "analytics", "implemented": "pending-bob"}
