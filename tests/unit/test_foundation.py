from pathlib import Path

from fastapi.testclient import TestClient
from src.api.app import app
from src.models import (
    ApprovalRecord,
    DataSnapshot,
    Hypothesis,
    Incident,
    PaperCandidate,
    RiskConfiguration,
    ValidationRun,
)
from src.services.audit import AuditService
from src.storage.local import LocalArtifactStore


def test_foundation_models_are_importable() -> None:
    assert Hypothesis.__name__ == "Hypothesis"
    assert DataSnapshot.__name__ == "DataSnapshot"
    assert ValidationRun.__name__ == "ValidationRun"
    assert RiskConfiguration.__name__ == "RiskConfiguration"
    assert PaperCandidate.__name__ == "PaperCandidate"
    assert ApprovalRecord.__name__ == "ApprovalRecord"
    assert Incident.__name__ == "Incident"


def test_audit_service_records_events() -> None:
    service = AuditService()
    event = service.record_event(event_type="created", object_type="hypothesis", object_id="h-1")

    assert event.event_type == "created"
    assert event.object_type == "hypothesis"
    assert service.list_events("h-1")[0].object_id == "h-1"


def test_local_artifact_store_round_trips_bytes(tmp_path: Path) -> None:
    store = LocalArtifactStore(base_dir=tmp_path)
    store.put_bytes("artifacts/demo.parquet", b"demo")

    assert store.get_bytes("artifacts/demo.parquet") == b"demo"


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "haelite"}
