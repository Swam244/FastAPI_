from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response, status,HTTPException
from typing import Dict
from collections import defaultdict
import time
import secrets


class SimpleRateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int, window_seconds: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_counts: Dict[str, list] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        curr_time = time.time()

        self.request_counts[client_ip] = [
            timestamp for timestamp in self.request_counts[client_ip]
            if curr_time - timestamp < self.window_seconds
        ]

        if len(self.request_counts[client_ip]) > self.max_requests:
            return Response(content="Request per second limit exceeded !!", status_code=status.HTTP_429_TOO_MANY_REQUESTS)

        self.request_counts[client_ip].append(curr_time)
        response = await call_next(request)
        return response


class CSRFMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key: str):
        super().__init__(app)
        self.secret_key = secret_key 

    async def dispatch(self, request: Request, call_next):
        if "csrf_token" not in request.session:
            request.session["csrf_token"] = secrets.token_hex(16)

        response = await call_next(request)
        response.set_cookie(
            key="csrf_token",
            value=request.session["csrf_token"],
            httponly=True,
            secure=True,
            samesite="Strict"
        )
        return response