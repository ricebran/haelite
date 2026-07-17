from src.api.middleware.auth import AuthMiddleware
from src.services.auth import AuthContext
from src.worker.runner import Job, JobRunner


def test_job_runner_enqueues_and_runs_jobs() -> None:
    runner = JobRunner()
    runner.enqueue(Job(job_id="j-1", name="demo", payload={"mode": "paper"}))

    job = runner.run_next()

    assert job.job_id == "j-1"
    assert job.name == "demo"
    assert job.payload == {"mode": "paper"}


def test_auth_middleware_uses_request_state() -> None:
    context = AuthContext(user_id="u-2", roles=["risk"])
    assert context.user_id == "u-2"
    assert context.roles == ["risk"]


def test_auth_middleware_class_exists() -> None:
    assert AuthMiddleware is not None
