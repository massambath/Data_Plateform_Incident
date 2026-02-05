# api/services/observability_service.py
from ingestion.validators import DBValidator

def get_observability_report():
    """
    Run all DB checks and return the observability report as a dict
    """
    validator = DBValidator()
    return validator.run_all_checks()
