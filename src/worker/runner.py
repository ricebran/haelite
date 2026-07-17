from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Job:
    job_id: str
    name: str
    payload: dict[str, object] | None = None


class JobRunner:
    def __init__(self) -> None:
        self._jobs: list[Job] = []

    def enqueue(self, job: Job) -> None:
        self._jobs.append(job)

    def run_next(self) -> Job:
        if not self._jobs:
            raise RuntimeError("no queued jobs")
        return self._jobs.pop(0)
