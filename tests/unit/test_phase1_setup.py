from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_phase1_setup_files_exist() -> None:
    required_files = [
        REPO_ROOT / "pyproject.toml",
        REPO_ROOT / "requirements.txt",
        REPO_ROOT / ".github/workflows/ci.yml",
        REPO_ROOT / "docker-compose.yml",
        REPO_ROOT / "README.md",
        REPO_ROOT / "scripts/seed-dev-identity.sh",
        REPO_ROOT / ".env.example",
        REPO_ROOT / ".pre-commit-config.yaml",
    ]

    for path in required_files:
        assert path.exists(), f"missing required file: {path.relative_to(REPO_ROOT)}"


def test_phase1_setup_files_reference_feature_quickstart() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "specs/001-paper-trading-platform/quickstart.md" in readme
