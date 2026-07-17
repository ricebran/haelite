from fastapi import Request
from fastapi.responses import JSONResponse
from src.services.auth import AuthContext
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("x-user-id")
        if not auth_header:
            return JSONResponse(status_code=401, content={"detail": "missing authentication"})

        context = AuthContext(user_id=auth_header, roles=["researcher"])
        request.state.auth_context = context
        return await call_next(request)
