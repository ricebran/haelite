from src.models import Base
from src.services.auth import AuthContext, get_authenticated_user, require_roles


def test_auth_helpers_expose_expected_context() -> None:
    ctx = AuthContext(user_id="u-1", roles=["researcher", "risk"])

    assert ctx.user_id == "u-1"
    assert ctx.roles == ["researcher", "risk"]


def test_auth_helpers_validate_roles() -> None:
    ctx = AuthContext(user_id="u-1", roles=["researcher"])

    assert get_authenticated_user(ctx) == "u-1"
    assert require_roles(ctx, {"researcher"}) is True
    assert require_roles(ctx, {"risk"}) is False


def test_models_module_exposes_sqlalchemy_base() -> None:
    assert Base is not None
