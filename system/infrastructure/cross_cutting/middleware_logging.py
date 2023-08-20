import logging
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestContextLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Any]],
    ) -> Response:
        """_summary_
        Args:
            request (Request)
            call_next (_type_)
        Returns:
            Response
        """
        await self.set_body(request, await request.body())
        request_body = await self.get_body(request)

        response = await call_next(request)

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        response_code = response.status_code
        response_headers = dict(response.headers)
        response_content = response_body.decode()

        if (
            "content-type" in request.headers
            and "multipart/form-data" in request.headers["content-type"]
        ):
            body = ""
        else:
            body = str(request_body.decode())

        document = {
            "@timestamp": datetime.utcnow().isoformat(),
            "method": str(request.method),
            "url": str(request.url),
            "headers": str(dict(request.headers)),
            "body": body,  # type: ignore
            "path-params": str(dict(request.path_params)),
            "query-params": str(dict(request.query_params)),
            "cookies": str(request.cookies),
            "response-code": str(response_code),
            "response-headers": str(response_headers),
            "response-content": str(response_content),
        }

        logger = logging.getLogger("short-url")
        logger.info(document)

        return Response(
            content=response_body,  # type: ignore
            status_code=response_code,
            headers=dict(response_headers),
            media_type=response.media_type,  # type: ignore
        )

    async def set_body(self, request: Request, body: bytes) -> None:
        """Set body from RequestArgs"""

        async def receive() -> Dict[str, Any]:
            return {"type": "http.request", "body": body}

        request._receive = receive  # noqa: WPS437

    async def get_body(self, request: Request) -> bytes:
        """Get body from request"""
        body = await request.body()
        await self.set_body(request, body)
        return body
