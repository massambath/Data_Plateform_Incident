from fastapi import APIRouter
from api.services.observability_service import get_observability_report

router = APIRouter(prefix="/metrics", tags=["Observability"])

@router.get("/observability")
def observability_status():
    """
    Returns data observability health report
    """
    return get_observability_report()
