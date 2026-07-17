from __future__ import annotations

from pathlib import Path


class LocalArtifactStore:
    def __init__(self, *, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or Path("/tmp/haelite-artifacts")
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def put_bytes(self, path: str, data: bytes) -> None:
        target = self.base_dir / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def get_bytes(self, path: str) -> bytes:
        return (self.base_dir / path).read_bytes()
