import logging
import time
import uuid

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("device_systems")

limiter = Limiter(key_func=get_remote_address)


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:8]
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-Request-ID"] = request_id

        logger.info(
            "%s %s %s request_id=%s process_time=%s",
            request.method,
            request.url.path,
            response.status_code,
            request_id,
            f"{process_time:.4f}"
        )

        return response
