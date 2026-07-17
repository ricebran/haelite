from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from src.api.middleware.auth import AuthMiddleware


def test_auth_middleware_allows_request_with_user_header() -> None:
    app = FastAPI()
    app.add_middleware(AuthMiddleware)

    @app.get("/demo")
    def demo(request: Request) -> dict[str, str]:
        return {"user_id": request.state.auth_context.user_id}

    client = TestClient(app)
    response = client.get("/demo", headers={"x-user-id": "u-7"})

    assert response.status_code == 200
    assert response.json() == {"user_id": "u-7"}


def test_auth_middleware_rejects_missing_user_header() -> None:
    app = FastAPI()
    app.add_middleware(AuthMiddleware)

    @app.get("/demo")
    def demo(request: Request) -> dict[str, bool]:
        return {"ok": True}

    client = TestClient(app)
    response = client.get("/demo")

    assert response.status_code == 401
