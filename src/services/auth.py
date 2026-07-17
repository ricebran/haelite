from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AuthContext:
    user_id: str
    roles: list[str] = field(default_factory=list)


def get_authenticated_user(context: AuthContext) -> str:
    return context.user_id


def require_roles(context: AuthContext, allowed_roles: set[str]) -> bool:
    return bool(set(context.roles) & allowed_roles)
