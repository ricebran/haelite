from src.services.status import StatusService


def test_status_service_reports_operational_defaults() -> None:
    service = StatusService()
    status = service.get_status()

    assert status["service"] == "haelite"
    assert status["status"] == "operational"
    assert status["incidents"] == []
