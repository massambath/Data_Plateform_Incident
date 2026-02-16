# tests/test_ingestion.py
import pytest
from ingestion.generate_data import generate_incident
from ingestion.validators import validate_incident
from datetime import datetime

def test_generate_incident_structure():
    start_date = datetime.now()
    incident = generate_incident(start_date)

    assert isinstance(incident, dict)
    assert "service_name" in incident
    assert "severity" in incident
    assert "incident_type" in incident
    assert "description" in incident
    assert "created_at" in incident
    assert "resolved_at" in incident

def test_validate_incident_valid():
    from datetime import datetime
    incident = {
        "service_name": "auth-service",
        "severity": "HIGH",
        "incident_type": "OUTAGE",
        "description": "Test",
        "created_at": datetime.now(),
        "resolved_at": None
    }
    assert validate_incident(incident) is True

def test_validate_incident_missing_field():
    incident = {
        "service_name": "auth-service",
        # "severity" missing
        "incident_type": "OUTAGE",
        "description": "Test",
        "created_at": datetime.now(),
        "resolved_at": None
    }
    with pytest.raises(ValueError):
        validate_incident(incident)

